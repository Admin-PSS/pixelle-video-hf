"""LLM Service - Script and content generation"""
import asyncio
from huggingface_hub import InferenceClient
from config import Config
import streamlit as st

class LLMService:
    """Generate scripts using HF Inference API"""
    
    def __init__(self, hf_token: str):
        self.client = InferenceClient(token=hf_token)
    
    def generate_script(self, topic: str, model: str = None) -> str:
        """Generate video script from topic"""
        if model is None:
            model = Config.HF_LLM_MODEL
        
        prompt = f"""Create a short engaging video script (250-300 words) about: {topic}

Format as clear, concise scenes:
- Scene 1: [Description and narration]
- Scene 2: [Description and narration]
- Scene 3: [Description and narration]

Make it engaging, clear, and suitable for a video."""
        
        try:
            response = self.client.text_generation(
                prompt,
                model=model,
                max_new_tokens=350,
                temperature=0.7,
                top_p=0.95,
            )
            return response
        except Exception as e:
            raise Exception(f"Script generation failed: {str(e)}")
    
    def generate_image_descriptions(self, script: str, model: str = None) -> list[str]:
        """Extract image descriptions from script"""
        if model is None:
            model = Config.HF_LLM_MODEL
        
        prompt = f"""From this video script, extract 3 short image descriptions (one per line).
Make them vivid, descriptive, and suitable for AI image generation.

Script:
{script}

Return only the 3 image descriptions, one per line:"""
        
        try:
            response = self.client.text_generation(
                prompt,
                model=model,
                max_new_tokens=200,
                temperature=0.7,
            )
            
            # Split into lines and clean
            descriptions = [line.strip() for line in response.split('\n') if line.strip()]
            return descriptions[:3]  # Take first 3
        except Exception as e:
            raise Exception(f"Image description generation failed: {str(e)}")
