"""
Catalog Dashboard UI Components
MCP-UI components for Square catalog management
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import structlog

logger = structlog.get_logger(__name__)

class CatalogDashboard:
    """Catalog dashboard UI component renderer"""
    
    def __init__(self):
        self.component_id = "catalog_dashboard"
        
    def render_table(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Render catalog items table for MCP-UI"""
        try:
            table_data = []
            
            for item in items:
                # Extract item data
                item_id = item.get("id", "unknown")
                name = item.get("name", "Unknown Item")
                price_amount = item.get("base_price_money", {}).get("amount", 0)
                price_display = f"${price_amount / 100:.2f}"
                is_active = item.get("present_at_all_locations", True)
                
                # Determine stock status
                if is_active:
                    stock_status = {
                        "text": "In Stock",
                        "color": "green",
                        "background": "#e8f5e8"
                    }
                else:
                    stock_status = {
                        "text": "Low Stock", 
                        "color": "orange",
                        "background": "#fff3cd"
                    }
                
                # Create action buttons
                actions = [
                    {
                        "type": "button",
                        "label": "Activate" if not is_active else "Deactivate",
                        "action": "toggle_item_status",
                        "params": {"item_id": item_id},
                        "style": "secondary",
                        "icon": "toggle"
                    },
                    {
                        "type": "button",
                        "label": "Details",
                        "action": "view_item_details", 
                        "params": {"item_id": item_id},
                        "style": "primary",
                        "icon": "info"
                    }
                ]
                
                table_data.append({
                    "id": item_id,
                    "name": name,
                    "price": price_display,
                    "status": stock_status,
                    "actions": actions,
                    "_raw_item": item  # Keep original data for reference
                })
            
            table_component = {
                "type": "table",
                "id": "catalog_items_table",
                "title": "Catalog Items",
                "columns": [
                    {
                        "key": "name",
                        "label": "Item Name",
                        "sortable": True,
                        "width": "35%"
                    },
                    {
                        "key": "price", 
                        "label": "Price",
                        "sortable": True,
                        "align": "right",
                        "width": "15%"
                    },
                    {
                        "key": "status",
                        "label": "Stock Status",
                        "type": "badge", 
                        "width": "25%"
                    },
                    {
                        "key": "actions",
                        "label": "Actions",
                        "type": "button_group",
                        "width": "25%"
                    }
                ],
                "data": table_data,
                "clickable_rows": True,
                "row_click_action": "view_item_details",
                "pagination": {
                    "enabled": True,
                    "page_size": 10
                },
                "filters": [
                    {
                        "key": "status",
                        "label": "Stock Status",
                        "options": ["All", "In Stock", "Low Stock"]
                    }
                ]
            }
            
            logger.info("Catalog table rendered", items_count=len(table_data))
            return table_component
            
        except Exception as e:
            logger.error("Failed to render catalog table", error=str(e))
            raise
    
    def render_toolbar(self) -> Dict[str, Any]:
        """Render catalog toolbar with action buttons"""
        toolbar = {
            "type": "toolbar",
            "id": "catalog_toolbar",
            "buttons": [
                {
                    "label": "Refresh",
                    "action": "refresh_catalog",
                    "style": "primary",
                    "icon": "refresh",
                    "hotkey": "Ctrl+R"
                },
                {
                    "label": "Add Item",
                    "action": "add_catalog_item",
                    "style": "secondary", 
                    "icon": "plus"
                },
                {
                    "label": "Export",
                    "action": "export_catalog",
                    "style": "outline",
                    "icon": "download"
                }
            ],
            "search": {
                "enabled": True,
                "placeholder": "Search items...",
                "action": "search_catalog"
            }
        }
        
        return toolbar
    
    def render_item_details_modal(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Render item details modal"""
        try:
            item_id = item.get("id", "unknown")
            name = item.get("name", "Unknown Item")
            price_amount = item.get("base_price_money", {}).get("amount", 0)
            price_display = f"${price_amount / 100:.2f}"
            description = item.get("description", "No description available")
            category_id = item.get("category_id", "uncategorized")
            is_active = item.get("present_at_all_locations", True)
            
            modal = {
                "type": "modal",
                "id": f"item_details_{item_id}",
                "title": f"Item Details: {name}",
                "size": "medium",
                "content": [
                    {
                        "type": "form",
                        "id": "item_details_form",
                        "fields": [
                            {
                                "type": "text",
                                "label": "Item Name",
                                "value": name,
                                "readonly": True
                            },
                            {
                                "type": "currency",
                                "label": "Price",
                                "value": price_display,
                                "readonly": True
                            },
                            {
                                "type": "textarea",
                                "label": "Description",
                                "value": description,
                                "readonly": True,
                                "rows": 3
                            },
                            {
                                "type": "select",
                                "label": "Category", 
                                "value": category_id,
                                "readonly": True,
                                "options": [
                                    {"value": "beverages", "label": "Beverages"},
                                    {"value": "food", "label": "Food"},
                                    {"value": "pastries", "label": "Pastries"},
                                    {"value": "uncategorized", "label": "Uncategorized"}
                                ]
                            },
                            {
                                "type": "toggle",
                                "label": "Active Status",
                                "value": is_active,
                                "action": "toggle_item_status",
                                "params": {"item_id": item_id}
                            }
                        ]
                    }
                ],
                "actions": [
                    {
                        "label": "Edit Item",
                        "action": "edit_catalog_item",
                        "params": {"item_id": item_id},
                        "style": "primary"
                    },
                    {
                        "label": "Close",
                        "action": "close_modal",
                        "style": "secondary"
                    }
                ]
            }
            
            logger.info("Item details modal rendered", item_id=item_id, name=name)
            return modal
            
        except Exception as e:
            logger.error("Failed to render item details modal", error=str(e))
            raise
    
    def render_dashboard(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Render complete catalog dashboard"""
        try:
            dashboard = {
                "type": "dashboard",
                "id": self.component_id,
                "title": "Square Catalog Management",
                "description": "View and manage your Square catalog items",
                "layout": "vertical",
                "components": [
                    self.render_toolbar(),
                    {
                        "type": "stats_row",
                        "stats": [
                            {
                                "label": "Total Items",
                                "value": len(items),
                                "icon": "package"
                            },
                            {
                                "label": "Active Items",
                                "value": len([item for item in items if item.get("present_at_all_locations", True)]),
                                "icon": "check_circle",
                                "color": "green"
                            },
                            {
                                "label": "Low Stock", 
                                "value": len([item for item in items if not item.get("present_at_all_locations", True)]),
                                "icon": "warning",
                                "color": "orange"
                            },
                            {
                                "label": "Total Value",
                                "value": f"${sum(item.get('base_price_money', {}).get('amount', 0) for item in items) / 100:.2f}",
                                "icon": "dollar_sign"
                            }
                        ]
                    },
                    self.render_table(items)
                ],
                "refresh_interval": 30000,  # 30 seconds
                "last_updated": datetime.utcnow().isoformat()
            }
            
            logger.info("Catalog dashboard rendered", 
                       total_items=len(items),
                       active_items=len([item for item in items if item.get("present_at_all_locations", True)]))
            
            return dashboard
            
        except Exception as e:
            logger.error("Failed to render catalog dashboard", error=str(e))
            raise
    
    def handle_action(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle UI actions from the dashboard"""
        try:
            logger.info("Handling catalog dashboard action", action=action, params=params)
            
            if action == "refresh_catalog":
                return {"action": "refresh", "target": "catalog"}
            
            elif action == "toggle_item_status":
                item_id = params.get("item_id")
                if not item_id:
                    raise ValueError("Missing item_id parameter")
                
                return {
                    "action": "toggle_status",
                    "target": "catalog_item",
                    "item_id": item_id
                }
            
            elif action == "view_item_details":
                item_id = params.get("item_id")
                if not item_id:
                    raise ValueError("Missing item_id parameter")
                
                return {
                    "action": "show_modal",
                    "target": "item_details",
                    "item_id": item_id
                }
            
            elif action == "search_catalog":
                query = params.get("query", "")
                return {
                    "action": "search",
                    "target": "catalog",
                    "query": query
                }
            
            else:
                logger.warning("Unknown catalog action", action=action)
                return {"action": "unknown", "error": f"Unknown action: {action}"}
                
        except Exception as e:
            logger.error("Failed to handle catalog action", action=action, error=str(e))
            raise

# Utility functions for testing
def create_sample_catalog_data() -> List[Dict[str, Any]]:
    """Create sample catalog data for testing"""
    return [
        {
            "id": "catalog_item_1",
            "name": "Coffee",
            "base_price_money": {"amount": 300, "currency": "USD"},
            "present_at_all_locations": True,
            "category_id": "beverages",
            "description": "Freshly brewed coffee"
        },
        {
            "id": "catalog_item_2",
            "name": "Sandwich", 
            "base_price_money": {"amount": 750, "currency": "USD"},
            "present_at_all_locations": True,
            "category_id": "food",
            "description": "Artisan sandwich"
        },
        {
            "id": "catalog_item_3",
            "name": "Soup",
            "base_price_money": {"amount": 500, "currency": "USD"},
            "present_at_all_locations": False,
            "category_id": "food",
            "description": "Soup of the day"
        },
        {
            "id": "catalog_item_4",
            "name": "Muffin",
            "base_price_money": {"amount": 250, "currency": "USD"},
            "present_at_all_locations": True,
            "category_id": "pastries", 
            "description": "Fresh baked muffin"
        }
    ]

def test_catalog_dashboard():
    """Test the catalog dashboard rendering"""
    dashboard = CatalogDashboard()
    sample_data = create_sample_catalog_data()
    
    # Test dashboard rendering
    result = dashboard.render_dashboard(sample_data)
    print(f"Dashboard rendered with {len(sample_data)} items")
    
    # Test action handling
    action_result = dashboard.handle_action("toggle_item_status", {"item_id": "catalog_item_1"})
    print(f"Action result: {action_result}")

if __name__ == "__main__":
    test_catalog_dashboard()
