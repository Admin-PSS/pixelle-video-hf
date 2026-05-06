"""TTS Service - Text-to-Speech generation"""
import edge_tts
import asyncio
from config import Config
import streamlit as st

class TTSService:
    """Generate speech using Edge-TTS (free, local)"""
    
    VOICES = {
        "English (Female)": "en-US-AriaNeural",
        "English (Male)": "en-US-GuyNeural",
        "Chinese (Female)": "zh-CN-XiaoxiaoNeural",
        "Spanish (Female)": "es-ES-ElviraNeural",
        "French (Female)": "fr-FR-DeniseNeural",
        "German (Female)": "de-DE-KatjaNeural",
    }
    
    def __init__(self):
        self.output_dir = Config.TEMP_DIR
    
    async def generate_tts_async(self, text: str, voice: str = "en-US-AriaNeural", 
                                  speed: float = 1.0) -> str:
        """Generate TTS audio (async)"""
        output_file = f"{self.output_dir}/audio.mp3"
        
        # Adjust rate for speed
        rate = f"+{int((speed-1)*100)}%" if speed != 1.0 else "+0%"
        
        try:
            communicate = edge_tts.Communicate(
                text=text,
                voice=voice,
                rate=rate
            )
            await communicate.save(output_file)
            return output_file
        except Exception as e:
            raise Exception(f"TTS generation failed: {str(e)}")
    
    def generate_tts(self, text: str, voice: str = "en-US-AriaNeural", 
                     speed: float = 1.0) -> str:
        """Generate TTS audio (sync wrapper)"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            self.generate_tts_async(text, voice, speed)
        )
        return result
    
    @staticmethod
    def get_voice_options() -> dict:
        """Get available voices"""
        return TTSService.VOICES
