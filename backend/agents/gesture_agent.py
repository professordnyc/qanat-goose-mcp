"""
Gesture Agent - MediaPipe Integration
Handles hand gesture recognition for UI control
"""

import asyncio
import cv2
import numpy as np
from typing import Dict, Any, Optional, Callable, Tuple
from datetime import datetime, timedelta
import structlog

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False

logger = structlog.get_logger(__name__)

class GestureAgent:
    """Gesture recognition agent using MediaPipe"""
    
    def __init__(self, config: Dict[str, Any], orchestrator=None):
        self.config = config
        self.mediapipe_config = config.get("mediapipe", {})
        self.confidence_threshold = float(self.mediapipe_config.get("confidence_threshold", 0.7))
        self.orchestrator = orchestrator
        
        # MediaPipe setup
        if MEDIAPIPE_AVAILABLE:
            self.mp_hands = mp.solutions.hands
            self.mp_drawing = mp.solutions.drawing_utils
            self.hands = self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=2,
                model_complexity=1,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
        else:
            self.mp_hands = None
            self.hands = None
        
        # Gesture mappings
        self.gesture_mappings = {
            "thumb_up": {
                "intent": "catalog.toggle_status",
                "description": "Toggle item active/inactive status",
                "cooldown_ms": 1000
            },
            "point_index": {
                "intent": "ui.select",
                "description": "Select table row or UI element",
                "cooldown_ms": 500
            },
            "open_palm": {
                "intent": "ui.refresh",
                "description": "Refresh current dashboard",
                "cooldown_ms": 2000
            },
            "peace_sign": {
                "intent": "ui.navigate",
                "description": "Switch between catalog and orders view",
                "cooldown_ms": 1500
            }
        }
        
        # Gesture state
        self.last_gesture_time = {}
        self.current_gesture = None
        self.gesture_confidence = 0.0
        self.is_detecting = False
        self.camera = None
        self.selected_item_id = None  # For context-aware gestures
        
        logger.info("GestureAgent initialized", 
                   mediapipe_available=MEDIAPIPE_AVAILABLE,
                   confidence_threshold=self.confidence_threshold)
    
    async def initialize(self):
        """Initialize the gesture agent"""
        if not MEDIAPIPE_AVAILABLE:
            logger.warning("MediaPipe not available, gesture features disabled")
            return
        
        logger.info("GestureAgent initialized with MediaPipe")
    
    async def start_detection(self, callback: Optional[Callable] = None, camera_id: int = 0):
        """Start gesture detection"""
        if not MEDIAPIPE_AVAILABLE:
            logger.error("MediaPipe not available, cannot start gesture detection")
            return
        
        try:
            self.is_detecting = True
            self.camera = cv2.VideoCapture(camera_id)
            
            if not self.camera.isOpened():
                logger.error("Failed to open camera", camera_id=camera_id)
                return
            
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            logger.info("Gesture detection started", camera_id=camera_id)
            
            while self.is_detecting:
                try:
                    ret, frame = self.camera.read()
                    if not ret:
                        logger.warning("Failed to read camera frame")
                        await asyncio.sleep(0.1)
                        continue
                    
                    # Process frame for gestures
                    gesture_result = await self._process_frame(frame)
                    
                    if gesture_result and callback:
                        await callback(gesture_result)
                    
                    # Brief pause to prevent overprocessing
                    await asyncio.sleep(0.033)  # ~30 FPS
                    
                except Exception as e:
                    logger.error("Error during gesture detection", error=str(e))
                    await asyncio.sleep(0.1)
        
        except Exception as e:
            logger.error("Failed to start gesture detection", error=str(e))
        finally:
            if self.camera:
                self.camera.release()
    
    async def stop_detection(self):
        """Stop gesture detection"""
        self.is_detecting = False
        if self.camera:
            self.camera.release()
        logger.info("Gesture detection stopped")
    
    async def _process_frame(self, frame: np.ndarray) -> Optional[Dict[str, Any]]:
        """Process a single frame for gesture recognition"""
        try:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process with MediaPipe
            results = self.hands.process(rgb_frame)
            
            if not results.multi_hand_landmarks:
                return None
            
            # Analyze first hand (for demo simplicity)
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # Detect gesture
            gesture, confidence = self._classify_gesture(hand_landmarks)
            
            if gesture and confidence > self.confidence_threshold:
                return await self._handle_gesture(gesture, confidence)
            
            return None
            
        except Exception as e:
            logger.error("Failed to process frame", error=str(e))
            return None
    
    def _classify_gesture(self, landmarks) -> Tuple[Optional[str], float]:
        """Classify hand gesture from landmarks"""
        try:
            # Extract landmark positions
            landmark_points = []
            for lm in landmarks.landmark:
                landmark_points.append([lm.x, lm.y])
            
            landmark_array = np.array(landmark_points)
            
            # Simple gesture classification based on landmark positions
            # (In production, you'd use more sophisticated ML models)
            
            # Thumb up detection
            thumb_tip = landmark_array[4]
            thumb_mcp = landmark_array[2]
            index_tip = landmark_array[8]
            
            # Check if thumb is extended upward
            if thumb_tip[1] < thumb_mcp[1] - 0.05:  # Thumb pointing up
                other_fingers_down = all(
                    landmark_array[tip][1] > landmark_array[tip-2][1] 
                    for tip in [8, 12, 16, 20]  # Other finger tips
                )
                if other_fingers_down:
                    return "thumb_up", 0.85
            
            # Point index detection
            index_extended = index_tip[1] < landmark_array[6][1] - 0.05
            other_fingers_folded = all(
                landmark_array[tip][1] > landmark_array[tip-2][1]
                for tip in [12, 16, 20]
            )
            if index_extended and other_fingers_folded:
                return "point_index", 0.8
            
            # Open palm detection (all fingers extended)
            all_extended = all(
                landmark_array[tip][1] < landmark_array[tip-2][1] - 0.03
                for tip in [8, 12, 16, 20]
            )
            if all_extended:
                return "open_palm", 0.75
            
            # Peace sign (index and middle extended)
            index_extended = landmark_array[8][1] < landmark_array[6][1] - 0.05
            middle_extended = landmark_array[12][1] < landmark_array[10][1] - 0.05
            others_folded = all(
                landmark_array[tip][1] > landmark_array[tip-2][1]
                for tip in [16, 20]
            )
            if index_extended and middle_extended and others_folded:
                return "peace_sign", 0.8
            
            return None, 0.0
            
        except Exception as e:
            logger.error("Failed to classify gesture", error=str(e))
            return None, 0.0
    
    async def _handle_gesture(self, gesture: str, confidence: float) -> Optional[Dict[str, Any]]:
        """Handle detected gesture"""
        try:
            # Check cooldown
            now = datetime.utcnow()
            mapping = self.gesture_mappings.get(gesture)
            
            if not mapping:
                return None
            
            last_time = self.last_gesture_time.get(gesture)
            cooldown_ms = mapping["cooldown_ms"]
            
            if last_time:
                time_diff = (now - last_time).total_seconds() * 1000
                if time_diff < cooldown_ms:
                    return None  # Still in cooldown
            
            # Update last gesture time
            self.last_gesture_time[gesture] = now
            
            logger.info("Gesture detected", gesture=gesture, confidence=confidence)
            
            # Prepare gesture parameters
            params = {}
            
            # Add context for specific gestures
            if gesture == "thumb_up" and self.selected_item_id:
                params["item_id"] = self.selected_item_id
            elif gesture == "ui.navigate":
                params["target"] = "toggle_catalog_orders"
            elif gesture == "ui.refresh":
                params["target"] = "current_view"
            
            # Create result
            result = {
                "status": "success",
                "gesture": gesture,
                "confidence": confidence,
                "intent": mapping["intent"],
                "params": params,
                "description": mapping["description"],
                "timestamp": now.isoformat()
            }
            
            # Execute through orchestrator
            if self.orchestrator:
                orchestrator_result = await self.orchestrator.process_intent(
                    mapping["intent"],
                    params,
                    "gesture"
                )
                result["orchestrator_result"] = orchestrator_result
            
            return result
            
        except Exception as e:
            logger.error("Failed to handle gesture", gesture=gesture, error=str(e))
            return None
    
    async def test_gesture(self, gesture: str) -> Dict[str, Any]:
        """Test a gesture without camera input"""
        try:
            mapping = self.gesture_mappings.get(gesture)
            if not mapping:
                return {
                    "status": "error",
                    "error": f"Unknown gesture: {gesture}"
                }
            
            # Simulate gesture detection
            result = await self._handle_gesture(gesture, 0.9)
            if not result:
                result = {
                    "status": "cooldown",
                    "gesture": gesture,
                    "message": "Gesture in cooldown period"
                }
            
            return result
            
        except Exception as e:
            logger.error("Failed to test gesture", gesture=gesture, error=str(e))
            return {
                "status": "error",
                "gesture": gesture,
                "error": str(e)
            }
    
    def set_selected_item(self, item_id: Optional[str]):
        """Set the currently selected item for context-aware gestures"""
        self.selected_item_id = item_id
        logger.info("Selected item updated", item_id=item_id)
    
    def get_available_gestures(self) -> Dict[str, str]:
        """Get list of available gestures"""
        return {
            gesture: info["description"]
            for gesture, info in self.gesture_mappings.items()
        }
    
    async def close(self):
        """Close the gesture agent"""
        await self.stop_detection()
        logger.info("GestureAgent closed")

# Utility function for testing
async def test_gesture_agent():
    """Test the gesture agent"""
    from .orchestrator import IntentOrchestrator
    
    config = {
        "mediapipe": {
            "confidence_threshold": "0.7"
        }
    }
    
    orchestrator = IntentOrchestrator()
    agent = GestureAgent(config, orchestrator)
    
    await agent.initialize()
    
    # Test gestures
    test_gestures = [
        "thumb_up",
        "point_index", 
        "open_palm",
        "peace_sign",
        "unknown_gesture"
    ]
    
    for gesture in test_gestures:
        result = await agent.test_gesture(gesture)
        print(f"Gesture: '{gesture}' -> {result['status']}")
    
    # Show available gestures
    gestures = agent.get_available_gestures()
    print(f"Available gestures: {list(gestures.keys())}")
    
    await agent.close()

if __name__ == "__main__":
    asyncio.run(test_gesture_agent())
