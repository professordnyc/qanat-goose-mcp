"""
Intent Orchestrator
Routes voice, gesture, and UI intents to appropriate services
"""

import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime
import structlog

logger = structlog.get_logger(__name__)

class IntentOrchestrator:
    """Orchestrates intents from voice, gesture, and UI interactions"""
    
    def __init__(self):
        self.intent_handlers = {}
        self.active_intents = {}
        self.intent_history = []
        
        # Register default intent handlers
        self._register_default_handlers()
        
        logger.info("IntentOrchestrator initialized")
    
    def _register_default_handlers(self):
        """Register default intent handlers"""
        
        # Catalog intents
        self.intent_handlers.update({
            "catalog.refresh": self._handle_catalog_refresh,
            "catalog.toggle_status": self._handle_catalog_toggle,
            "catalog.view_details": self._handle_catalog_details,
            "catalog.search": self._handle_catalog_search
        })
        
        # Order intents  
        self.intent_handlers.update({
            "orders.view": self._handle_orders_view,
            "orders.refresh": self._handle_orders_refresh,
            "orders.complete": self._handle_order_complete,
            "orders.refund": self._handle_order_refund,
            "orders.details": self._handle_order_details
        })
        
        # UI intents
        self.intent_handlers.update({
            "ui.select": self._handle_ui_select,
            "ui.refresh": self._handle_ui_refresh,
            "ui.navigate": self._handle_ui_navigate
        })
        
        # System intents
        self.intent_handlers.update({
            "system.help": self._handle_system_help,
            "system.status": self._handle_system_status
        })
    
    async def process_intent(
        self,
        intent: str,
        params: Dict[str, Any],
        source: str = "unknown"
    ) -> Dict[str, Any]:
        """Process an intent and route to appropriate handler"""
        try:
            logger.info("Processing intent", intent=intent, params=params, source=source)
            
            # Record intent
            intent_record = {
                "intent": intent,
                "params": params,
                "source": source,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "processing"
            }
            
            intent_id = f"{intent}_{datetime.utcnow().timestamp()}"
            self.active_intents[intent_id] = intent_record
            
            # Find and execute handler
            handler = self.intent_handlers.get(intent)
            if not handler:
                logger.warning("No handler found for intent", intent=intent)
                result = {
                    "status": "error",
                    "error": f"No handler for intent: {intent}",
                    "intent": intent
                }
            else:
                result = await handler(params)
                result["intent"] = intent
                result["source"] = source
            
            # Update intent record
            intent_record["status"] = result.get("status", "completed")
            intent_record["result"] = result
            
            # Move to history
            self.intent_history.append(intent_record)
            del self.active_intents[intent_id]
            
            # Keep history size manageable
            if len(self.intent_history) > 100:
                self.intent_history = self.intent_history[-50:]
            
            logger.info("Intent processed", intent=intent, status=result.get("status"))
            return result
            
        except Exception as e:
            logger.error("Failed to process intent", intent=intent, error=str(e))
            return {
                "status": "error", 
                "error": str(e),
                "intent": intent
            }
    
    # Catalog handlers
    async def _handle_catalog_refresh(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle catalog refresh intent"""
        return {
            "status": "success",
            "action": "refresh_catalog",
            "message": "Refreshing catalog items...",
            "ui_update": True
        }
    
    async def _handle_catalog_toggle(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle catalog item status toggle"""
        item_id = params.get("item_id")
        if not item_id:
            return {"status": "error", "error": "Missing item_id"}
        
        return {
            "status": "success",
            "action": "toggle_item_status",
            "item_id": item_id,
            "message": f"Toggling status for item {item_id}",
            "ui_update": True
        }
    
    async def _handle_catalog_details(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle view catalog item details"""
        item_id = params.get("item_id")
        if not item_id:
            return {"status": "error", "error": "Missing item_id"}
        
        return {
            "status": "success",
            "action": "show_item_details",
            "item_id": item_id,
            "message": f"Showing details for item {item_id}",
            "ui_update": True
        }
    
    async def _handle_catalog_search(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle catalog search"""
        query = params.get("query", "")
        return {
            "status": "success",
            "action": "search_catalog",
            "query": query,
            "message": f"Searching catalog for: {query}",
            "ui_update": True
        }
    
    # Order handlers
    async def _handle_orders_view(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle view orders intent"""
        return {
            "status": "success",
            "action": "show_orders_dashboard", 
            "message": "Loading recent orders...",
            "ui_update": True
        }
    
    async def _handle_orders_refresh(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle orders refresh intent"""
        return {
            "status": "success",
            "action": "refresh_orders",
            "message": "Refreshing orders...",
            "ui_update": True
        }
    
    async def _handle_order_complete(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle mark order complete"""
        order_id = params.get("order_id")
        if not order_id:
            return {"status": "error", "error": "Missing order_id"}
        
        return {
            "status": "success",
            "action": "mark_order_complete",
            "order_id": order_id,
            "message": f"Marking order {order_id[:8]}... as complete",
            "ui_update": True
        }
    
    async def _handle_order_refund(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle process order refund"""
        order_id = params.get("order_id")
        reason = params.get("reason", "Customer request")
        
        if not order_id:
            return {"status": "error", "error": "Missing order_id"}
        
        return {
            "status": "success",
            "action": "process_order_refund",
            "order_id": order_id,
            "reason": reason,
            "message": f"Processing refund for order {order_id[:8]}...",
            "ui_update": True
        }
    
    async def _handle_order_details(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle view order details"""
        order_id = params.get("order_id")
        if not order_id:
            return {"status": "error", "error": "Missing order_id"}
        
        return {
            "status": "success",
            "action": "show_order_details",
            "order_id": order_id,
            "message": f"Showing details for order {order_id[:8]}...",
            "ui_update": True
        }
    
    # UI handlers
    async def _handle_ui_select(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle UI element selection"""
        element_id = params.get("element_id")
        element_type = params.get("element_type", "unknown")
        
        return {
            "status": "success",
            "action": "ui_select",
            "element_id": element_id,
            "element_type": element_type,
            "message": f"Selected {element_type}: {element_id}",
            "ui_update": True
        }
    
    async def _handle_ui_refresh(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle UI refresh"""
        target = params.get("target", "current_view")
        
        return {
            "status": "success",
            "action": "refresh_ui",
            "target": target,
            "message": f"Refreshing {target}...",
            "ui_update": True
        }
    
    async def _handle_ui_navigate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle UI navigation"""
        target = params.get("target", "dashboard")
        
        return {
            "status": "success", 
            "action": "navigate",
            "target": target,
            "message": f"Navigating to {target}...",
            "ui_update": True
        }
    
    # System handlers
    async def _handle_system_help(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle help request"""
        available_commands = [
            "refresh catalog - Update catalog items",
            "show orders - Display recent orders", 
            "toggle item status - Activate/deactivate items",
            "complete order - Mark order as complete",
            "refund order - Process order refund"
        ]
        
        return {
            "status": "success",
            "action": "show_help",
            "message": "Available commands:",
            "data": available_commands,
            "ui_update": False
        }
    
    async def _handle_system_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle system status request"""
        return {
            "status": "success",
            "action": "system_status",
            "message": "Qanat system is running",
            "data": {
                "active_intents": len(self.active_intents),
                "processed_intents": len(self.intent_history),
                "available_handlers": len(self.intent_handlers)
            },
            "ui_update": False
        }
    
    def get_intent_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent intent history"""
        return self.intent_history[-limit:]
    
    def get_active_intents(self) -> Dict[str, Dict[str, Any]]:
        """Get currently active intents"""
        return self.active_intents.copy()
    
    def register_handler(self, intent: str, handler) -> None:
        """Register a new intent handler"""
        self.intent_handlers[intent] = handler
        logger.info("Registered intent handler", intent=intent)
    
    def unregister_handler(self, intent: str) -> None:
        """Unregister an intent handler"""
        if intent in self.intent_handlers:
            del self.intent_handlers[intent]
            logger.info("Unregistered intent handler", intent=intent)

# Utility function for testing
async def test_orchestrator():
    """Test the intent orchestrator"""
    orchestrator = IntentOrchestrator()
    
    # Test catalog refresh
    result = await orchestrator.process_intent(
        "catalog.refresh", 
        {}, 
        "test"
    )
    print(f"Catalog refresh: {result}")
    
    # Test order completion
    result = await orchestrator.process_intent(
        "orders.complete",
        {"order_id": "test_order_123"},
        "test"
    )
    print(f"Order complete: {result}")
    
    # Test help
    result = await orchestrator.process_intent(
        "system.help",
        {},
        "test"
    )
    print(f"Help: {result}")
    
    # Show history
    history = orchestrator.get_intent_history()
    print(f"Intent history: {len(history)} items")

if __name__ == "__main__":
    asyncio.run(test_orchestrator())
