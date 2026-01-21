"""
WebSocket Server with Google ADK Agent
Handles real-time communication with React UI using intelligent agent
"""
import asyncio
import json
import os
import websockets
from typing import Set
from websockets.server import WebSocketServerProtocol

from session_manager import get_session_manager
from adk_agent import get_adk_agent


class WebSocketServer:
    """WebSocket server with Google ADK Agent integration"""
    
    def __init__(self, host: str = "localhost", port: int = 8000):
        self.host = host
        self.port = port
        self.clients: Set[WebSocketServerProtocol] = set()
        self.session_manager = get_session_manager()
        
        # Initialize Google ADK Agent
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("⚠️  WARNING: GOOGLE_API_KEY not set. Agent will use fallback logic.")
            print("   Set it with: export GOOGLE_API_KEY='your-api-key'")
        
        self.agent = get_adk_agent(api_key=api_key)
        print("🤖 Google ADK Agent initialized")
    
    async def handle_client(self, websocket: WebSocketServerProtocol):
        """Handle individual client connection"""
        print(f"✅ Client connected from {websocket.remote_address}")
        self.clients.add(websocket)
        session_id = None
        
        try:
            # Create session
            session_id = self.session_manager.create_session()
            print(f"📝 Created session: {session_id}")
            
            # Get initial widget from agent
            session = self.session_manager.get_session(session_id)
            response = await self.agent.process_user_action(
                action="connect",
                session_context=session["context"]
            )
            
            await self._send_response(websocket, session_id, response)
            
            # Handle incoming messages
            async for message in websocket:
                await self.handle_message(websocket, message, session_id)
        
        except websockets.exceptions.ConnectionClosed:
            print(f"❌ Client disconnected")
        except Exception as e:
            print(f"❌ Error handling client: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.clients.remove(websocket)
            if session_id:
                self.session_manager.delete_session(session_id)
                print(f"🗑️  Deleted session: {session_id}")
    
    async def handle_message(self, websocket: WebSocketServerProtocol, message: str, session_id: str):
        """Handle incoming message from client"""
        try:
            data = json.loads(message)
            action = data.get("action")
            
            print(f"📨 Received action: {action}")
            
            # Get current session
            session = self.session_manager.get_session(session_id)
            if not session:
                print(f"❌ Session not found: {session_id}")
                return
            
            # Update session context based on action
            if action == "select_date":
                self.session_manager.update_session(session_id, {
                    "context": {
                        "selected_date_value": data.get("date"),
                        "selected_date": data.get("label", data.get("date"))
                    }
                })
                session = self.session_manager.get_session(session_id)
                print(f"📅 Date selected: {data.get('date')}")
            
            elif action == "select_time":
                self.session_manager.update_session(session_id, {
                    "context": {
                        "selected_time_value": data.get("time"),
                        "selected_time": data.get("label", data.get("time"))
                    }
                })
                session = self.session_manager.get_session(session_id)
                print(f"⏰ Time selected: {data.get('time')}")
            
            elif action == "confirm_timezone":
                # Get timezone details
                from widget_populator import get_widget_populator
                tz_abbr = data.get("timezone")
                tz_details = get_widget_populator().get_timezone_by_abbr(tz_abbr)
                
                self.session_manager.update_session(session_id, {
                    "context": {
                        "timezone": tz_details["label"],
                        "timezone_abbr": tz_details["value"],
                        "current_action": None
                    }
                })
                session = self.session_manager.get_session(session_id)
                print(f"🌍 Timezone changed to: {tz_details['label']}")
            
            elif action == "change_timezone":
                self.session_manager.update_session(session_id, {
                    "context": {"current_action": "selecting_timezone"}
                })
                session = self.session_manager.get_session(session_id)
                print("🌍 Timezone change requested (follow-up action)")
            
            elif action == "close_widget":
                await websocket.send(json.dumps({
                    "type": "closed",
                    "message": "Widget closed"
                }))
                return
            
            # Let agent process the action
            response = await self.agent.process_user_action(
                action=action,
                session_context=session["context"],
                data=data
            )
            
            await self._send_response(websocket, session_id, response)
        
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON: {message}")
        except Exception as e:
            print(f"❌ Error handling message: {e}")
            import traceback
            traceback.print_exc()
    
    async def _send_response(
        self,
        websocket: WebSocketServerProtocol,
        session_id: str,
        response: dict
    ):
        """Send response to client"""
        response_type = response.get("type")
        
        if response_type == "widget_render":
            await websocket.send(json.dumps({
                "type": "widget_render",
                "session_id": session_id,
                "widget": response["widget"]
            }))
        
        elif response_type == "meeting_scheduled":
            await websocket.send(json.dumps({
                "type": "meeting_scheduled",
                "session_id": session_id,
                "meeting": response["meeting"],
                "message": response["message"]
            }))
        
        elif response_type == "agent_message":
            await websocket.send(json.dumps({
                "type": "message",
                "session_id": session_id,
                "message": response["message"]
            }))
        
        elif response_type == "error":
            await websocket.send(json.dumps({
                "type": "error",
                "session_id": session_id,
                "message": response.get("message", "An error occurred")
            }))
    
    async def cleanup_task(self):
        """Background task to cleanup expired sessions"""
        while True:
            await asyncio.sleep(300)  # 5 minutes
            cleaned = self.session_manager.cleanup_expired_sessions()
            if cleaned > 0:
                print(f"🧹 Cleaned up {cleaned} expired sessions")
    
    async def start(self):
        """Start the WebSocket server"""
        # Start cleanup task
        asyncio.create_task(self.cleanup_task())
        
        print("="*60)
        print("🚀 ADK WebSocket Server with Google Gemini Agent")
        print("="*60)
        print(f"📡 Server: ws://{self.host}:{self.port}")
        print(f"🤖 Agent: Gemini 2.0 Flash")
        print(f"🔧 Tools: MCP Widget Schemas")
        print(f"💾 Sessions: In-memory storage")
        print("="*60)
        
        if not os.getenv("GOOGLE_API_KEY"):
            print("⚠️  Running in FALLBACK mode (no API key)")
            print("   To enable full agent: export GOOGLE_API_KEY='your-key'")
            print("="*60)
        
        async with websockets.serve(self.handle_client, self.host, self.port):
            await asyncio.Future()  # Run forever


async def main():
    """Main entry point"""
    server = WebSocketServer()
    await server.start()


if __name__ == "__main__":
    print("\n🎯 Starting ADK Server with Google Gemini Agent...\n")
    asyncio.run(main())
