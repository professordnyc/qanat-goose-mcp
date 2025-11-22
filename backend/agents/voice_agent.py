"""
Voice Agent - ElevenLabs Integration
Handles speech-to-text for voice commands
"""

import asyncio
import aiohttp
import io
import wave
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import structlog

try:
    import pyaudio
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    
logger = structlog.get_logger(__name__)

class VoiceAgent:
    """Voice input agent using ElevenLabs STT"""
    
    def __init__(self, config: Dict[str, Any], orchestrator=None):
        self.config = config
        self.elevenlabs_config = config.get("elevenlabs", {})
        self.api_key = self.elevenlabs_config.get("api_key")
        self.voice_id = self.elevenlabs_config.get("voice_id", "pNInz6obpgDQGcFmaJgB")
        self.orchestrator = orchestrator
        
        # Audio settings
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.channels = 1
        self.format = pyaudio.paInt16 if AUDIO_AVAILABLE else None
        
        # Voice command mappings
        self.command_mappings = {
            "refresh catalog": {
                "intent": "catalog.refresh",
                "params": {},
                "response": "Refreshing your catalog items..."
            },
            "update catalog": {
                "intent": "catalog.refresh", 
                "params": {},
                "response": "Updating catalog data..."
            },
            "reload items": {
                "intent": "catalog.refresh",
                "params": {},
                "response": "Reloading catalog items..."
            },
            "show orders": {
                "intent": "orders.view",
                "params": {},
                "response": "Loading your recent orders..."
            },
            "view orders": {
                "intent": "orders.view",
                "params": {},
                "response": "Displaying recent orders..."
            },
            "recent orders": {
                "intent": "orders.view",
                "params": {},
                "response": "Showing recent orders..."
            },
            "help": {
                "intent": "system.help",
                "params": {},
                "response": "Here are the available voice commands..."
            },
            "what can you do": {
                "intent": "system.help",
                "params": {},
                "response": "I can help you manage your Square catalog and orders..."
            }
        }
        
        self.session: Optional[aiohttp.ClientSession] = None
        self.audio_stream = None
        self.is_listening = False
        
        logger.info("VoiceAgent initialized", api_available=bool(self.api_key))
    
    async def initialize(self):
        """Initialize the voice agent"""
        if not self.api_key:
            logger.warning("ElevenLabs API key not provided, voice features disabled")
            return
        
        self.session = aiohttp.ClientSession(
            headers={
                "xi-api-key": self.api_key,
                "Content-Type": "application/json"
            }
        )
        
        logger.info("VoiceAgent initialized with ElevenLabs API")
    
    async def start_listening(self, callback: Optional[Callable] = None):
        """Start listening for voice commands"""
        if not AUDIO_AVAILABLE:
            logger.error("PyAudio not available, cannot start voice listening")
            return
        
        if not self.api_key:
            logger.error("No ElevenLabs API key, cannot start voice listening")
            return
        
        try:
            self.is_listening = True
            
            # Initialize audio
            audio = pyaudio.PyAudio()
            
            self.audio_stream = audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            logger.info("Voice listening started", sample_rate=self.sample_rate)
            
            # Listen for voice commands
            while self.is_listening:
                try:
                    # Record audio chunk (simplified for demo)
                    frames = []
                    for _ in range(0, int(self.sample_rate / self.chunk_size * 3)):  # 3 seconds
                        data = self.audio_stream.read(self.chunk_size)
                        frames.append(data)
                    
                    # Process the audio
                    audio_data = b''.join(frames)
                    text = await self._transcribe_audio(audio_data)
                    
                    if text:
                        result = await self.process_voice_command(text)
                        if callback:
                            await callback(result)
                    
                    # Brief pause
                    await asyncio.sleep(0.5)
                    
                except Exception as e:
                    logger.error("Error during voice listening", error=str(e))
                    await asyncio.sleep(1)
            
        except Exception as e:
            logger.error("Failed to start voice listening", error=str(e))
        finally:
            if self.audio_stream:
                self.audio_stream.stop_stream()
                self.audio_stream.close()
            
    async def stop_listening(self):
        """Stop listening for voice commands"""
        self.is_listening = False
        logger.info("Voice listening stopped")
    
    async def _transcribe_audio(self, audio_data: bytes) -> Optional[str]:
        """Transcribe audio using ElevenLabs STT (simulated for demo)"""
        try:
            # For demo purposes, we'll simulate STT responses
            # In real implementation, this would call ElevenLabs STT API
            
            logger.info("Transcribing audio", audio_size=len(audio_data))
            
            # Simulate API call delay
            await asyncio.sleep(0.1)
            
            # Mock transcription results for demo
            demo_transcriptions = [
                "refresh catalog",
                "show orders", 
                "help",
                None  # No speech detected
            ]
            
            # Return random demo result (in real app, this would be actual STT)
            import random
            result = random.choice(demo_transcriptions)
            
            if result:
                logger.info("Audio transcribed", text=result)
            
            return result
            
        except Exception as e:
            logger.error("Failed to transcribe audio", error=str(e))
            return None
    
    async def process_voice_command(self, text: str) -> Dict[str, Any]:
        """Process transcribed voice command"""
        try:
            text_lower = text.lower().strip()
            logger.info("Processing voice command", text=text_lower)
            
            # Find matching command
            command_info = None
            for trigger, info in self.command_mappings.items():
                if trigger in text_lower:
                    command_info = info
                    break
            
            if not command_info:
                logger.info("No matching voice command found", text=text_lower)
                return {
                    "status": "no_match",
                    "text": text,
                    "message": "Voice command not recognized"
                }
            
            # Execute command through orchestrator
            result = {
                "status": "success",
                "text": text,
                "intent": command_info["intent"],
                "params": command_info["params"],
                "response": command_info["response"]
            }
            
            if self.orchestrator:
                orchestrator_result = await self.orchestrator.process_intent(
                    command_info["intent"],
                    command_info["params"],
                    "voice"
                )
                result["orchestrator_result"] = orchestrator_result
            
            logger.info("Voice command processed", intent=command_info["intent"])
            
            # Speak response (TTS)
            await self._speak_response(command_info["response"])
            
            return result
            
        except Exception as e:
            logger.error("Failed to process voice command", text=text, error=str(e))
            return {
                "status": "error",
                "text": text,
                "error": str(e)
            }
    
    async def _speak_response(self, text: str):
        """Speak response using ElevenLabs TTS"""
        try:
            if not self.session or not self.api_key:
                logger.info("TTS response (simulated)", text=text)
                return
            
            # For demo, we'll just log the TTS response
            # In real implementation, this would call ElevenLabs TTS API
            logger.info("Speaking response", text=text)
            
            # Simulate TTS API call
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
            payload = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.75,
                    "similarity_boost": 0.75,
                    "style": 0.0,
                    "use_speaker_boost": True
                }
            }
            
            # Mock API response for demo
            await asyncio.sleep(0.1)  # Simulate API delay
            logger.info("TTS response generated", text_length=len(text))
            
        except Exception as e:
            logger.error("Failed to speak response", text=text, error=str(e))
    
    async def test_voice_command(self, text: str) -> Dict[str, Any]:
        """Test a voice command without audio input"""
        return await self.process_voice_command(text)
    
    def get_available_commands(self) -> Dict[str, str]:
        """Get list of available voice commands"""
        return {
            trigger: info["response"] 
            for trigger, info in self.command_mappings.items()
        }
    
    async def close(self):
        """Close the voice agent"""
        await self.stop_listening()
        
        if self.session:
            await self.session.close()
            
        logger.info("VoiceAgent closed")

# Utility function for testing
async def test_voice_agent():
    """Test the voice agent"""
    from .orchestrator import IntentOrchestrator
    
    config = {
        "elevenlabs": {
            "api_key": "test_key",
            "voice_id": "test_voice"
        }
    }
    
    orchestrator = IntentOrchestrator()
    agent = VoiceAgent(config, orchestrator)
    
    await agent.initialize()
    
    # Test voice commands
    test_commands = [
        "refresh catalog",
        "show orders", 
        "help",
        "unknown command"
    ]
    
    for command in test_commands:
        result = await agent.test_voice_command(command)
        print(f"Command: '{command}' -> {result['status']}")
    
    # Show available commands
    commands = agent.get_available_commands()
    print(f"Available commands: {list(commands.keys())}")
    
    await agent.close()

if __name__ == "__main__":
    asyncio.run(test_voice_agent())
