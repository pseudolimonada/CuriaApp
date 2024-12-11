# Versao 2
import redis
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
import json

app = FastAPI
redis_client = redis.StrictRedis(host='localhost', port=6379,db=0)
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
            
@app.websocket("/businesses/<int:business_id>/notifications_for_new_orders")
async def websocket_new_orders(websocket: WebSocket, business_id: str):
    """
    WebSocket endpoint for real-time order notification
    """
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
<<<<<<< HEAD
        
=======

        
>>>>>>> 7958eb9 (Added second version (almost completed) of notification_for_new_orders.py)
