"""
Square Catalog Service
Handles catalog item operations via Square API
"""

import asyncio
import aiohttp
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import structlog

logger = structlog.get_logger(__name__)

class CatalogService:
    """Service for Square catalog operations"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.square_config = config["square"]
        self.api_key = self.square_config["api_key"]
        self.environment = self.square_config["environment"]
        self.base_url = self._get_base_url()
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Mock data for demo (Square Sandbox integration)
        self.demo_catalog = {
            "items": [
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
                    "present_at_all_locations": False,  # Low stock
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
        }
        
        logger.info("CatalogService initialized", environment=self.environment)
    
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
        logger.info("CatalogService session initialized")
    
    async def get_items(
        self, 
        limit: int = 50,
        cursor: Optional[str] = None,
        category_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Retrieve catalog items"""
        try:
            # For MVP demo, return seeded data
            logger.info("Fetching catalog items", limit=limit, cursor=cursor, category_ids=category_ids)
            
            items = self.demo_catalog["items"]
            
            # Apply category filter if specified
            if category_ids:
                items = [item for item in items if item.get("category_id") in category_ids]
            
            # Apply limit
            items = items[:limit]
            
            result = {
                "items": items,
                "cursor": None  # No pagination for demo
            }
            
            logger.info("Catalog items retrieved", count=len(items))
            return result
            
        except Exception as e:
            logger.error("Failed to get catalog items", error=str(e))
            raise
    
    async def toggle_status(self, item_id: str, status: Optional[str] = None) -> Dict[str, Any]:
        """Toggle item active/inactive status"""
        try:
            logger.info("Toggling item status", item_id=item_id, status=status)
            
            # Find item in demo data
            item = None
            for i, demo_item in enumerate(self.demo_catalog["items"]):
                if demo_item["id"] == item_id:
                    item = demo_item
                    break
            
            if not item:
                raise ValueError(f"Item not found: {item_id}")
            
            # Toggle status
            if status:
                new_status = status.lower() == "active"
            else:
                new_status = not item.get("present_at_all_locations", True)
            
            item["present_at_all_locations"] = new_status
            
            result = {
                "item_id": item_id,
                "old_status": "active" if not new_status else "inactive", 
                "new_status": "active" if new_status else "inactive",
                "updated_at": datetime.utcnow().isoformat()
            }
            
            logger.info("Item status toggled", **result)
            return result
            
        except Exception as e:
            logger.error("Failed to toggle item status", item_id=item_id, error=str(e))
            raise
    
    async def get_item_details(self, item_id: str) -> Dict[str, Any]:
        """Get detailed information about a catalog item"""
        try:
            logger.info("Getting item details", item_id=item_id)
            
            # Find item in demo data
            item = None
            for demo_item in self.demo_catalog["items"]:
                if demo_item["id"] == item_id:
                    item = demo_item.copy()
                    break
            
            if not item:
                raise ValueError(f"Item not found: {item_id}")
            
            # Add additional details for UI
            item.update({
                "stock_status": "In Stock" if item.get("present_at_all_locations") else "Low Stock",
                "last_updated": datetime.utcnow().isoformat(),
                "inventory_count": 25 if item.get("present_at_all_locations") else 2
            })
            
            logger.info("Item details retrieved", item_id=item_id, name=item.get("name"))
            return item
            
        except Exception as e:
            logger.error("Failed to get item details", item_id=item_id, error=str(e))
            raise
    
    async def seed_demo_data(self) -> Dict[str, Any]:
        """Seed demo catalog data for testing"""
        try:
            logger.info("Seeding demo catalog data")
            
            # In a real implementation, this would make Square API calls
            # For demo, we just confirm our mock data is ready
            
            result = {
                "status": "success",
                "items_seeded": len(self.demo_catalog["items"]),
                "categories": ["beverages", "food", "pastries"],
                "total_value": sum(
                    item.get("base_price_money", {}).get("amount", 0) 
                    for item in self.demo_catalog["items"]
                ) / 100
            }
            
            logger.info("Demo catalog data seeded", **result)
            return result
            
        except Exception as e:
            logger.error("Failed to seed demo data", error=str(e))
            raise
    
    async def close(self):
        """Close the HTTP session"""
        if self.session:
            await self.session.close()
            logger.info("CatalogService session closed")

    async def __aenter__(self):
        """Async context manager entry"""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()

# Utility function for testing
async def test_catalog_service():
    """Test the catalog service"""
    config = {
        "square": {
            "api_key": "test_key",
            "environment": "sandbox"
        }
    }
    
    async with CatalogService(config) as service:
        # Test getting items
        items = await service.get_items()
        print(f"Items: {len(items['items'])}")
        
        # Test toggling status
        if items["items"]:
            first_item = items["items"][0]
            toggle_result = await service.toggle_status(first_item["id"])
            print(f"Toggle result: {toggle_result}")
        
        # Test seeding demo data
        seed_result = await service.seed_demo_data()
        print(f"Seed result: {seed_result}")

if __name__ == "__main__":
    asyncio.run(test_catalog_service())
