"""
Orders Dashboard UI Components
MCP-UI components for Square orders management
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import structlog

logger = structlog.get_logger(__name__)

class OrdersDashboard:
    """Orders dashboard UI component renderer"""
    
    def __init__(self):
        self.component_id = "orders_dashboard"
        
    def render_table(self, orders: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Render orders table for MCP-UI"""
        try:
            table_data = []
            
            for order in orders:
                # Extract order data
                order_id = order.get("id", "unknown")
                short_id = order_id[:8] + "..." if len(order_id) > 8 else order_id
                state = order.get("state", "UNKNOWN")
                total_amount = order.get("total_money", {}).get("amount", 0)
                total_display = f"${total_amount / 100:.2f}"
                
                # Extract customer info
                fulfillments = order.get("fulfillments", [])
                customer_name = "Guest"
                if fulfillments:
                    pickup_details = fulfillments[0].get("pickup_details", {})
                    recipient = pickup_details.get("recipient", {})
                    customer_name = recipient.get("display_name", "Guest")
                
                # Extract items summary
                line_items = order.get("line_items", [])
                items_summary = ", ".join([
                    f"{item.get('name', 'Unknown')} x{item.get('quantity', '1')}"
                    for item in line_items
                ])
                
                # Create status badge
                status_colors = {
                    "OPEN": {"color": "yellow", "background": "#fff3cd", "text": "Pending"},
                    "COMPLETED": {"color": "green", "background": "#d4edda", "text": "Completed"},
                    "CANCELED": {"color": "red", "background": "#f8d7da", "text": "Refunded"},
                    "UNKNOWN": {"color": "gray", "background": "#f8f9fa", "text": "Unknown"}
                }
                
                status_badge = status_colors.get(state, status_colors["UNKNOWN"])
                
                # Create action buttons based on order state
                actions = []
                
                if state == "OPEN":
                    actions.extend([
                        {
                            "type": "button",
                            "label": "Complete",
                            "action": "mark_order_complete",
                            "params": {"order_id": order_id},
                            "style": "success",
                            "icon": "check"
                        },
                        {
                            "type": "button", 
                            "label": "Refund",
                            "action": "process_refund",
                            "params": {"order_id": order_id},
                            "style": "warning",
                            "icon": "refund"
                        }
                    ])
                
                actions.append({
                    "type": "button",
                    "label": "Details",
                    "action": "view_order_details",
                    "params": {"order_id": order_id},
                    "style": "primary",
                    "icon": "info"
                })
                
                # Format created time
                created_at = order.get("created_at", "")
                if created_at:
                    try:
                        created_dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        time_display = created_dt.strftime("%m/%d %I:%M %p")
                    except:
                        time_display = "Unknown"
                else:
                    time_display = "Unknown"
                
                table_data.append({
                    "id": order_id,
                    "order_id": short_id,
                    "customer": customer_name,
                    "items": items_summary,
                    "total": total_display,
                    "status": status_badge,
                    "created": time_display,
                    "actions": actions,
                    "_raw_order": order  # Keep original data
                })
            
            table_component = {
                "type": "table",
                "id": "orders_table",
                "title": "Recent Orders",
                "columns": [
                    {
                        "key": "order_id",
                        "label": "Order ID",
                        "sortable": True,
                        "width": "15%"
                    },
                    {
                        "key": "customer",
                        "label": "Customer",
                        "sortable": True,
                        "width": "20%"
                    },
                    {
                        "key": "items",
                        "label": "Items",
                        "width": "25%"
                    },
                    {
                        "key": "total",
                        "label": "Total",
                        "sortable": True,
                        "align": "right",
                        "width": "10%"
                    },
                    {
                        "key": "status",
                        "label": "Status",
                        "type": "badge",
                        "width": "15%"
                    },
                    {
                        "key": "actions",
                        "label": "Actions",
                        "type": "button_group",
                        "width": "15%"
                    }
                ],
                "data": table_data,
                "clickable_rows": True,
                "row_click_action": "view_order_details",
                "pagination": {
                    "enabled": True,
                    "page_size": 10
                },
                "filters": [
                    {
                        "key": "status",
                        "label": "Status",
                        "options": ["All", "Pending", "Completed", "Refunded"]
                    }
                ],
                "sort": {
                    "default_column": "created",
                    "default_direction": "desc"
                }
            }
            
            logger.info("Orders table rendered", orders_count=len(table_data))
            return table_component
            
        except Exception as e:
            logger.error("Failed to render orders table", error=str(e))
            raise
    
    def render_toolbar(self) -> Dict[str, Any]:
        """Render orders toolbar with action buttons"""
        toolbar = {
            "type": "toolbar",
            "id": "orders_toolbar",
            "buttons": [
                {
                    "label": "Refresh",
                    "action": "refresh_orders",
                    "style": "primary",
                    "icon": "refresh",
                    "hotkey": "Ctrl+R"
                },
                {
                    "label": "Today's Orders",
                    "action": "filter_today_orders",
                    "style": "secondary",
                    "icon": "calendar"
                },
                {
                    "label": "Export",
                    "action": "export_orders",
                    "style": "outline",
                    "icon": "download"
                }
            ],
            "date_range": {
                "enabled": True,
                "action": "filter_orders_by_date"
            }
        }
        
        return toolbar
    
    def render_order_details_modal(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Render order details modal"""
        try:
            order_id = order.get("id", "unknown")
            state = order.get("state", "UNKNOWN")
            total_amount = order.get("total_money", {}).get("amount", 0)
            total_display = f"${total_amount / 100:.2f}"
            
            # Extract customer info
            fulfillments = order.get("fulfillments", [])
            customer_info = {"name": "Guest", "email": "N/A", "phone": "N/A"}
            if fulfillments:
                pickup_details = fulfillments[0].get("pickup_details", {})
                recipient = pickup_details.get("recipient", {})
                customer_info["name"] = recipient.get("display_name", "Guest")
                customer_info["email"] = recipient.get("email_address", "N/A")
                customer_info["phone"] = recipient.get("phone_number", "N/A")
            
            # Extract line items
            line_items = order.get("line_items", [])
            items_list = []
            for item in line_items:
                items_list.append({
                    "name": item.get("name", "Unknown Item"),
                    "quantity": item.get("quantity", "1"),
                    "price": f"${item.get('base_price_money', {}).get('amount', 0) / 100:.2f}",
                    "total": f"${item.get('total_money', {}).get('amount', 0) / 100:.2f}"
                })
            
            # Format timestamps
            created_at = order.get("created_at", "")
            updated_at = order.get("updated_at", "")
            
            try:
                created_display = datetime.fromisoformat(created_at.replace('Z', '+00:00')).strftime("%B %d, %Y at %I:%M %p")
                updated_display = datetime.fromisoformat(updated_at.replace('Z', '+00:00')).strftime("%B %d, %Y at %I:%M %p")
            except:
                created_display = created_at
                updated_display = updated_at
            
            modal = {
                "type": "modal",
                "id": f"order_details_{order_id}",
                "title": f"Order Details: {order_id[:12]}...",
                "size": "large",
                "content": [
                    {
                        "type": "section",
                        "title": "Order Information",
                        "content": [
                            {
                                "type": "info_grid",
                                "items": [
                                    {"label": "Order ID", "value": order_id},
                                    {"label": "Status", "value": state.title()},
                                    {"label": "Total Amount", "value": total_display},
                                    {"label": "Created", "value": created_display},
                                    {"label": "Last Updated", "value": updated_display}
                                ]
                            }
                        ]
                    },
                    {
                        "type": "section",
                        "title": "Customer Information",
                        "content": [
                            {
                                "type": "info_grid",
                                "items": [
                                    {"label": "Name", "value": customer_info["name"]},
                                    {"label": "Email", "value": customer_info["email"]},
                                    {"label": "Phone", "value": customer_info["phone"]}
                                ]
                            }
                        ]
                    },
                    {
                        "type": "section",
                        "title": "Order Items",
                        "content": [
                            {
                                "type": "items_table",
                                "columns": ["Item", "Quantity", "Price", "Total"],
                                "data": items_list
                            }
                        ]
                    }
                ],
                "actions": []
            }
            
            # Add action buttons based on order state
            if state == "OPEN":
                modal["actions"].extend([
                    {
                        "label": "Mark Complete",
                        "action": "mark_order_complete",
                        "params": {"order_id": order_id},
                        "style": "success"
                    },
                    {
                        "label": "Process Refund",
                        "action": "process_refund", 
                        "params": {"order_id": order_id},
                        "style": "warning"
                    }
                ])
            
            modal["actions"].append({
                "label": "Close",
                "action": "close_modal",
                "style": "secondary"
            })
            
            logger.info("Order details modal rendered", order_id=order_id, state=state)
            return modal
            
        except Exception as e:
            logger.error("Failed to render order details modal", error=str(e))
            raise
    
    def render_dashboard(self, orders: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Render complete orders dashboard"""
        try:
            # Calculate statistics
            total_orders = len(orders)
            pending_orders = len([order for order in orders if order.get("state") == "OPEN"])
            completed_orders = len([order for order in orders if order.get("state") == "COMPLETED"])
            total_revenue = sum(
                order.get("total_money", {}).get("amount", 0) 
                for order in orders 
                if order.get("state") == "COMPLETED"
            ) / 100
            
            dashboard = {
                "type": "dashboard",
                "id": self.component_id,
                "title": "Square Orders Management",
                "description": "View and manage your Square orders",
                "layout": "vertical",
                "components": [
                    self.render_toolbar(),
                    {
                        "type": "stats_row",
                        "stats": [
                            {
                                "label": "Total Orders",
                                "value": total_orders,
                                "icon": "receipt"
                            },
                            {
                                "label": "Pending",
                                "value": pending_orders,
                                "icon": "clock",
                                "color": "yellow"
                            },
                            {
                                "label": "Completed",
                                "value": completed_orders,
                                "icon": "check_circle",
                                "color": "green"
                            },
                            {
                                "label": "Revenue",
                                "value": f"${total_revenue:.2f}",
                                "icon": "dollar_sign",
                                "color": "blue"
                            }
                        ]
                    },
                    self.render_table(orders)
                ],
                "refresh_interval": 15000,  # 15 seconds
                "last_updated": datetime.utcnow().isoformat()
            }
            
            logger.info("Orders dashboard rendered",
                       total_orders=total_orders,
                       pending_orders=pending_orders,
                       completed_orders=completed_orders,
                       total_revenue=total_revenue)
            
            return dashboard
            
        except Exception as e:
            logger.error("Failed to render orders dashboard", error=str(e))
            raise
    
    def handle_action(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle UI actions from the orders dashboard"""
        try:
            logger.info("Handling orders dashboard action", action=action, params=params)
            
            if action == "refresh_orders":
                return {"action": "refresh", "target": "orders"}
            
            elif action == "mark_order_complete":
                order_id = params.get("order_id")
                if not order_id:
                    raise ValueError("Missing order_id parameter")
                
                return {
                    "action": "mark_complete",
                    "target": "order",
                    "order_id": order_id
                }
            
            elif action == "process_refund":
                order_id = params.get("order_id")
                if not order_id:
                    raise ValueError("Missing order_id parameter")
                
                return {
                    "action": "process_refund",
                    "target": "order",
                    "order_id": order_id,
                    "reason": "Customer request"
                }
            
            elif action == "view_order_details":
                order_id = params.get("order_id")
                if not order_id:
                    raise ValueError("Missing order_id parameter")
                
                return {
                    "action": "show_modal",
                    "target": "order_details",
                    "order_id": order_id
                }
            
            elif action == "filter_today_orders":
                today = datetime.utcnow().strftime("%Y-%m-%d")
                return {
                    "action": "filter",
                    "target": "orders",
                    "created_after": f"{today}T00:00:00Z"
                }
            
            else:
                logger.warning("Unknown orders action", action=action)
                return {"action": "unknown", "error": f"Unknown action: {action}"}
                
        except Exception as e:
            logger.error("Failed to handle orders action", action=action, error=str(e))
            raise

# Utility functions for testing
def create_sample_orders_data() -> List[Dict[str, Any]]:
    """Create sample orders data for testing"""
    from datetime import timedelta
    
    base_time = datetime.utcnow()
    
    return [
        {
            "id": "order_001",
            "state": "OPEN",
            "created_at": (base_time - timedelta(hours=2)).isoformat(),
            "updated_at": (base_time - timedelta(hours=2)).isoformat(),
            "line_items": [
                {
                    "name": "Coffee",
                    "quantity": "1",
                    "base_price_money": {"amount": 300, "currency": "USD"},
                    "total_money": {"amount": 300, "currency": "USD"}
                },
                {
                    "name": "Muffin",
                    "quantity": "1", 
                    "base_price_money": {"amount": 250, "currency": "USD"},
                    "total_money": {"amount": 250, "currency": "USD"}
                }
            ],
            "total_money": {"amount": 550, "currency": "USD"},
            "fulfillments": [{
                "pickup_details": {
                    "recipient": {"display_name": "John Doe"}
                }
            }]
        },
        {
            "id": "order_002",
            "state": "COMPLETED",
            "created_at": (base_time - timedelta(hours=4)).isoformat(),
            "updated_at": (base_time - timedelta(hours=3)).isoformat(),
            "line_items": [
                {
                    "name": "Sandwich",
                    "quantity": "1",
                    "base_price_money": {"amount": 750, "currency": "USD"},
                    "total_money": {"amount": 750, "currency": "USD"}
                }
            ],
            "total_money": {"amount": 750, "currency": "USD"},
            "fulfillments": [{
                "pickup_details": {
                    "recipient": {"display_name": "Jane Smith"}
                }
            }]
        },
        {
            "id": "order_003",
            "state": "OPEN",
            "created_at": (base_time - timedelta(minutes=30)).isoformat(),
            "updated_at": (base_time - timedelta(minutes=30)).isoformat(),
            "line_items": [
                {
                    "name": "Soup",
                    "quantity": "1",
                    "base_price_money": {"amount": 500, "currency": "USD"},
                    "total_money": {"amount": 500, "currency": "USD"}
                }
            ],
            "total_money": {"amount": 500, "currency": "USD"},
            "fulfillments": [{
                "pickup_details": {
                    "recipient": {"display_name": "Bob Wilson"}
                }
            }]
        }
    ]

def test_orders_dashboard():
    """Test the orders dashboard rendering"""
    dashboard = OrdersDashboard()
    sample_data = create_sample_orders_data()
    
    # Test dashboard rendering
    result = dashboard.render_dashboard(sample_data)
    print(f"Orders dashboard rendered with {len(sample_data)} orders")
    
    # Test action handling
    action_result = dashboard.handle_action("mark_order_complete", {"order_id": "order_001"})
    print(f"Action result: {action_result}")

if __name__ == "__main__":
    test_orders_dashboard()
