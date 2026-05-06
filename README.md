# Pixelle-Video on Hugging Face Spaces

🎬 **Completely FREE AI Video Generation Platform**

## Features

✅ **AI Script Generation** - Creates engaging video scripts using Mistral 7B  
✅ **AI Image Generation** - Generates beautiful images using Stable Diffusion  
✅ **Text-to-Speech** - Converts scripts to audio using Edge-TTS  
✅ **100% Free** - All powered by Hugging Face infrastructure  
✅ **HF Pro Ready** - Takes advantage of your HF Pro account for faster inference  

## How It Works

```
Topic Input
    ↓
AI Script Generator (Mistral)
    ↓
Image Description Extractor
    ↓
AI Image Generator (Stable Diffusion)
    ↓
Text-to-Speech (Edge-TTS)
    ↓
Your Video Assets Ready!
```

## Quick Start

### 1. Get HF Token (2 min)

1. Go to: https://huggingface.co/settings/tokens
2. Click: "New token"
3. Fill: Name = `pixelle-video`, Type = "Read"
4. Copy the token

### 2. Add Secret to Space (1 min)

1. Open your Space: https://huggingface.co/spaces/YOUR_USERNAME/pixelle-video-hf
2. Click: Settings (⚙️) → Repository secrets
3. Add Secret:
   - **Key**: `HF_TOKEN`
   - **Value**: (paste your token from step 1)

### 3. Use It! (30 sec)

1. Visit your Space URL
2. Enter a topic
3. Click buttons to generate script, images, and audio
4. Done! ✨

## System Requirements

- HF Account (free or Pro)
- HF Token (free)
- That's it!

## Cost Breakdown

| Component | Cost |
|-----------|------|
| HF Spaces | $0 (included with HF Pro) |
| Mistral 7B Inference | $0 (HF Inference API) |
| Stable Diffusion Inference | $0 (HF Inference API) |
| Edge-TTS | $0 (local, free) |
| Storage | $0 (500GB on Space) |
| **TOTAL** | **$0/month** |

## Models Used

- **LLM**: Mistral-7B-Instruct (or Llama-2-7B)
- **Image**: Stable Diffusion 3 (or SDXL)
- **TTS**: Edge-TTS (Microsoft - free)

All hosted on Hugging Face! 🤗

## Advanced Usage

### Using With Your Own LLM API

If you have an LLM API (OpenAI, etc.), edit `config.py`:

```python
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")
```

Then add these to Space Secrets:
- `LLM_API_KEY`
- `LLM_BASE_URL`
- `LLM_MODEL`

### Extending the App

The code is modular and extensible:

- `services/llm.py` - Language model integration
- `services/image.py` - Image generation
- `services/tts.py` - Text-to-speech
- `app.py` - Streamlit UI

Add new features by creating new services!

## Troubleshooting

### "HF_TOKEN not set"
- Space needs HF_TOKEN in Secrets
- Make sure the secret name is exactly `HF_TOKEN`
- Space will auto-restart after adding secret

### "Model loading..."
- First run loads models (5-30 seconds)
- Subsequent runs are faster
- With HF Pro, loading is faster!

### "Inference timeout"
- HF Inference API can be slow on free tier
- With HF Pro, inference is much faster
- Or wait a few minutes and retry

## Performance Tips

- **Cache models locally** - First run loads, subsequent runs are instant
- **Use smaller sizes** - 512x512 images generate faster than 1024x1024
- **HF Pro advantage** - Get faster inference and higher rate limits
- **Batch requests** - Generate multiple at once

## Architecture

```
┌─────────────────────────────────────┐
│   Streamlit App (HF Spaces)         │
│   • User Interface                  │
│   • Session Management              │
└──────────────┬──────────────────────┘
               │
      ┌────────┼────────┐
      │        │        │
      ↓        ↓        ↓
   LLM API  Image API  Edge-TTS
 (HF Inference)      (Local)
```

## File Structure

```
pixelle-video-hf/
├── app.py              # Main Streamlit app
├── config.py           # Configuration
├── requirements.txt    # Dependencies
├── .streamlit/
│   └── config.toml     # Streamlit config
├── services/
│   ├── __init__.py
│   ├── llm.py         # Script generation
│   ├── image.py       # Image generation
│   └── tts.py         # Audio generation
└── data/              # Output storage
```

## Next Steps

After getting this working:

1. **Add Video Composition** - Combine images + audio into video
2. **Add History** - Save previous generations
3. **Add Templates** - Different video styles
4. **Add Batch Processing** - Generate multiple videos
5. **Add Export** - Download in different formats

See `HF_SPACES_ZERO_COST.md` for advanced features!

## Support & Links

- 📘 Streamlit Docs: https://docs.streamlit.io
- 🤗 HF Docs: https://huggingface.co/docs
- 📖 HF Spaces Guide: https://huggingface.co/docs/hub/spaces
- 🐛 Issues: Open an issue on GitHub

## License

Apache 2.0 - See LICENSE file

## Credit

Built by AIDC-AI Team  
Powered by Hugging Face 🤗

---

**Enjoy creating AI videos for free!** 🎬✨
