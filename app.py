"""
Pixelle-Video - Free AI Video Generation on Hugging Face
Powered by HF Inference API + Edge-TTS + Streamlit
"""

import streamlit as st
import os
import tempfile
from config import Config
from services.llm import LLMService
from services.tts import TTSService
from services.image import ImageService
from services.video import VideoService
from PIL import Image

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Pixelle-Video - FREE",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    .main {
        max-width: 1200px;
        margin: 0 auto;
    }
    .step-header {
        border-left: 4px solid #FF6B6B;
        padding-left: 15px;
        margin: 20px 0 10px 0;
    }
    .success-box {
        background-color: #D4EDDA;
        border: 1px solid #C3E6CB;
        color: #155724;
        padding: 12px;
        border-radius: 4px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #D1ECF1;
        border: 1px solid #BEE5EB;
        color: #0C5460;
        padding: 12px;
        border-radius: 4px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.title("🎬 Pixelle-Video")
st.markdown("### AI-Powered Video Generation on Hugging Face Spaces")
st.markdown("""
**Completely FREE. No subscriptions. No costs.**
- 📝 AI Script Generation (Mistral 7B)
- 🖼️ AI Image Generation (Stable Diffusion)
- 🔊 Text-to-Speech (Edge-TTS)
- 🎬 Video Composition (MoviePy)
- All powered by Hugging Face
""")

# ==================== CHECK CONFIGURATION ====================
hf_token = os.getenv("HF_TOKEN", "")

if not hf_token:
    st.error("""
    ❌ **HF_TOKEN not configured!**
    
    To use this app:
    1. Get your HF token: https://huggingface.co/settings/tokens
    2. Add it to Space Secrets as `HF_TOKEN`
    3. The Space will auto-restart
    """)
    st.stop()

# ==================== INITIALIZE SERVICES ====================
@st.cache_resource
def init_services():
    """Initialize all services (runs once per session)"""
    return {
        "llm": LLMService(hf_token),
        "tts": TTSService(),
        "image": ImageService(hf_token),
        "video": VideoService(),
    }

services = init_services()

st.markdown("---")

# ==================== SESSION STATE ====================
if "script" not in st.session_state:
    st.session_state.script = None
if "images" not in st.session_state:
    st.session_state.images = None
if "audio_path" not in st.session_state:
    st.session_state.audio_path = None
if "video_prompts" not in st.session_state:
    st.session_state.video_prompts = None
if "video_path" not in st.session_state:
    st.session_state.video_path = None
if "uploaded_images" not in st.session_state:
    st.session_state.uploaded_images = None
if "mode" not in st.session_state:
    st.session_state.mode = "text-to-video"

# ==================== MODE SELECTION ====================
st.markdown('<h2 class="step-header">🎬 Choose Your Mode</h2>', unsafe_allow_html=True)

mode = st.radio(
    "How do you want to create your video?",
    ["Text-to-Video (Generate everything)", "Image-to-Video (Use your own images)"],
    index=0 if st.session_state.mode == "text-to-video" else 1,
    horizontal=True,
    help="Text-to-Video: Generate script → images → audio → video. Image-to-Video: Upload images + create audio → video"
)

st.session_state.mode = "text-to-video" if mode == "Text-to-Video (Generate everything)" else "image-to-video"

st.markdown("---")

# ==================== TEXT-TO-VIDEO MODE ====================
if st.session_state.mode == "text-to-video":
    
    # STEP 1: GENERATE SCRIPT
    st.markdown('<h2 class="step-header">📝 Step 1: Generate Script</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        topic = st.text_area(
            "What should your video be about?",
            value="A beautiful sunset over the ocean",
            height=100,
            placeholder="Enter a topic or description for your video...",
            key="topic_input"
        )
    
    with col2:
        llm_model = st.selectbox(
            "LLM Model:",
            [
                ("Mistral 7B (Fast)", "mistralai/Mistral-7B-Instruct-v0.2"),
                ("Llama 2 7B", "meta-llama/Llama-2-7b-chat-hf"),
            ],
            index=0,
            help="Choose the language model for script generation"
        )
    
    if st.button("✨ Generate Script", type="primary", use_container_width=True):
        with st.spinner("⏳ Generating script using HF Inference API..."):
            try:
                st.session_state.script = services["llm"].generate_script(
                    topic,
                    model=llm_model[1]
                )
                st.markdown('<div class="success-box">✅ Script generated successfully!</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state.script = None
    
    # Display generated script
    if st.session_state.script:
        st.markdown('<div class="info-box">📄 Generated Script:</div>', unsafe_allow_html=True)
        st.text_area("", value=st.session_state.script, height=200, disabled=True)
    
    st.markdown("---")
    
    # STEP 2: GENERATE IMAGES
    st.markdown('<h2 class="step-header">🖼️ Step 2: Generate Images</h2>', unsafe_allow_html=True)
    
    if st.session_state.script is None:
        st.info("💡 Generate a script first!")
    else:
        image_model = st.selectbox(
            "Image Model:",
            [
                ("Stable Diffusion 3 (Best)", "stabilityai/stable-diffusion-3-medium"),
                ("Stable Diffusion XL", "stabilityai/stable-diffusion-xl-base-1.0"),
            ],
            index=0,
            help="Choose the image generation model"
        )
        
        if st.button("📸 Generate Images from Script", type="primary", use_container_width=True):
            with st.spinner("🎨 Generating images... (this may take 30-60 seconds)"):
                try:
                    # Extract image descriptions from script
                    st.info("📝 Extracting image descriptions...")
                    prompts = services["llm"].generate_image_descriptions(st.session_state.script)
                    st.session_state.video_prompts = prompts
                    
                    # Generate images
                    st.info("🖼️ Generating images...")
                    images = services["image"].generate_images(prompts, model=image_model[1])
                    st.session_state.images = images
                    
                    st.markdown('<div class="success-box">✅ Images generated successfully!</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.session_state.images = None
    
    # Display generated images
    if st.session_state.images:
        st.markdown('<div class="info-box">🎨 Generated Images:</div>', unsafe_allow_html=True)
        cols = st.columns(len(st.session_state.images))
        for i, (col, img) in enumerate(zip(cols, st.session_state.images)):
            with col:
                st.image(img)
                if st.session_state.video_prompts and i < len(st.session_state.video_prompts):
                    st.caption(st.session_state.video_prompts[i])
    
    st.markdown("---")
    
    # STEP 3: GENERATE AUDIO
    st.markdown('<h2 class="step-header">🔊 Step 3: Generate Audio</h2>', unsafe_allow_html=True)
    
    if st.session_state.script is None:
        st.info("💡 Generate a script first!")
    else:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            voice = st.selectbox(
                "Voice:",
                list(TTSService.get_voice_options().keys()),
                index=0,
                help="Choose the voice for text-to-speech"
            )
        
        with col2:
            tts_speed = st.slider(
                "Speed:",
                min_value=0.5,
                max_value=2.0,
                value=1.0,
                step=0.1,
                help="Adjust speech speed"
            )
        
        if st.button("🎤 Generate Audio", type="primary", use_container_width=True):
            with st.spinner("🔊 Generating audio (Edge-TTS)..."):
                try:
                    voice_id = TTSService.get_voice_options()[voice]
                    audio_path = services["tts"].generate_tts(
                        st.session_state.script,
                        voice=voice_id,
                        speed=tts_speed
                    )
                    st.session_state.audio_path = audio_path
                    st.markdown('<div class="success-box">✅ Audio generated successfully!</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.session_state.audio_path = None
    
    # Display audio player
    if st.session_state.audio_path:
        st.markdown('<div class="info-box">🎵 Generated Audio:</div>', unsafe_allow_html=True)
        with open(st.session_state.audio_path, "rb") as f:
            st.audio(f, format="audio/mp3")
    
    st.markdown("---")

else:  # IMAGE-TO-VIDEO MODE
    st.markdown('<h2 class="step-header">🖼️ Step 1: Upload Your Images</h2>', unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Upload images for your video (PNG, JPG, JPEG)",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        help="Upload multiple images in the order you want them to appear"
    )
    
    if uploaded_files:
        # Save uploaded images to temp directory
        temp_dir = tempfile.gettempdir()
        image_paths = []
        
        st.markdown('<div class="info-box">📸 Your Uploaded Images:</div>', unsafe_allow_html=True)
        cols = st.columns(min(len(uploaded_files), 3))
        
        for i, uploaded_file in enumerate(uploaded_files):
            # Save to temp
            temp_path = os.path.join(temp_dir, f"upload_{i}_{uploaded_file.name}")
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            image_paths.append(temp_path)
            
            # Display thumbnail
            col_idx = i % 3
            with cols[col_idx]:
                st.image(Image.open(temp_path), use_column_width=True)
                st.caption(f"Image {i+1}")
        
        st.session_state.uploaded_images = image_paths
    
    st.markdown("---")
    
    st.markdown('<h2 class="step-header">🎤 Step 2: Create Audio</h2>', unsafe_allow_html=True)
    
    if st.session_state.uploaded_images is None or len(st.session_state.uploaded_images) == 0:
        st.info("💡 Upload images first!")
    else:
        # Option to upload existing audio or generate new
        audio_mode = st.radio(
            "Audio source:",
            ["Generate new audio (TTS)", "Upload existing audio"],
            horizontal=True,
            help="Generate new audio from text or upload your own MP3"
        )
        
        if audio_mode == "Generate new audio (TTS)":
            col1, col2 = st.columns([2, 1])
            
            with col1:
                audio_text = st.text_area(
                    "Enter the text to convert to speech:",
                    value="Here is a beautiful collection of images.",
                    height=80,
                    placeholder="Enter the script for your audio..."
                )
            
            with col2:
                voice = st.selectbox(
                    "Voice:",
                    list(TTSService.get_voice_options().keys()),
                    index=0,
                    help="Choose the voice for text-to-speech"
                )
            
            if st.button("🎤 Generate Audio", type="primary", use_container_width=True, key="gen_audio_img"):
                with st.spinner("🔊 Generating audio (Edge-TTS)..."):
                    try:
                        voice_id = TTSService.get_voice_options()[voice]
                        audio_path = services["tts"].generate_tts(audio_text, voice=voice_id, speed=1.0)
                        st.session_state.audio_path = audio_path
                        st.markdown('<div class="success-box">✅ Audio generated successfully!</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        st.session_state.audio_path = None
        
        else:  # Upload existing audio
            uploaded_audio = st.file_uploader(
                "Upload your audio file (MP3, WAV, OGG)",
                type=["mp3", "wav", "ogg"],
                help="Upload an existing audio file"
            )
            
            if uploaded_audio:
                temp_audio_path = os.path.join(tempfile.gettempdir(), uploaded_audio.name)
                with open(temp_audio_path, "wb") as f:
                    f.write(uploaded_audio.getbuffer())
                st.session_state.audio_path = temp_audio_path
                st.markdown('<div class="success-box">✅ Audio uploaded successfully!</div>', unsafe_allow_html=True)
        
        # Display audio player
        if st.session_state.audio_path:
            st.markdown('<div class="info-box">🎵 Your Audio:</div>', unsafe_allow_html=True)
            with open(st.session_state.audio_path, "rb") as f:
                st.audio(f, format="audio/mp3")
    
    st.markdown("---")

# ==================== STEP 4: COMPOSE VIDEO (Both modes) ====================
st.markdown('<h2 class="step-header">🎬 Step 4: Compose Video</h2>', unsafe_allow_html=True)

# Determine if we have all required components
has_images = st.session_state.images is not None or st.session_state.uploaded_images is not None
has_audio = st.session_state.audio_path is not None

if not has_images or not has_audio:
    st.info("💡 Complete the steps above first!")
else:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        images_per_second = st.slider(
            "Images per second:",
            min_value=0.25,
            max_value=2.0,
            value=0.5,
            step=0.25,
            help="How many images to show per second (lower = slower transitions)"
        )
    
    with col2:
        fps = st.selectbox(
            "Video quality (FPS):",
            [24, 30, 60],
            index=0,
            help="24 FPS = standard, 30 FPS = smooth, 60 FPS = very smooth"
        )
    
    if st.button("🎥 Create Video", type="primary", use_container_width=True):
        with st.spinner("🎬 Composing video... (this may take 1-2 minutes)"):
            try:
                # Get image paths
                image_paths = st.session_state.images if st.session_state.images else st.session_state.uploaded_images
                
                # Compose video
                video_output_path = os.path.join(tempfile.gettempdir(), "pixelle_video_final.mp4")
                result = services["video"].compose_video(
                    image_paths,
                    st.session_state.audio_path,
                    output_path=video_output_path,
                    images_per_second=images_per_second,
                    fps=fps
                )
                
                st.session_state.video_path = result
                st.markdown('<div class="success-box">✅ Video created successfully!</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state.video_path = None

# Display video player and download
if st.session_state.video_path:
    st.markdown('<div class="info-box">🎥 Your Video:</div>', unsafe_allow_html=True)
    st.video(st.session_state.video_path)
    
    # Download button
    with open(st.session_state.video_path, "rb") as f:
        st.download_button(
            label="📥 Download Video",
            data=f,
            file_name="pixelle_video.mp4",
            mime="video/mp4",
            use_container_width=True
        )

st.markdown("---")

# ==================== SUMMARY ====================
st.markdown('<h2 class="step-header">✨ Summary</h2>', unsafe_allow_html=True)

if st.session_state.mode == "text-to-video":
    summary_cols = st.columns(4)
    
    with summary_cols[0]:
        status = "✅ Done" if st.session_state.script else "⏳ Pending"
        st.metric("Script", status)
    
    with summary_cols[1]:
        status = "✅ Done" if st.session_state.images else "⏳ Pending"
        st.metric("Images", status)
    
    with summary_cols[2]:
        status = "✅ Done" if st.session_state.audio_path else "⏳ Pending"
        st.metric("Audio", status)
    
    with summary_cols[3]:
        status = "✅ Done" if st.session_state.video_path else "⏳ Pending"
        st.metric("Video", status)
else:  # image-to-video mode
    summary_cols = st.columns(3)
    
    with summary_cols[0]:
        status = "✅ Done" if st.session_state.uploaded_images else "⏳ Pending"
        st.metric("Images", status)
    
    with summary_cols[1]:
        status = "✅ Done" if st.session_state.audio_path else "⏳ Pending"
        st.metric("Audio", status)
    
    with summary_cols[2]:
        status = "✅ Done" if st.session_state.video_path else "⏳ Pending"
        st.metric("Video", status)

st.markdown("---")

# ==================== FOOTER ====================
st.markdown("""
<div style='text-align: center; color: #666; font-size: 12px; margin-top: 30px;'>
    <p>🚀 <strong>Pixelle-Video</strong> by AIDC-AI</p>
    <p>Powered by 🤗 Hugging Face Spaces | Mistral 7B | Stable Diffusion | Edge-TTS | MoviePy</p>
    <p><a href="https://github.com/AIDC-AI/Pixelle-Video">GitHub</a> | 
       <a href="https://huggingface.co/spaces">Spaces</a> | 
       <a href="https://huggingface.co">Hugging Face</a></p>
    <p style='margin-top: 10px;'>Cost: <strong>$0/month</strong> - Completely Free!</p>
    <p><a href="#">📚 See VIDEO_FEATURES.md for detailed documentation</a></p>
</div>
""", unsafe_allow_html=True)
