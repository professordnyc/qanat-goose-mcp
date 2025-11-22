"""
Qanat MCP-UI Server
Main MCP server for Goose Desktop integration
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime

import structlog
from mcp import McpServer, Tool, Resource
from mcp.server import NotificationOptions, ServerCapabilities
from mcp.types import (
    CallToolRequest, CallToolResult, 
    ListToolsRequest, ListToolsResult,
    ListResourcesRequest, ListResourcesResult,
    ReadResourceRequest, ReadResourceResult,
    TextContent, EmbeddedResource
)

# Import our services
from ..services.catalog_service import CatalogService
from ..services.orders_service import OrdersService
from ..agents.orchestrator import IntentOrchestrator
from ...config.environments.env_loader import get_config

logger = structlog.get_logger(__name__)

@dataclass
class QanatServer:
    """Main Qanat MCP-UI Server"""
    
    def __init__(self):
        self.config = get_config()
        self.server = McpServer("qanat-ui")
        self.catalog_service = CatalogService(self.config)
        self.orders_service = OrdersService(self.config)
        self.orchestrator = IntentOrchestrator()
        
        # Setup MCP server capabilities
        self.server.capabilities = ServerCapabilities(
            tools=True,
            resources=True,
            notifications=NotificationOptions(changed=True)
        )
        
        # Register handlers
        self._register_tools()
        self._register_resources()
        
        logger.info("Qanat MCP-UI Server initialized")
    
    def _register_tools(self):
        """Register MCP tools for Square operations"""
        
        @self.server.tool("get_catalog_items")
        async def get_catalog_items(
            limit: int = 50,
            cursor: Optional[str] = None,
            category_ids: Optional[List[str]] = None
        ) -> CallToolResult:
            """Retrieve catalog items from Square"""
            try:
                items = await self.catalog_service.get_items(
                    limit=limit, cursor=cursor, category_ids=category_ids
                )
                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps(items, indent=2))],
                    isError=False
                )
            except Exception as e:
                logger.error("Failed to get catalog items", error=str(e))
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {str(e)}")],
                    isError=True
                )
        
        @self.server.tool("toggle_item_status")
        async def toggle_item_status(
            item_id: str,
            status: Optional[str] = None
        ) -> CallToolResult:
            """Toggle catalog item active/inactive status"""
            try:
                result = await self.catalog_service.toggle_status(item_id, status)
                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps(result, indent=2))],
                    isError=False
                )
            except Exception as e:
                logger.error("Failed to toggle item status", item_id=item_id, error=str(e))
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {str(e)}")],
                    isError=True
                )
        
        @self.server.tool("get_recent_orders")
        async def get_recent_orders(
            limit: int = 20,
            location_ids: Optional[List[str]] = None,
            created_after: Optional[str] = None
        ) -> CallToolResult:
            """Fetch recent orders from Square"""
            try:
                orders = await self.orders_service.get_recent_orders(
                    limit=limit, location_ids=location_ids, created_after=created_after
                )
                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps(orders, indent=2))],
                    isError=False
                )
            except Exception as e:
                logger.error("Failed to get recent orders", error=str(e))
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {str(e)}")],
                    isError=True
                )
        
        @self.server.tool("get_order_details")
        async def get_order_details(order_id: str) -> CallToolResult:
            """Get detailed order information"""
            try:
                order = await self.orders_service.get_order_details(order_id)
                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps(order, indent=2))],
                    isError=False
                )
            except Exception as e:
                logger.error("Failed to get order details", order_id=order_id, error=str(e))
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {str(e)}")],
                    isError=True
                )
        
        @self.server.tool("process_refund")
        async def process_refund(order_id: str, reason: str = "Customer request") -> CallToolResult:
            """Process refund for an order"""
            try:
                result = await self.orders_service.process_refund(order_id, reason)
                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps(result, indent=2))],
                    isError=False
                )
            except Exception as e:
                logger.error("Failed to process refund", order_id=order_id, error=str(e))
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {str(e)}")],
                    isError=True
                )
        
        @self.server.tool("mark_order_complete")
        async def mark_order_complete(order_id: str) -> CallToolResult:
            """Mark order as completed"""
            try:
                result = await self.orders_service.mark_complete(order_id)
                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps(result, indent=2))],
                    isError=False
                )
            except Exception as e:
                logger.error("Failed to mark order complete", order_id=order_id, error=str(e))
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {str(e)}")],
                    isError=True
                )
    
    def _register_resources(self):
        """Register MCP resources for UI components"""
        
        @self.server.resource("qanat://catalog/dashboard")
        async def catalog_dashboard() -> ReadResourceResult:
            """Catalog management dashboard"""
            try:
                items = await self.catalog_service.get_items(limit=50)
                dashboard_data = {
                    "type": "dashboard",
                    "title": "Square Catalog",
                    "components": [
                        {
                            "type": "table",
                            "id": "catalog_table",
                            "columns": [
                                {"key": "name", "label": "Item Name", "sortable": True},
                                {"key": "price", "label": "Price", "sortable": True},
                                {"key": "status", "label": "Status", "type": "badge"},
                                {"key": "actions", "label": "Actions", "type": "buttons"}
                            ],
                            "data": [
                                {
                                    "id": item.get("id"),
                                    "name": item.get("name", "Unknown"),
                                    "price": f"${item.get('base_price_money', {}).get('amount', 0) / 100:.2f}",
                                    "status": {
                                        "text": "In Stock" if item.get("present_at_all_locations") else "Out of Stock",
                                        "color": "green" if item.get("present_at_all_locations") else "red"
                                    },
                                    "actions": [
                                        {
                                            "label": "Toggle Status",
                                            "action": "toggle_item_status",
                                            "params": {"item_id": item.get("id")}
                                        },
                                        {
                                            "label": "Details",
                                            "action": "view_item_details",
                                            "params": {"item_id": item.get("id")}
                                        }
                                    ]
                                }
                                for item in items.get("items", [])
                            ],
                            "clickable_rows": True
                        },
                        {
                            "type": "button_group",
                            "buttons": [
                                {"label": "Refresh", "action": "refresh_catalog", "primary": True},
                                {"label": "Add Item", "action": "add_item"}
                            ]
                        }
                    ]
                }
                
                return ReadResourceResult(
                    contents=[TextContent(
                        type="text",
                        text=json.dumps(dashboard_data, indent=2)
                    )]
                )
            except Exception as e:
                logger.error("Failed to render catalog dashboard", error=str(e))
                return ReadResourceResult(
                    contents=[TextContent(
                        type="text",
                        text=f"Error loading catalog: {str(e)}"
                    )]
                )
        
        @self.server.resource("qanat://orders/dashboard")
        async def orders_dashboard() -> ReadResourceResult:
            """Orders monitoring dashboard"""
            try:
                orders = await self.orders_service.get_recent_orders(limit=20)
                dashboard_data = {
                    "type": "dashboard",
                    "title": "Recent Orders",
                    "components": [
                        {
                            "type": "table",
                            "id": "orders_table",
                            "columns": [
                                {"key": "order_id", "label": "Order ID", "sortable": True},
                                {"key": "customer", "label": "Customer"},
                                {"key": "items", "label": "Items"},
                                {"key": "total", "label": "Total", "sortable": True},
                                {"key": "status", "label": "Status", "type": "badge"},
                                {"key": "actions", "label": "Actions", "type": "buttons"}
                            ],
                            "data": [
                                {
                                    "id": order.get("id"),
                                    "order_id": order.get("id", "")[:8] + "...",
                                    "customer": order.get("fulfillments", [{}])[0].get("pickup_details", {}).get("recipient", {}).get("display_name", "Guest"),
                                    "items": ", ".join([
                                        item.get("name", "Unknown") 
                                        for item in order.get("line_items", [])
                                    ]),
                                    "total": f"${order.get('total_money', {}).get('amount', 0) / 100:.2f}",
                                    "status": {
                                        "text": order.get("state", "UNKNOWN").title(),
                                        "color": {
                                            "OPEN": "yellow",
                                            "COMPLETED": "green", 
                                            "CANCELED": "red"
                                        }.get(order.get("state"), "gray")
                                    },
                                    "actions": [
                                        {
                                            "label": "Refund",
                                            "action": "process_refund",
                                            "params": {"order_id": order.get("id")},
                                            "visible": order.get("state") == "OPEN"
                                        },
                                        {
                                            "label": "Complete",
                                            "action": "mark_order_complete", 
                                            "params": {"order_id": order.get("id")},
                                            "visible": order.get("state") == "OPEN"
                                        },
                                        {
                                            "label": "Details",
                                            "action": "view_order_details",
                                            "params": {"order_id": order.get("id")}
                                        }
                                    ]
                                }
                                for order in orders.get("orders", [])
                            ],
                            "clickable_rows": True
                        },
                        {
                            "type": "button_group",
                            "buttons": [
                                {"label": "Refresh", "action": "refresh_orders", "primary": True},
                                {"label": "Export", "action": "export_orders"}
                            ]
                        }
                    ]
                }
                
                return ReadResourceResult(
                    contents=[TextContent(
                        type="text",
                        text=json.dumps(dashboard_data, indent=2)
                    )]
                )
            except Exception as e:
                logger.error("Failed to render orders dashboard", error=str(e))
                return ReadResourceResult(
                    contents=[TextContent(
                        type="text",
                        text=f"Error loading orders: {str(e)}"
                    )]
                )
    
    async def start(self, host: str = "localhost", port: int = 3001):
        """Start the MCP server"""
        logger.info("Starting Qanat MCP-UI Server", host=host, port=port)
        
        # Initialize services
        await self.catalog_service.initialize()
        await self.orders_service.initialize()
        
        # Start server
        await self.server.run(host=host, port=port)
    
    async def stop(self):
        """Stop the MCP server"""
        logger.info("Stopping Qanat MCP-UI Server")
        await self.server.stop()

# Server instance for module-level access
server_instance = None

async def get_server() -> QanatServer:
    """Get the global server instance"""
    global server_instance
    if server_instance is None:
        server_instance = QanatServer()
    return server_instance

def main():
    """Main entry point for the server"""
    import sys
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    config = get_config()
    host = config["mcp_server"]["host"]
    port = config["mcp_server"]["port"]
    
    async def run_server():
        server = await get_server()
        await server.start(host, port)
    
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error("Server error", error=str(e))
        sys.exit(1)

import asyncio

if __name__ == "__main__":
    # Initialize your Qanat MCP server
    qanat = QanatServer()

    # Run the MCP server's async loop so Goose can connect
    try:
        asyncio.run(qanat.server.run())
    except KeyboardInterrupt:
        print("Qanat MCP server stopped by user")