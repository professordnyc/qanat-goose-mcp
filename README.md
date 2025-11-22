## Qanat Goose MCP Extension

🔄 Looking for the standalone prototype? See [Qanat](https://github.com/professordnyc/Qanat).

Qanat Goose MCP Extension is an agent‑based Goose MCP‑UI extension that wraps the Square MCP Server, integrating sandbox catalog/orders with voice and gesture agents for an interactive seller dashboard.

## 🏗️ Architecture

Qanat integrates with Goose Desktop as a custom MCP-UI extension:

```
Goose Desktop (MCP-UI surface)
    ↓
Qanat MCP-UI Extension ← Voice/Gesture Agents  
    ↓
Square MCP Server
    ↓  
Square API
```

## 🚀 Quick Start

1. **Setup Environment**
   ```bash
   # Copy environment template
   cp env.example .env
   
   # Edit .env with your API keys
   # SQUARE_API_KEY=your_key_here
   # ELEVENLABS_API_KEY=your_key_here
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the MCP Server**
   ```bash
   npm run dev
   # or
   python -m backend.mcp_servers.qanat_server
   ```

4. **Connect to Goose Desktop**
   - Add Qanat as MCP-UI extension in Goose settings
   - Server will run on localhost:3001

## 🔄 Running Both Qanat Demos
There are two versions of Qanat available:
Qanat (Baseline Prototype)
- Standalone dashboard using Web Speech API and seeded demo data.
- Runs entirely in the browser, with fallback APIs when Square is unreachable.
- To run:
- Clone the qanat repo.
- Install dependencies (npm install).
- Start the backend mock server (npm run dev).
- Start the frontend (cd frontend && npm run dev).
- Visit http://localhost:5173 in Chrome and allow microphone access.
Qanat Goose MCP Extension (Advanced)
- Goose MCP‑UI extension wrapping Square MCP Server.
- Integrates Square sandbox catalog/orders with voice and gesture agents.
- To run:
- Clone the qanat-goose-mcp repo.
- Copy env.template → .env and add your Square sandbox OAuth credentials.
- Start the MCP server (npm run dev or python -m backend.mcp_servers.qanat_server).
- In Goose Desktop, add Qanat as an MCP‑UI extension with endpoint http://localhost:3001.
- Interact via voice, gesture, or UI buttons.

## 📁 Project Structure

```
qanat_v2/
├── backend/                    # Core backend services
│   ├── agents/                # Goose subagents (voice, gesture)
│   ├── services/              # Square API integration
│   └── mcp_servers/           # MCP protocol servers
├── config/                    # Configuration files
│   ├── extensions/            # Extension configs (Square, voice, gesture)
│   └── environments/          # Environment loading utilities
├── docs/                      # Project documentation
│   ├── PROJECT_BOARD.md       # Development task breakdown
│   ├── PLAN.md               # MVP development plan  
│   └── Qanat_Architecture_Overview.md
├── requirements.txt           # Python dependencies
├── package.json              # Project metadata & scripts
└── env.example               # Environment template
```

## 🎯 MVP Features

- **Catalog Dashboard**: View and manage Square catalog items
- **Orders Dashboard**: Monitor recent orders and status updates  
- **Voice Control**: "Refresh catalog" command via ElevenLabs
- **Gesture Control**: Toggle item status with thumb-up gesture via MediaPipe
- **Interactive UI**: Clickable tables and action buttons in Goose Desktop

## 🛠️ Development

See [docs/PROJECT_BOARD.md](docs/PROJECT_BOARD.md) for detailed development tasks and timeline.

### Key Components

- **MCP-UI Server**: `backend/mcp_servers/qanat_server.py`
- **Square Integration**: `backend/services/`
- **Voice Agent**: Uses ElevenLabs for speech-to-text
- **Gesture Agent**: Uses MediaPipe for hand gesture recognition

### Configuration Files

- `config/extensions/square_mcp.json` - Square API integration config
- `config/extensions/qanat_mcp_ui.json` - UI component definitions  
- `config/extensions/elevenlabs_voice.json` - Voice command mappings
- `config/extensions/mediapipe_gesture.json` - Gesture recognition setup

## 🔧 Scripts

```bash
npm run dev          # Start development server
npm run start        # Start production server  
npm run test         # Run tests
npm run setup        # Install dependencies
npm run config       # Validate configuration
```

## 📋 Environment Variables

Required variables (copy from `env.example`):

- `SQUARE_API_KEY` - Your Square API key  
- `SQUARE_ENVIRONMENT` - sandbox/production
- `ELEVENLABS_API_KEY` - ElevenLabs API key for voice features
- `MEDIAPIPE_CONFIDENCE_THRESHOLD` - Gesture detection sensitivity

## 🎮 Usage

### Voice Commands
- "Refresh catalog" - Reload catalog items
- "Show orders" - Display recent orders  
- "Help" - Show available commands

### Gesture Controls  
- 👍 **Thumb up** - Toggle item active/inactive status
- 👉 **Point** - Select table row
- ✋ **Open palm** - Refresh current view
- ✌️ **Peace sign** - Switch catalog/orders view

## 🧪 Testing

```bash
# Run all tests
npm run test

# Test Square integration
python -m pytest tests/test_square_services.py

# Test voice commands  
python -m pytest tests/test_voice_agent.py

# Test gesture recognition
python -m pytest tests/test_gesture_agent.py
```

## 📝 License

MIT License - see LICENSE file for details.

---

*Built with ❤️ for Square sellers using Goose Desktop*

## Contact

Reach me here or on Discord: @professordnyc
