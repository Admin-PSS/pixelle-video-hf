"""
Video composition service - Assemble images + audio into MP4
"""

import os
import tempfile
from pathlib import Path
from PIL import Image
import numpy as np


class VideoService:
    """Handle video composition from images and audio"""
    
    @staticmethod
    def compose_video(image_paths, audio_path, output_path=None, images_per_second=0.5, fps=24):
        """
        Compose images + audio into an MP4 video
        
        Args:
            image_paths: List of image file paths
            audio_path: Path to MP3 audio file
            output_path: Where to save MP4 (default: temp directory)
            images_per_second: How many images to show per second (default: 0.5 = 2 seconds per image)
            fps: Video frame rate (default: 24)
        
        Returns:
            Path to generated MP4 file
        """
        try:
            from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
        except ImportError:
            raise ImportError("MoviePy not installed. Run: pip install moviepy")
        
        if not image_paths or len(image_paths) == 0:
            raise ValueError("No images provided")
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Calculate duration per image
        duration_per_image = 1.0 / images_per_second
        
        # Load audio to get total duration
        audio = AudioFileClip(audio_path)
        total_audio_duration = audio.duration
        
        # Create video clips from images
        clips = []
        current_time = 0
        
        for i, img_path in enumerate(image_paths):
            if not os.path.exists(img_path):
                raise FileNotFoundError(f"Image not found: {img_path}")
            
            # Calculate duration for this clip
            if i == len(image_paths) - 1:
                # Last image: extend to match audio duration
                duration = total_audio_duration - current_time
            else:
                duration = duration_per_image
            
            # Ensure minimum duration
            if duration < 0.1:
                duration = 0.1
            
            clip = ImageClip(img_path).set_duration(duration)
            clips.append(clip)
            current_time += duration
        
        # Concatenate all clips
        video = concatenate_videoclips(clips, method="chain")
        
        # Add audio (trim to video duration if needed)
        if audio.duration > video.duration:
            audio = audio.subclipped(0, video.duration)
        video = video.set_audio(audio)
        
        # Generate output path if not provided
        if output_path is None:
            temp_dir = tempfile.gettempdir()
            output_path = os.path.join(temp_dir, "pixelle_video_output.mp4")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        
        # Write video file
        video.write_videofile(
            output_path,
            fps=fps,
            verbose=False,
            logger=None,
            codec='libx264',
            audio_codec='aac'
        )
        
        # Close resources
        audio.close()
        video.close()
        
        return output_path
    
    @staticmethod
    def get_optimal_image_dimensions(image_paths):
        """
        Calculate optimal video dimensions based on images
        Returns the most common resolution
        """
        resolutions = {}
        for img_path in image_paths:
            try:
                img = Image.open(img_path)
                res = img.size
                resolutions[res] = resolutions.get(res, 0) + 1
            except Exception:
                pass
        
        if not resolutions:
            return (1280, 720)  # Default HD
        
        # Return most common resolution
        return max(resolutions.items(), key=lambda x: x[1])[0]
