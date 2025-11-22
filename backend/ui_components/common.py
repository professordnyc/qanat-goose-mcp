"""
Common UI Components and Utilities
Shared functionality across dashboard components
"""

from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import structlog

logger = structlog.get_logger(__name__)

class UIActionHandler:
    """Handles UI actions and routes them to appropriate services"""
    
    def __init__(self, orchestrator=None):
        self.orchestrator = orchestrator
        self.action_handlers = {}
        self.ui_state = {}
        self.loading_states = {}
        
        # Register default action handlers
        self._register_default_handlers()
        
        logger.info("UIActionHandler initialized")
    
    def _register_default_handlers(self):
        """Register default UI action handlers"""
        
        # Button click handlers
        self.action_handlers.update({
            "refresh_catalog": self._handle_refresh_catalog,
            "toggle_item_status": self._handle_toggle_item_status,
            "view_item_details": self._handle_view_item_details,
            "refresh_orders": self._handle_refresh_orders,
            "mark_order_complete": self._handle_mark_order_complete,
            "process_refund": self._handle_process_refund,
            "view_order_details": self._handle_view_order_details,
            "close_modal": self._handle_close_modal,
            "search_catalog": self._handle_search_catalog,
            "filter_orders": self._handle_filter_orders
        })
    
    async def handle_action(
        self, 
        action: str, 
        params: Dict[str, Any],
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Handle a UI action"""
        try:
            logger.info("Handling UI action", action=action, params=params)
            
            # Set loading state
            self._set_loading_state(action, True)
            
            # Find and execute handler
            handler = self.action_handlers.get(action)
            if not handler:
                logger.warning("No handler found for action", action=action)
                result = {
                    "status": "error",
                    "error": f"No handler for action: {action}",
                    "action": action
                }
            else:
                result = await handler(params, context or {})
                result["action"] = action
            
            # Clear loading state
            self._set_loading_state(action, False)
            
            logger.info("UI action handled", action=action, status=result.get("status"))
            return result
            
        except Exception as e:
            self._set_loading_state(action, False)
            logger.error("Failed to handle UI action", action=action, error=str(e))
            return {
                "status": "error",
                "error": str(e),
                "action": action
            }
    
    # Action handlers
    async def _handle_refresh_catalog(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle catalog refresh"""
        if self.orchestrator:
            orchestrator_result = await self.orchestrator.process_intent(
                "catalog.refresh", params, "ui"
            )
            return {
                "status": "success",
                "message": "Catalog refreshed successfully",
                "ui_update": True,
                "orchestrator_result": orchestrator_result
            }
        
        return {
            "status": "success", 
            "message": "Catalog refresh requested",
            "ui_update": True
        }
    
    async def _handle_toggle_item_status(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle item status toggle"""
        item_id = params.get("item_id")
        if not item_id:
            return {"status": "error", "error": "Missing item_id"}
        
        if self.orchestrator:
            orchestrator_result = await self.orchestrator.process_intent(
                "catalog.toggle_status", params, "ui"
            )
            return {
                "status": "success",
                "message": f"Item status toggled for {item_id[:8]}...",
                "ui_update": True,
                "orchestrator_result": orchestrator_result
            }
        
        return {
            "status": "success",
            "message": f"Status toggle requested for item {item_id[:8]}...",
            "ui_update": True
        }
    
    async def _handle_view_item_details(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle view item details"""
        item_id = params.get("item_id")
        if not item_id:
            return {"status": "error", "error": "Missing item_id"}
        
        return {
            "status": "success",
            "message": f"Showing details for item {item_id[:8]}...",
            "ui_update": True,
            "modal": {
                "type": "item_details",
                "item_id": item_id
            }
        }
    
    async def _handle_refresh_orders(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle orders refresh"""
        if self.orchestrator:
            orchestrator_result = await self.orchestrator.process_intent(
                "orders.refresh", params, "ui"
            )
            return {
                "status": "success",
                "message": "Orders refreshed successfully",
                "ui_update": True,
                "orchestrator_result": orchestrator_result
            }
        
        return {
            "status": "success",
            "message": "Orders refresh requested", 
            "ui_update": True
        }
    
    async def _handle_mark_order_complete(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle mark order complete"""
        order_id = params.get("order_id")
        if not order_id:
            return {"status": "error", "error": "Missing order_id"}
        
        if self.orchestrator:
            orchestrator_result = await self.orchestrator.process_intent(
                "orders.complete", params, "ui"
            )
            return {
                "status": "success",
                "message": f"Order {order_id[:8]}... marked as complete",
                "ui_update": True,
                "orchestrator_result": orchestrator_result
            }
        
        return {
            "status": "success",
            "message": f"Order completion requested for {order_id[:8]}...",
            "ui_update": True
        }
    
    async def _handle_process_refund(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle process refund"""
        order_id = params.get("order_id")
        if not order_id:
            return {"status": "error", "error": "Missing order_id"}
        
        params.setdefault("reason", "Customer request")
        
        if self.orchestrator:
            orchestrator_result = await self.orchestrator.process_intent(
                "orders.refund", params, "ui"
            )
            return {
                "status": "success", 
                "message": f"Refund processed for order {order_id[:8]}...",
                "ui_update": True,
                "orchestrator_result": orchestrator_result
            }
        
        return {
            "status": "success",
            "message": f"Refund requested for order {order_id[:8]}...",
            "ui_update": True
        }
    
    async def _handle_view_order_details(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle view order details"""
        order_id = params.get("order_id")
        if not order_id:
            return {"status": "error", "error": "Missing order_id"}
        
        return {
            "status": "success",
            "message": f"Showing details for order {order_id[:8]}...",
            "ui_update": True,
            "modal": {
                "type": "order_details",
                "order_id": order_id
            }
        }
    
    async def _handle_close_modal(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle close modal"""
        return {
            "status": "success",
            "message": "Modal closed",
            "ui_update": True,
            "modal": {"action": "close"}
        }
    
    async def _handle_search_catalog(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle catalog search"""
        query = params.get("query", "")
        
        if self.orchestrator:
            orchestrator_result = await self.orchestrator.process_intent(
                "catalog.search", params, "ui"
            )
            return {
                "status": "success",
                "message": f"Searching catalog for: {query}",
                "ui_update": True,
                "orchestrator_result": orchestrator_result
            }
        
        return {
            "status": "success",
            "message": f"Catalog search requested: {query}",
            "ui_update": True
        }
    
    async def _handle_filter_orders(self, params: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle orders filter"""
        filter_type = params.get("filter", "all")
        
        return {
            "status": "success",
            "message": f"Filtering orders by: {filter_type}",
            "ui_update": True,
            "filter": {
                "type": "orders",
                "value": filter_type
            }
        }
    
    def _set_loading_state(self, action: str, is_loading: bool):
        """Set loading state for an action"""
        if is_loading:
            self.loading_states[action] = datetime.utcnow().isoformat()
        else:
            self.loading_states.pop(action, None)
    
    def get_loading_states(self) -> Dict[str, str]:
        """Get current loading states"""
        return self.loading_states.copy()
    
    def register_handler(self, action: str, handler: Callable):
        """Register a custom action handler"""
        self.action_handlers[action] = handler
        logger.info("Registered action handler", action=action)

class UIStateManager:
    """Manages UI state and updates"""
    
    def __init__(self):
        self.state = {
            "current_view": "catalog",
            "selected_items": [],
            "filters": {},
            "modals": [],
            "notifications": []
        }
        self.subscribers = []
        
        logger.info("UIStateManager initialized")
    
    def get_state(self) -> Dict[str, Any]:
        """Get current UI state"""
        return self.state.copy()
    
    def update_state(self, updates: Dict[str, Any]):
        """Update UI state"""
        try:
            self.state.update(updates)
            logger.info("UI state updated", updates=list(updates.keys()))
            
            # Notify subscribers
            for subscriber in self.subscribers:
                try:
                    subscriber(self.state)
                except Exception as e:
                    logger.error("Failed to notify subscriber", error=str(e))
        except Exception as e:
            logger.error("Failed to update UI state", error=str(e))
    
    def subscribe(self, callback: Callable):
        """Subscribe to state changes"""
        self.subscribers.append(callback)
        logger.info("New UI state subscriber added", total=len(self.subscribers))
    
    def add_notification(self, message: str, type: str = "info", duration: int = 5000):
        """Add a notification"""
        notification = {
            "id": f"notif_{datetime.utcnow().timestamp()}",
            "message": message,
            "type": type,
            "timestamp": datetime.utcnow().isoformat(),
            "duration": duration
        }
        
        self.state["notifications"].append(notification)
        logger.info("Notification added", message=message, type=type)
    
    def clear_notifications(self):
        """Clear all notifications"""
        self.state["notifications"] = []
        logger.info("Notifications cleared")

def create_loading_component(message: str = "Loading...") -> Dict[str, Any]:
    """Create a loading component"""
    return {
        "type": "loading",
        "message": message,
        "spinner": True,
        "timestamp": datetime.utcnow().isoformat()
    }

def create_error_component(error: str, retry_action: str = None) -> Dict[str, Any]:
    """Create an error component"""
    component = {
        "type": "error",
        "message": error,
        "timestamp": datetime.utcnow().isoformat(),
        "style": "error"
    }
    
    if retry_action:
        component["actions"] = [{
            "label": "Retry",
            "action": retry_action,
            "style": "primary"
        }]
    
    return component

def create_success_component(message: str) -> Dict[str, Any]:
    """Create a success component"""
    return {
        "type": "success",
        "message": message,
        "timestamp": datetime.utcnow().isoformat(),
        "style": "success",
        "auto_dismiss": 3000
    }

# Global instances
_action_handler = None
_state_manager = None

def get_action_handler(orchestrator=None) -> UIActionHandler:
    """Get global action handler instance"""
    global _action_handler
    if _action_handler is None:
        _action_handler = UIActionHandler(orchestrator)
    return _action_handler

def get_state_manager() -> UIStateManager:
    """Get global state manager instance"""
    global _state_manager
    if _state_manager is None:
        _state_manager = UIStateManager()
    return _state_manager

# Utility function for testing
async def test_ui_components():
    """Test UI components"""
    from ..agents.orchestrator import IntentOrchestrator
    
    orchestrator = IntentOrchestrator()
    handler = get_action_handler(orchestrator)
    state_manager = get_state_manager()
    
    # Test action handling
    result = await handler.handle_action(
        "refresh_catalog", 
        {}, 
        {"user": "test"}
    )
    print(f"Action result: {result}")
    
    # Test state management
    state_manager.update_state({"current_view": "orders"})
    state_manager.add_notification("Test notification", "info")
    
    current_state = state_manager.get_state()
    print(f"UI State: {current_state}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_ui_components())
