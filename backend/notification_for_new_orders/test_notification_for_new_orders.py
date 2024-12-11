import pytest
import httpx
import websockets
import asyncio
import json

BASE_URL = "http://localhost:8000"  # Update if the server runs on a different host/port
WS_URL = "ws://localhost:6379"  # WebSocket base URL

@pytest.mark.asyncio
async def test_websocket_notifications():
    """
    Test WebSocket notifications on new order creation.
    """
    business_id = "test_business"
    token = "dummy_token"  # Replace with a valid token if needed

    # Mock order data
    order_data = {
        "user_id": "test_user",
        "order_date": "2024-12-10",
        "order_data": [
            {"product_id": "product1", "product_quantity": "2"},
            {"product_id": "product2", "product_quantity": "3"},
        ],
    }

    # Function to simulate WebSocket client
    async def websocket_client():
        async with websockets.connect(
            f"{WS_URL}/businesses/{business_id}/notifications_for_new_orders?token={token}"
        ) as ws:
            # Wait for server message (with a timeout)
            try:
                message = await asyncio.wait_for(ws.recv(), timeout=5)
                return json.loads(message)
            except asyncio.TimeoutError:
                pytest.fail("WebSocket notification timed out")

    # Launch WebSocket client
    websocket_task = asyncio.create_task(websocket_client())

    # Create a new order via REST API
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/orders/{business_id}/orders", json=order_data)

    # Verify REST API response
    assert response.status_code == 200, "Failed to submit order"

    # Retrieve WebSocket notification
    ws_message = await websocket_task

    # Verify WebSocket notification content
    assert ws_message["user_id"] == order_data["user_id"], "User ID mismatch in notification"
    assert ws_message["order_date"] == order_data["order_date"], "Order date mismatch in notification"
    assert ws_message["order_items"] == order_data["order_data"], "Order items mismatch in notification"
