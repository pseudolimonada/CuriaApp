from locust import User, task, between
import websocket

class WebSocketUser(User):
    wait_time = between(1, 5)

    @task
    def test_websocket(self):
        ws = websocket.WebSocket()
        try:
            ws.connect("wss://your-domain.com/businesses/test-business-id/notifications_for_new_orders?token=your-jwt-token")
            ws.send("Test message")
            response = ws.recv()
            print(f"Received: {response}")
        finally:
            ws.close()