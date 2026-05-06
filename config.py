# Configuration - Load from environment variables
import os

class Config:
    """Configuration loaded from environment variables"""
    
    # HF Token (required)
    HF_TOKEN = os.getenv("HF_TOKEN", "")
    
    # LLM Configuration
    LLM_API_KEY = os.getenv("LLM_API_KEY", "")
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")
    
    # HF Models (defaults provided)
    HF_LLM_MODEL = os.getenv("HF_LLM_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")
    HF_IMAGE_MODEL = os.getenv("HF_IMAGE_MODEL", "stabilityai/stable-diffusion-3-medium")
    
    # Storage paths
    DATA_DIR = "/data" if os.path.exists("/data") else "./data"
    TEMP_DIR = "/tmp" if os.path.exists("/tmp") else "./temp"
    
    # Limits
    MAX_OUTPUT_SIZE = 500 * 1024 * 1024  # 500MB
    MAX_VIDEO_LENGTH = 60  # seconds
    
    # UI Settings
    PAGE_SIZE = 12
    CACHE_TTL = 3600  # 1 hour
