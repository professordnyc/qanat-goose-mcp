"""
Environment configuration loader for Qanat
Handles .env file loading and validation
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import structlog

logger = structlog.get_logger(__name__)

class EnvironmentLoader:
    """Load and validate environment configuration"""
    
    def __init__(self, env_file: Optional[str] = None):
        """Initialize environment loader
        
        Args:
            env_file: Path to .env file (default: .env in project root)
        """
        self.project_root = Path(__file__).parent.parent.parent
        self.env_file = env_file or self.project_root / ".env"
        
    def load(self) -> Dict[str, Any]:
        """Load environment variables and return configuration dict"""
        
        # Load .env file if it exists
        if self.env_file.exists():
            load_dotenv(self.env_file)
            logger.info("Loaded environment file", path=str(self.env_file))
        else:
            logger.warning("No .env file found", expected_path=str(self.env_file))
        
        config = {
            # Square API Configuration
            "square": {
                "api_key": os.getenv("SQUARE_API_KEY"),
                "environment": os.getenv("SQUARE_ENVIRONMENT", "sandbox"),
                "application_id": os.getenv("SQUARE_APPLICATION_ID")
            },
            
            # ElevenLabs Configuration
            "elevenlabs": {
                "api_key": os.getenv("ELEVENLABS_API_KEY"),
                "voice_id": os.getenv("ELEVENLABS_VOICE_ID", "pNInz6obpgDQGcFmaJgB")
            },
            
            # MediaPipe Configuration
            "mediapipe": {
                "model_path": os.getenv("MEDIAPIPE_MODEL_PATH", "./models/"),
                "confidence_threshold": float(os.getenv("MEDIAPIPE_CONFIDENCE_THRESHOLD", "0.7"))
            },
            
            # MCP Server Configuration  
            "mcp_server": {
                "host": os.getenv("MCP_SERVER_HOST", "localhost"),
                "port": int(os.getenv("MCP_SERVER_PORT", "3001")),
                "debug": os.getenv("MCP_SERVER_DEBUG", "false").lower() == "true"
            },
            
            # Logging Configuration
            "logging": {
                "level": os.getenv("LOG_LEVEL", "INFO"),
                "file": os.getenv("LOG_FILE", "logs/qanat.log")
            }
        }
        
        # Validate required configuration
        self._validate_config(config)
        
        return config
    
    def _validate_config(self, config: Dict[str, Any]) -> None:
        """Validate that required configuration is present"""
        
        required_fields = [
            ("square.api_key", "SQUARE_API_KEY"),
            ("elevenlabs.api_key", "ELEVENLABS_API_KEY") 
        ]
        
        missing_fields = []
        
        for field_path, env_var in required_fields:
            keys = field_path.split(".")
            value = config
            
            for key in keys:
                value = value.get(key)
                if value is None:
                    break
                    
            if not value:
                missing_fields.append(env_var)
        
        if missing_fields:
            logger.error(
                "Missing required environment variables",
                missing=missing_fields,
                env_file=str(self.env_file)
            )
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_fields)}. "
                f"Please check your .env file at {self.env_file}"
            )
        
        logger.info("Environment configuration validated successfully")

# Global configuration instance
_config_instance = None

def get_config() -> Dict[str, Any]:
    """Get the global configuration instance"""
    global _config_instance
    
    if _config_instance is None:
        loader = EnvironmentLoader()
        _config_instance = loader.load()
    
    return _config_instance

def reload_config(env_file: Optional[str] = None) -> Dict[str, Any]:
    """Reload configuration from environment file"""
    global _config_instance
    
    loader = EnvironmentLoader(env_file)
    _config_instance = loader.load()
    
    return _config_instance
