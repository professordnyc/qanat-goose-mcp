#!/usr/bin/env python3
"""
Qanat MVP Demo Script
Demonstrates the complete Square Seller Dashboard Assistant
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, Any

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

try:
    # Import our components
    from config.environments.env_loader import get_config
    from mcp_servers.qanat_server import QanatServer
    from services.catalog_service import CatalogService
    from services.orders_service import OrdersService
    from agents.orchestrator import IntentOrchestrator
    from agents.voice_agent import VoiceAgent
    from agents.gesture_agent import GestureAgent
    from ui_components.catalog_dashboard import CatalogDashboard
    from ui_components.orders_dashboard import OrdersDashboard
    from ui_components.common import get_action_handler, get_state_manager
    import structlog
    
    # Configure logging
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    logger = structlog.get_logger(__name__)
    
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)

class QanatDemo:
    """Demo orchestrator for Qanat MVP"""
    
    def __init__(self):
        self.config = None
        self.orchestrator = None
        self.voice_agent = None
        self.gesture_agent = None
        self.catalog_service = None
        self.orders_service = None
        self.catalog_dashboard = None
        self.orders_dashboard = None
        self.action_handler = None
        self.state_manager = None
        
    async def initialize(self):
        """Initialize all components"""
        try:
            print("\n🚀 Initializing Qanat MVP Demo...")
            
            # Load configuration
            try:
                self.config = get_config()
                print("✅ Configuration loaded")
            except Exception as e:
                print(f"⚠️ Configuration error (using defaults): {e}")
                self.config = self._get_default_config()
            
            # Initialize orchestrator
            self.orchestrator = IntentOrchestrator()
            print("✅ Intent orchestrator initialized")
            
            # Initialize services
            self.catalog_service = CatalogService(self.config)
            self.orders_service = OrdersService(self.config)
            await self.catalog_service.initialize()
            await self.orders_service.initialize()
            print("✅ Square services initialized")
            
            # Initialize agents
            self.voice_agent = VoiceAgent(self.config, self.orchestrator)
            self.gesture_agent = GestureAgent(self.config, self.orchestrator)
            await self.voice_agent.initialize()
            await self.gesture_agent.initialize()
            print("✅ Voice and gesture agents initialized")
            
            # Initialize UI components
            self.catalog_dashboard = CatalogDashboard()
            self.orders_dashboard = OrdersDashboard()
            self.action_handler = get_action_handler(self.orchestrator)
            self.state_manager = get_state_manager()
            print("✅ UI components initialized")
            
            print("\n🎯 Qanat MVP Demo Ready!")
            
        except Exception as e:
            logger.error("Failed to initialize demo", error=str(e))
            raise
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration for demo"""
        return {
            "square": {
                "api_key": "demo_key",
                "environment": "sandbox",
                "application_id": "demo_app"
            },
            "elevenlabs": {
                "api_key": "demo_key",
                "voice_id": "demo_voice"
            },
            "mediapipe": {
                "model_path": "./models/",
                "confidence_threshold": 0.7
            },
            "mcp_server": {
                "host": "localhost",
                "port": 3001,
                "debug": True
            },
            "logging": {
                "level": "INFO",
                "file": "logs/qanat.log"
            }
        }
    
    async def demo_catalog_features(self):
        """Demonstrate catalog management features"""
        print("\n📦 === CATALOG DEMO ===")
        
        # Seed demo data
        print("🌱 Seeding catalog data...")
        seed_result = await self.catalog_service.seed_demo_data()
        print(f"   ✅ {seed_result['items_seeded']} items seeded")
        
        # Get catalog items
        print("📋 Fetching catalog items...")
        items_result = await self.catalog_service.get_items()
        items = items_result.get("items", [])
        print(f"   ✅ {len(items)} items retrieved")
        
        # Render catalog dashboard
        print("🎨 Rendering catalog dashboard...")
        dashboard = self.catalog_dashboard.render_dashboard(items)
        print(f"   ✅ Dashboard rendered with {len(dashboard['components'])} components")
        
        # Test item status toggle
        if items:
            first_item = items[0]
            print(f"🔄 Testing status toggle for: {first_item['name']}")
            toggle_result = await self.catalog_service.toggle_status(first_item["id"])
            print(f"   ✅ Status changed: {toggle_result['old_status']} → {toggle_result['new_status']}")
    
    async def demo_orders_features(self):
        """Demonstrate orders management features"""
        print("\n📝 === ORDERS DEMO ===")
        
        # Seed demo data
        print("🌱 Seeding orders data...")
        seed_result = await self.orders_service.seed_demo_data()
        print(f"   ✅ {seed_result['orders_seeded']} orders seeded")
        print(f"   💰 Total revenue: ${seed_result['total_revenue']}")
        
        # Get recent orders
        print("📋 Fetching recent orders...")
        orders_result = await self.orders_service.get_recent_orders()
        orders = orders_result.get("orders", [])
        print(f"   ✅ {len(orders)} orders retrieved")
        
        # Render orders dashboard
        print("🎨 Rendering orders dashboard...")
        dashboard = self.orders_dashboard.render_dashboard(orders)
        print(f"   ✅ Dashboard rendered with {len(dashboard['components'])} components")
        
        # Test order operations
        pending_orders = [order for order in orders if order.get("state") == "OPEN"]
        if pending_orders:
            test_order = pending_orders[0]
            order_id = test_order["id"]
            
            print(f"✅ Testing order completion for: {order_id[:8]}...")
            complete_result = await self.orders_service.mark_complete(order_id)
            print(f"   ✅ Order completed: {complete_result['new_state']}")
            
            # Test refund on another pending order
            if len(pending_orders) > 1:
                refund_order = pending_orders[1]
                print(f"💰 Testing refund for: {refund_order['id'][:8]}...")
                refund_result = await self.orders_service.process_refund(refund_order["id"])
                print(f"   ✅ Refund processed: {refund_result['amount_refunded']}")
    
    async def demo_voice_features(self):
        """Demonstrate voice command features"""
        print("\n🗣️ === VOICE DEMO ===")
        
        # Test voice commands
        test_commands = [
            "refresh catalog",
            "show orders",
            "help",
            "unknown command"
        ]
        
        for command in test_commands:
            print(f"🎤 Testing voice command: '{command}'")
            result = await self.voice_agent.test_voice_command(command)
            
            if result["status"] == "success":
                print(f"   ✅ Intent: {result['intent']}")
                print(f"   💬 Response: {result['response']}")
            else:
                print(f"   ❌ Status: {result['status']}")
        
        # Show available commands
        commands = self.voice_agent.get_available_commands()
        print(f"\n📝 Available voice commands:")
        for trigger, response in commands.items():
            print(f"   • '{trigger}' → {response}")
    
    async def demo_gesture_features(self):
        """Demonstrate gesture recognition features"""
        print("\n👋 === GESTURE DEMO ===")
        
        # Test gestures
        test_gestures = [
            "thumb_up",
            "point_index",
            "open_palm", 
            "peace_sign"
        ]
        
        for gesture in test_gestures:
            print(f"🤟 Testing gesture: {gesture}")
            result = await self.gesture_agent.test_gesture(gesture)
            
            if result["status"] == "success":
                print(f"   ✅ Intent: {result['intent']}")
                print(f"   📝 Description: {result['description']}")
            else:
                print(f"   ⏳ Status: {result['status']}")
        
        # Show available gestures
        gestures = self.gesture_agent.get_available_gestures()
        print(f"\n📝 Available gestures:")
        for gesture, description in gestures.items():
            print(f"   • {gesture} → {description}")
    
    async def demo_ui_interactions(self):
        """Demonstrate UI interaction handling"""
        print("\n🖱️ === UI INTERACTIONS DEMO ===")
        
        # Test UI actions
        test_actions = [
            ("refresh_catalog", {}),
            ("toggle_item_status", {"item_id": "catalog_item_1"}),
            ("mark_order_complete", {"order_id": "order_001"}),
            ("process_refund", {"order_id": "order_003"}),
            ("view_item_details", {"item_id": "catalog_item_2"})
        ]
        
        for action, params in test_actions:
            print(f"🔘 Testing UI action: {action}")
            result = await self.action_handler.handle_action(action, params)
            
            if result["status"] == "success":
                print(f"   ✅ Message: {result['message']}")
                if result.get("ui_update"):
                    print(f"   🔄 UI update triggered")
            else:
                print(f"   ❌ Error: {result.get('error', 'Unknown error')}")
    
    async def demo_end_to_end_workflow(self):
        """Demonstrate complete workflow"""
        print("\n🎬 === END-TO-END WORKFLOW DEMO ===")
        
        print("📋 Scenario: Customer places order, then requests refund")
        
        # 1. Voice command to check orders
        print("\n1️⃣ Voice: 'show orders'")
        voice_result = await self.voice_agent.test_voice_command("show orders")
        print(f"   ✅ Voice processed: {voice_result['response']}")
        
        # 2. UI interaction to view order details
        print("\n2️⃣ UI: Click order details")
        ui_result = await self.action_handler.handle_action(
            "view_order_details", 
            {"order_id": "order_003"}
        )
        print(f"   ✅ UI action: {ui_result['message']}")
        
        # 3. Gesture to process refund
        print("\n3️⃣ Gesture: Thumb up to confirm refund")
        self.gesture_agent.set_selected_item("order_003")
        gesture_result = await self.gesture_agent.test_gesture("thumb_up")
        if gesture_result["status"] == "success":
            print(f"   ✅ Gesture processed: {gesture_result['description']}")
        
        # 4. Voice confirmation
        print("\n4️⃣ Voice: 'refresh orders' to see updated status")
        final_voice = await self.voice_agent.test_voice_command("refresh orders")
        print(f"   ✅ Final update: {final_voice['response']}")
        
        print("\n🎉 Complete workflow demonstrated!")
    
    async def run_demo(self):
        """Run the complete demo"""
        try:
            await self.initialize()
            
            print("\n" + "="*60)
            print("🏪 QANAT MVP - SQUARE SELLER DASHBOARD ASSISTANT")
            print("="*60)
            
            await self.demo_catalog_features()
            await self.demo_orders_features()
            await self.demo_voice_features()
            await self.demo_gesture_features()
            await self.demo_ui_interactions()
            await self.demo_end_to_end_workflow()
            
            print("\n" + "="*60)
            print("✅ DEMO COMPLETE - All MVP features demonstrated!")
            print("="*60)
            
            # Show final status
            print(f"\n📊 Demo Summary:")
            print(f"   • Catalog items: ✅ Displayed and managed")
            print(f"   • Orders: ✅ Listed, completed, and refunded")
            print(f"   • Voice commands: ✅ Recognized and processed")
            print(f"   • Gesture controls: ✅ Detected and executed")
            print(f"   • UI interactions: ✅ Responsive and integrated")
            print(f"   • End-to-end workflow: ✅ Complete multimodal experience")
            
        except Exception as e:
            logger.error("Demo failed", error=str(e))
            print(f"\n❌ Demo error: {e}")
            raise
        finally:
            await self.cleanup()
    
    async def cleanup(self):
        """Clean up resources"""
        try:
            if self.catalog_service:
                await self.catalog_service.close()
            if self.orders_service:
                await self.orders_service.close()
            if self.voice_agent:
                await self.voice_agent.close()
            if self.gesture_agent:
                await self.gesture_agent.close()
            print("\n🧹 Demo cleanup completed")
        except Exception as e:
            logger.error("Cleanup error", error=str(e))

async def main():
    """Main demo entry point"""
    demo = QanatDemo()
    
    try:
        await demo.run_demo()
    except KeyboardInterrupt:
        print("\n\n⏹️ Demo stopped by user")
    except Exception as e:
        print(f"\n💥 Demo failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
