Qanat Architecture Overview
+-------------------+
|   Goose Desktop   |   <-- Container environment
|  (MCP-UI surface) |
+---------+---------+
|
v
+-------------------+        +-------------------+
|   Qanat MCP-UI    |        |   Other Goose     |
|   Extension       |        |   Extensions      |
| (Custom MCP server|        | (optional)        |
|  wrapping Square) |        +-------------------+
+---------+---------+
|
v
+-------------------+
| Square MCP Server |
| (Catalog, Orders, |
|  Refunds, etc.)   |
+---------+---------+
|
v
+-------------------+
| Square API        |
| (Seller data)     |
+-------------------+

## Voice/Gesture Inputs (parallel):

+-------------------+        +-------------------+
| ElevenLabs STT/TTS|        | MediaPipe Gesture |
| Voice Agent       |        | Agent             |
+---------+---------+        +---------+---------+
|                           |
v                           v
Intent routed to Qanat MCP-UI Extension
(e.g., "Show orders", "Refund order")

## UI Rendering:

Qanat MCP-UI Extension returns structured UI payloads
→ Goose Desktop renders tables, buttons, status badges
→ User interacts via click, voice, or gesture 