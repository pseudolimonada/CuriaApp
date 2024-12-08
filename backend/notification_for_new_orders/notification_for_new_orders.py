from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

connections = {}

async def notify_new_order(business_id: str, order_data: dict):
    """
    Notify all active WebSocket connections for the given business_id.
    """
    if business_id in connections:
        for connection in connections[business_id]:
            await connection.send_json(order_data)
        
@router.websocket("/businesses/<int:business_id>/notifications_for_new_orders")
async def websocket_new_orders(websocket: WebSocket, business_id: str):
    """
    WebSocket endpoint to handle real time notifications for new orders
    """
    await websocket.accept()
    
    if business_id not in connections:
        connections[business_id] = []
    connections[business_id].append(websocket)
    
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connections[business_id].remove(websocket)
        if not connections[business_id]:
            del connections[business_id]