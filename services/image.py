"""Image Service - Image generation via HF Inference API"""
from huggingface_hub import InferenceClient
from config import Config
from PIL import Image
from io import BytesIO
import streamlit as st

class ImageService:
    """Generate images using HF Inference API"""
    
    def __init__(self, hf_token: str):
        self.client = InferenceClient(token=hf_token)
    
    def generate_image(self, prompt: str, model: str = None) -> Image.Image:
        """Generate single image from prompt"""
        if model is None:
            model = Config.HF_IMAGE_MODEL
        
        try:
            image = self.client.text_to_image(
                prompt,
                model=model,
                negative_prompt="low quality, blurry, distorted",
                height=512,
                width=512,
            )
            return image
        except Exception as e:
            raise Exception(f"Image generation failed: {str(e)}")
    
    def generate_images(self, prompts: list[str], model: str = None) -> list[Image.Image]:
        """Generate multiple images"""
        if model is None:
            model = Config.HF_IMAGE_MODEL
        
        images = []
        for prompt in prompts:
            try:
                image = self.generate_image(prompt, model)
                images.append(image)
            except Exception as e:
                st.warning(f"Failed to generate image for '{prompt}': {str(e)}")
                continue
        
        return images
    
    def save_images(self, images: list[Image.Image], base_name: str = "scene") -> list[str]:
        """Save images to disk"""
        saved_paths = []
        for i, image in enumerate(images):
            path = f"{Config.DATA_DIR}/{base_name}_{i}.png"
            image.save(path)
            saved_paths.append(path)
        return saved_paths
