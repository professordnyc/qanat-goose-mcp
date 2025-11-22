# Qanat Component Specifications

## UI Component Definitions

### Catalog Dashboard Table Structure
```typescript
interface CatalogTableRow {
  id: string;
  name: string;
  price: number;
  status: 'active' | 'inactive';
  category?: string;
  inventory_count?: number;
  actions: ['toggle_status', 'view_details', 'edit'];
}

interface CatalogTableComponent {
  type: 'table';
  columns: ['name', 'price', 'status', 'actions'];
  data: CatalogTableRow[];
  clickable_rows: true;
  sortable: ['name', 'price', 'status'];
  filterable: ['status', 'category'];
}
```

### Orders Dashboard Table Structure  
```typescript
interface OrderTableRow {
  id: string;
  order_id: string;
  customer_name?: string;
  customer_email?: string;
  total_money: {
    amount: number;
    currency: 'USD';
  };
  status: 'pending' | 'fulfilled' | 'cancelled';
  created_at: string;
  actions: ['view_details', 'update_status'];
}

interface OrderTableComponent {
  type: 'table'; 
  columns: ['order_id', 'customer', 'total', 'status'];
  data: OrderTableRow[];
  clickable_rows: true;
  status_badges: true;
  sortable: ['order_id', 'total', 'created_at'];
  filterable: ['status'];
}
```

## Voice/Gesture Integration Points

### Voice Command Intents
```typescript
interface VoiceIntent {
  trigger: string[];
  intent: string;
  target: string;
  response: string;
}

// Example mappings
const VOICE_INTENTS: VoiceIntent[] = [
  {
    trigger: ["refresh catalog", "update catalog", "reload items"],
    intent: "catalog.refresh", 
    target: "get_catalog_items",
    response: "Refreshing your catalog items..."
  },
  {
    trigger: ["show orders", "view orders", "recent orders"],
    intent: "orders.view",
    target: "get_recent_orders", 
    response: "Loading your recent orders..."
  }
];
```

### Gesture Action Mappings
```typescript
interface GestureMapping {
  gesture: string;
  intent: string;
  target: string;
  description: string;
  cooldown_ms: number;
}

// Example mappings  
const GESTURE_MAPPINGS: GestureMapping[] = [
  {
    gesture: "thumb_up",
    intent: "catalog.toggle_status",
    target: "toggle_item_status", 
    description: "Toggle item active/inactive status",
    cooldown_ms: 1000
  },
  {
    gesture: "point_index",
    intent: "ui.select",
    target: "select_table_row",
    description: "Select table row or UI element", 
    cooldown_ms: 500
  }
];
```

## MCP Protocol Specifications

### Tool Definitions
```json
{
  "tools": [
    {
      "name": "get_catalog_items",
      "description": "Retrieve catalog items from Square API",
      "inputSchema": {
        "type": "object",
        "properties": {
          "limit": {"type": "number", "default": 50},
          "cursor": {"type": "string"},
          "category_ids": {"type": "array", "items": {"type": "string"}}
        }
      }
    },
    {
      "name": "toggle_item_status",
      "description": "Toggle catalog item active/inactive status", 
      "inputSchema": {
        "type": "object",
        "properties": {
          "item_id": {"type": "string", "required": true},
          "status": {"type": "string", "enum": ["active", "inactive"]}
        },
        "required": ["item_id"]
      }
    },
    {
      "name": "get_recent_orders",
      "description": "Fetch recent orders from Square API",
      "inputSchema": {
        "type": "object", 
        "properties": {
          "limit": {"type": "number", "default": 20},
          "location_ids": {"type": "array", "items": {"type": "string"}},
          "created_after": {"type": "string", "format": "date-time"}
        }
      }
    },
    {
      "name": "get_order_details", 
      "description": "Get detailed order information",
      "inputSchema": {
        "type": "object",
        "properties": {
          "order_id": {"type": "string", "required": true}
        },
        "required": ["order_id"]
      }
    }
  ]
}
```

### Resource Definitions
```json
{
  "resources": [
    {
      "uri": "qanat://catalog/dashboard",
      "name": "Catalog Dashboard",
      "description": "Interactive catalog management interface",
      "mimeType": "application/vnd.qanat.dashboard+json"
    },
    {
      "uri": "qanat://orders/dashboard", 
      "name": "Orders Dashboard",
      "description": "Recent orders monitoring interface",
      "mimeType": "application/vnd.qanat.dashboard+json"
    }
  ]
}
```

## Data Flow Specifications

### Square API → MCP Server → UI Flow
```
1. User action (click/voice/gesture)
2. Intent recognized and routed to MCP tool
3. MCP tool calls Square service
4. Square service makes API request
5. Response formatted for UI component
6. UI component updated in Goose Desktop
```

### Error Handling Flow
```
1. API/Service error occurs
2. Error logged with structured logging
3. User-friendly error message prepared
4. UI shows error state with retry option
5. Voice/TTS announces error (if voice enabled)
```

## Testing Specifications

### Unit Test Requirements
- All Square API service methods
- Voice intent recognition accuracy  
- Gesture detection confidence levels
- MCP protocol message handling
- UI component rendering

### Integration Test Scenarios
- End-to-end catalog refresh via voice
- Gesture-triggered item status toggle
- Order details modal display
- Error recovery and retry flows
- Multi-modal interaction sequences

### Performance Requirements
- Voice command response < 2 seconds
- Gesture recognition latency < 500ms  
- Table rendering < 1 second for 50 items
- API request timeout: 10 seconds
- UI update refresh rate: 60fps

---

*Component specifications for Qanat MVP development*  
*Version: 0.1.0*  
*Updated: 2025-11-21*
