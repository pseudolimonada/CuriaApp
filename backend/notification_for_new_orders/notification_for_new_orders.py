# Versao 2
import redis, json, subprocess, sys, importlib.util
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from flask import Blueprint, request, jsonify
from db_models import Business
from extensions import db
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation


# Verify in file if packages are installed instead in a bash file
package_names = ['cognitive-complexity', 'pydriller']

for package_name in package_names:
    if importlib.util.find_spec(package_name) is None:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])


app = FastAPI()
redis_client = redis.StrictRedis(host='localhost', port=6379,db=0)
businesses_blueprint = Blueprint('businesses', __name__)

active_connections = {}  # Local cache for in-memory connections (for this instance)

async def notify_new_order(business_id: str, notification:dict):
    """
    Notify WebSocket connections for a specific business.
    """
    redis_key = f"business:{business_id}:connections"
    connections = redis_client.smembers(redis_key)
    
    for con_id in connections:
        try:
            websocket = active_connections[con_id.decode()]
            await websocket.send_json(notification)
        except Exception:
            # Remove invalid connections
            redis_client.srem(redis_key,con_id)
            active_connections.pop(con_id.decode(),None)
            
@app.websocket("/businesses/{business_id}/notifications_for_new_orders")
async def websocket_new_orders(websocket: WebSocket, business_id: str):
    """
    WebSocket endpoint for real-time order notification
    """
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code = 500)
        return
    

    conn_id = str(id(websocket)) # Unique ID for a connection
    redis_key = f"business:{business_id}.connections"
    await websocket.accept()
    redis_client.sadd(redis_key, conn_id)
    active_connections[conn_id] = websocket
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        print(f"Client disconnected: {conn_id}")
    except Exception as e:
        print(f"Error with connection {conn_id}: {str(e)}")
    finally:
        redis_client.srem(redis_key, conn_id)
        active_connections.pop(conn_id, None)