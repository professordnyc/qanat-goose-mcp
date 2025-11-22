"""
Square Orders Service
Handles order operations and refunds via Square API
"""

import asyncio
import aiohttp
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import structlog
import uuid

logger = structlog.get_logger(__name__)

class OrdersService:
    """Service for Square orders operations"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.square_config = config["square"]
        self.api_key = self.square_config["api_key"]
        self.environment = self.square_config["environment"]
        self.base_url = self._get_base_url()
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Mock demo orders data
        self.demo_orders = {
            "orders": [
                {
                    "id": "order_001",
                    "state": "OPEN",
                    "created_at": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
                    "updated_at": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
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
                            "recipient": {
                                "display_name": "John Doe"
                            }
                        }
                    }]
                },
                {
                    "id": "order_002",
                    "state": "COMPLETED", 
                    "created_at": (datetime.utcnow() - timedelta(hours=4)).isoformat(),
                    "updated_at": (datetime.utcnow() - timedelta(hours=3)).isoformat(),
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
                            "recipient": {
                                "display_name": "Jane Smith"
                            }
                        }
                    }]
                },
                {
                    "id": "order_003",
                    "state": "OPEN",
                    "created_at": (datetime.utcnow() - timedelta(minutes=30)).isoformat(),
                    "updated_at": (datetime.utcnow() - timedelta(minutes=30)).isoformat(),
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
                            "recipient": {
                                "display_name": "Bob Wilson"
                            }
                        }
                    }]
                }
            ]
        }
        
        logger.info("OrdersService initialized", environment=self.environment)
    
    def _get_base_url(self) -> str:
        """Get Square API base URL based on environment"""
        if self.environment == "production":
            return "https://connect.squareup.com/v2"
        else:
            return "https://connect.squareupsandbox.com/v2"
    
    async def initialize(self):
        """Initialize the service and HTTP session"""
        self.session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json", 
                "Square-Version": "2023-10-18"
            }
        )
        logger.info("OrdersService session initialized")
    
    async def get_recent_orders(
        self,
        limit: int = 20,
        location_ids: Optional[List[str]] = None,
        created_after: Optional[str] = None
    ) -> Dict[str, Any]:
        """Fetch recent orders"""
        try:
            logger.info("Fetching recent orders", limit=limit, location_ids=location_ids)
            
            orders = self.demo_orders["orders"]
            
            # Apply date filter if specified
            if created_after:
                cutoff_date = datetime.fromisoformat(created_after.replace('Z', '+00:00'))
                orders = [
                    order for order in orders
                    if datetime.fromisoformat(order["created_at"].replace('Z', '+00:00')) > cutoff_date
                ]
            
            # Apply limit
            orders = orders[:limit]
            
            result = {
                "orders": orders,
                "cursor": None  # No pagination for demo
            }
            
            logger.info("Recent orders retrieved", count=len(orders))
            return result
            
        except Exception as e:
            logger.error("Failed to get recent orders", error=str(e))
            raise
    
    async def get_order_details(self, order_id: str) -> Dict[str, Any]:
        """Get detailed order information"""
        try:
            logger.info("Getting order details", order_id=order_id)
            
            # Find order in demo data
            order = None
            for demo_order in self.demo_orders["orders"]:
                if demo_order["id"] == order_id:
                    order = demo_order.copy()
                    break
            
            if not order:
                raise ValueError(f"Order not found: {order_id}")
            
            # Add additional details for UI
            order.update({
                "payment_status": "COMPLETED" if order["state"] == "COMPLETED" else "PENDING",
                "items_summary": ", ".join([
                    f"{item['name']} x{item['quantity']}"
                    for item in order.get("line_items", [])
                ]),
                "customer_info": order.get("fulfillments", [{}])[0].get("pickup_details", {}).get("recipient", {})
            })
            
            logger.info("Order details retrieved", order_id=order_id)
            return order
            
        except Exception as e:
            logger.error("Failed to get order details", order_id=order_id, error=str(e))
            raise
    
    async def mark_complete(self, order_id: str) -> Dict[str, Any]:
        """Mark an order as completed"""
        try:
            logger.info("Marking order as complete", order_id=order_id)
            
            # Find and update order in demo data
            order = None
            for demo_order in self.demo_orders["orders"]:
                if demo_order["id"] == order_id:
                    order = demo_order
                    break
            
            if not order:
                raise ValueError(f"Order not found: {order_id}")
            
            if order["state"] != "OPEN":
                raise ValueError(f"Order {order_id} is not in OPEN state")
            
            # Update order state
            order["state"] = "COMPLETED"
            order["updated_at"] = datetime.utcnow().isoformat()
            
            result = {
                "order_id": order_id,
                "old_state": "OPEN",
                "new_state": "COMPLETED", 
                "updated_at": order["updated_at"],
                "total": f"${order.get('total_money', {}).get('amount', 0) / 100:.2f}"
            }
            
            logger.info("Order marked as complete", **result)
            return result
            
        except Exception as e:
            logger.error("Failed to mark order complete", order_id=order_id, error=str(e))
            raise
    
    async def process_refund(self, order_id: str, reason: str = "Customer request") -> Dict[str, Any]:
        """Process a refund for an order"""
        try:
            logger.info("Processing refund", order_id=order_id, reason=reason)
            
            # Find order in demo data
            order = None
            for demo_order in self.demo_orders["orders"]:
                if demo_order["id"] == order_id:
                    order = demo_order
                    break
            
            if not order:
                raise ValueError(f"Order not found: {order_id}")
            
            if order["state"] not in ["OPEN", "COMPLETED"]:
                raise ValueError(f"Order {order_id} cannot be refunded in {order['state']} state")
            
            # Create refund record
            refund_id = f"refund_{uuid.uuid4().hex[:8]}"
            refund_amount = order.get("total_money", {}).get("amount", 0)
            
            # Update order state to cancelled
            order["state"] = "CANCELED"
            order["updated_at"] = datetime.utcnow().isoformat()
            
            result = {
                "refund_id": refund_id,
                "order_id": order_id,
                "amount_refunded": f"${refund_amount / 100:.2f}",
                "reason": reason,
                "status": "COMPLETED",
                "processed_at": datetime.utcnow().isoformat(),
                "original_total": f"${refund_amount / 100:.2f}"
            }
            
            logger.info("Refund processed", **result)
            return result
            
        except Exception as e:
            logger.error("Failed to process refund", order_id=order_id, error=str(e))
            raise
    
    async def seed_demo_data(self) -> Dict[str, Any]:
        """Seed demo orders data for testing"""
        try:
            logger.info("Seeding demo orders data")
            
            # In a real implementation, this would make Square API calls
            # For demo, we just confirm our mock data is ready
            
            total_revenue = sum(
                order.get("total_money", {}).get("amount", 0)
                for order in self.demo_orders["orders"]
                if order.get("state") == "COMPLETED"
            ) / 100
            
            pending_orders = len([
                order for order in self.demo_orders["orders"]
                if order.get("state") == "OPEN"
            ])
            
            result = {
                "status": "success",
                "orders_seeded": len(self.demo_orders["orders"]),
                "pending_orders": pending_orders,
                "completed_orders": len(self.demo_orders["orders"]) - pending_orders,
                "total_revenue": total_revenue
            }
            
            logger.info("Demo orders data seeded", **result)
            return result
            
        except Exception as e:
            logger.error("Failed to seed demo orders data", error=str(e))
            raise
    
    async def close(self):
        """Close the HTTP session"""
        if self.session:
            await self.session.close()
            logger.info("OrdersService session closed")

    async def __aenter__(self):
        """Async context manager entry"""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()

# Utility function for testing
async def test_orders_service():
    """Test the orders service"""
    config = {
        "square": {
            "api_key": "test_key",
            "environment": "sandbox"
        }
    }
    
    async with OrdersService(config) as service:
        # Test getting orders
        orders = await service.get_recent_orders()
        print(f"Orders: {len(orders['orders'])}")
        
        # Test order details
        if orders["orders"]:
            first_order = orders["orders"][0]
            details = await service.get_order_details(first_order["id"])
            print(f"Order details: {details['id']}")
        
        # Test seeding demo data
        seed_result = await service.seed_demo_data()
        print(f"Seed result: {seed_result}")

if __name__ == "__main__":
    asyncio.run(test_orders_service())
