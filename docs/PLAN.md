# Qanat MVP Development Plan

## Project Overview
Build **Qanat** - a custom Goose MCP-UI extension that helps sellers manage their Square catalog and orders through interactive dashboards. The MVP integrates Square MCP for API access and renders UI components within Goose Desktop.

## MVP Goals (40-minute session)
- Create a functional MCP-UI extension that displays Square data
- Implement basic catalog and order management features
- Demonstrate interactive UI rendering in Goose Desktop
- Establish foundation for voice/gesture inputs (future)

## Core MVP Features

### 1. MCP-UI Extension Setup (10 minutes)
- **File**: `qanat_mcp_server.py`
- **Goal**: Basic MCP server that wraps Square MCP
- **Features**:
  - MCP server initialization
  - Connection to Square MCP
  - Basic error handling
  - Health check endpoints

### 2. Catalog Dashboard (15 minutes)
- **Goal**: Display and manage Square catalog items
- **UI Components**:
  - Items list table (name, price, status)
  - Item details modal
  - Basic item status toggles (active/inactive)
- **Data Sources**:
  - Square catalog API via Square MCP
  - Real-time inventory status

### 3. Orders Dashboard (10 minutes)
- **Goal**: View and manage recent orders
- **UI Components**:
  - Orders list (ID, customer, total, status)
  - Order details view
  - Basic status updates (pending → fulfilled)
- **Data Sources**:
  - Square orders API
  - Payment status information

### 4. Interactive UI Rendering (5 minutes)
- **Goal**: Demonstrate click interactions within Goose Desktop
- **Features**:
  - Clickable table rows
  - Action buttons (refresh, toggle status)
  - Status badges with color coding
  - Loading states

## Project Structure
```
qanat_v2/
├── PLAN.md                     # This file
├── README.md                   # Project documentation  
├── Qanat_Architecture_Overview.md  # Architecture diagram
├── qanat_mcp_server.py         # Main MCP-UI server
├── ui_components/              # UI rendering logic
│   ├── __init__.py
│   ├── catalog_dashboard.py    # Catalog UI components
│   ├── orders_dashboard.py     # Orders UI components
│   └── common.py              # Shared UI utilities
├── square_integration/         # Square API wrappers
│   ├── __init__.py
│   ├── catalog_service.py      # Catalog operations
│   └── orders_service.py       # Order operations
├── config/                     # Configuration files
│   ├── server_config.json      # MCP server settings
│   └── square_config.json      # Square API credentials
└── tests/                      # Basic tests
```

## Development Sequence

### Phase 1: MCP Server Foundation (10 minutes)
1. Create `qanat_mcp_server.py` with MCP-UI protocol
2. Set up basic server lifecycle (start, stop, health)
3. Establish connection pattern to Square MCP
4. Implement basic logging and error handling

### Phase 2: Catalog Management (15 minutes)
1. Create `catalog_service.py` - wrapper for Square catalog API
2. Build `catalog_dashboard.py` - UI components for item management
3. Implement:
   - Items list table with pagination
   - Item toggle (active/inactive)
   - Basic item details view
4. Test catalog display in Goose Desktop

### Phase 3: Orders Management (10 minutes) 
1. Create `orders_service.py` - wrapper for Square orders API
2. Build `orders_dashboard.py` - UI components for order management
3. Implement:
   - Recent orders list
   - Order status display
   - Order details modal
4. Test orders display in Goose Desktop

### Phase 4: UI Polish & Interaction (5 minutes)
1. Add loading states and error handling to UI
2. Implement click handlers for interactive elements
3. Add refresh functionality
4. Style status badges and action buttons

## UI Component Examples

### Catalog Dashboard
```json
{
  "type": "dashboard",
  "title": "Square Catalog",
  "components": [
    {
      "type": "table",
      "columns": ["Name", "Price", "Status", "Actions"],
      "data": [...],
      "clickable_rows": true
    },
    {
      "type": "button_group",
      "buttons": [
        {"label": "Refresh", "action": "refresh_catalog"},
        {"label": "Add Item", "action": "add_item"}
      ]
    }
  ]
}
```

### Orders Dashboard  
```json
{
  "type": "dashboard", 
  "title": "Recent Orders",
  "components": [
    {
      "type": "table",
      "columns": ["Order ID", "Customer", "Total", "Status"],
      "data": [...],
      "status_badges": true
    }
  ]
}
```

## Success Criteria
- [ ] MCP-UI server runs and connects to Square MCP
- [ ] Catalog dashboard displays items from Square API
- [ ] Orders dashboard shows recent orders
- [ ] UI renders properly in Goose Desktop
- [ ] Click interactions work (item details, status toggles)
- [ ] Basic error handling for API failures
- [ ] Demo ready: can show live Square data in interactive UI

## Technical Stack
- **Protocol**: MCP-UI for Goose Desktop integration
- **Backend**: Python MCP server
- **APIs**: Square MCP for catalog/orders data
- **UI**: JSON-based component definitions
- **Configuration**: JSON config files for credentials

## Future Enhancements (Post-MVP)
- Voice input via ElevenLabs integration
- Gesture controls via MediaPipe
- Advanced order management (refunds, modifications)
- Inventory alerts and notifications
- Customer management features
- Sales analytics dashboard

## Demo Script (End of Session)
1. Start Qanat MCP server in Goose Desktop
2. Show catalog dashboard with real Square items
3. Demonstrate item status toggle
4. Switch to orders dashboard 
5. Click on order to show details
6. Refresh data to show real-time updates

## Risk Mitigation
- **Square API limits**: Implement caching and rate limiting
- **Authentication**: Use sandbox credentials for demo
- **UI complexity**: Keep components simple and functional
- **Time constraint**: Focus on data display over advanced interactions

---
*Project: Qanat Square Management Extension*  
*Target: 40-minute MVP implementation*  
*Status: Ready for development*  
*Created: 2025-11-21 15:49*
