# Qanat MVP - Sprint Task Board

**Project**: Qanat Square Seller Dashboard Assistant  
**Sprint Duration**: 40 minutes  
**Team**: 4 developers (Architect, Backend, Frontend, QA)  
**Created**: 2025-11-21 15:57

## Sprint Goals
- [ ] Functional MCP-UI extension displaying Square catalog/orders
- [ ] Interactive UI components (tables, buttons, click handlers)
- [ ] Voice input for one command (catalog refresh)
- [ ] Gesture input for one action (toggle item status)
- [ ] Demo-ready MVP with live Square data

---

## 🏗️ **ARCHITECT TASKS** (Minutes 0-10)
*Must complete first - blocks other development*

### **CRITICAL PATH** ⚠️
- [ ] **A1**: Set up project structure and directories (2 min)
  - Create `ui_components/`, `square_integration/`, `config/` folders
  - Initialize `__init__.py` files
  - Set up basic project skeleton

- [ ] **A2**: Define MCP-UI protocol interfaces (3 min)
  - Design data models for catalog/order responses
  - Define UI component JSON schemas
  - Create base classes for Square integration

- [ ] **A3**: Configure development environment (2 min)
  - Set up Square sandbox credentials
  - Create `requirements.txt` with dependencies
  - Configure MCP server settings template

- [ ] **A4**: Document component specifications (3 min)
  - Define catalog table structure
  - Define orders table structure
  - Specify voice/gesture integration points

---

## 🔧 **BACKEND DEVELOPER TASKS** (Minutes 5-30)
*Can start after A1-A2 complete*

### **CORE SERVICES** (Minutes 5-20)
- [ ] **B1**: Build MCP server foundation (5 min)
  - `qanat_mcp_server.py` - basic MCP protocol implementation
  - Health check and lifecycle management
  - Connection to Square MCP

- [ ] **B2**: Implement Square catalog service (5 min)
  - `square_integration/catalog_service.py`
  - Fetch items, toggle status, get item details
  - Error handling and caching

- [ ] **B3**: Implement Square orders service (5 min)
  - `square_integration/orders_service.py`
  - Fetch recent orders, get order details
  - Status updates and filtering

### **INPUT INTEGRATIONS** (Minutes 20-30)
- [ ] **B4**: Voice input integration (5 min)
  - ElevenLabs STT for "refresh catalog" command
  - Route voice intent to catalog service
  - Basic speech-to-action mapping

- [ ] **B5**: Gesture input integration (5 min)
  - MediaPipe for item status toggle gesture
  - Simple hand gesture recognition (tap/swipe)
  - Connect gesture to catalog toggle action

---

## 🎨 **FRONTEND DEVELOPER TASKS** (Minutes 10-35)
*Can start after A2 complete*

### **UI COMPONENTS** (Minutes 10-25)
- [ ] **F1**: Build catalog dashboard UI (8 min)
  - `ui_components/catalog_dashboard.py`
  - Items table with name, price, status columns
  - Toggle buttons and refresh functionality
  - Item details modal

- [ ] **F2**: Build orders dashboard UI (7 min)
  - `ui_components/orders_dashboard.py`
  - Orders table with ID, customer, total, status
  - Status badges with color coding
  - Order details view

### **INTERACTION LAYER** (Minutes 25-35)
- [ ] **F3**: Implement click handlers (5 min)
  - Table row clicks for details
  - Button actions (refresh, toggle)
  - Loading states and error messages

- [ ] **F4**: Style and polish UI (5 min)
  - Status badge colors (green/yellow/red)
  - Consistent button styling
  - Responsive table layout

---

## 🧪 **QA DEVELOPER TASKS** (Minutes 15-40)
*Can start after B1 complete*

### **TESTING & VALIDATION** (Minutes 15-35)
- [ ] **Q1**: Set up test environment (5 min)
  - Square sandbox account validation
  - Mock data creation for testing
  - Test runner configuration

- [ ] **Q2**: Test Square integrations (8 min)
  - Verify catalog data retrieval
  - Test order data display
  - Validate API error handling

- [ ] **Q3**: Test UI interactions (7 min)
  - Click handlers functionality
  - Voice command recognition
  - Gesture action triggers

### **DEMO PREPARATION** (Minutes 35-40)
- [ ] **Q4**: End-to-end testing (3 min)
  - Full workflow from voice/gesture to UI update
  - Performance validation
  - Demo script verification

- [ ] **Q5**: Bug fixes and polish (2 min)
  - Address critical issues found
  - Ensure demo readiness

---

## ⏱️ **PARALLEL EXECUTION TIMELINE**

### **Minutes 0-5: Foundation**
- Architect: Project setup (A1, A2) 
- Others: Wait/prepare

### **Minutes 5-15: Core Development**
- Backend: MCP server + catalog service (B1, B2)
- Frontend: Wait for A2 completion
- QA: Wait for B1 completion

### **Minutes 10-20: UI & Services**
- Backend: Orders service (B3)
- Frontend: Catalog dashboard (F1)
- QA: Test environment setup (Q1)

### **Minutes 15-30: Advanced Features**
- Backend: Voice + gesture integration (B4, B5)
- Frontend: Orders dashboard (F2)
- QA: Square integrations testing (Q2)

### **Minutes 30-40: Integration & Testing**
- Backend: Done, support QA
- Frontend: Interactions + polish (F3, F4)
- QA: UI testing + demo prep (Q3, Q4, Q5)

---

## 🚫 **BLOCKED DEPENDENCIES**

- **Backend B1** blocks QA Q1 (need server running)
- **Architect A2** blocks Frontend F1, F2 (need component specs)
- **Backend B2, B3** blocks QA Q2 (need services to test)
- **All development** blocks QA Q4 (need complete system)

---

## 🎯 **DEMO SUCCESS CRITERIA**

**Must Have (MVP)**:
- [ ] Catalog table displays live Square items
- [ ] Orders table shows recent Square orders  
- [ ] Click interactions work (item details, refresh)
- [ ] Voice command triggers catalog refresh
- [ ] Gesture toggles item status

**Nice to Have**:
- [ ] Smooth loading states
- [ ] Error handling demonstrations
- [ ] Status badge color coding

---

## 🚨 **RISK MITIGATION**

**High Risk**:
- Square API connectivity issues → Use mock data backup
- Voice/gesture integration complexity → Simplify to basic triggers
- Time overruns → Prioritize catalog over orders if needed

**Medium Risk**:
- MCP-UI rendering issues → Test early and often
- Cross-agent coordination → Clear handoff points defined

---

*Last Updated: 2025-11-21 15:57*  
*Sprint Status: Ready to Start*
