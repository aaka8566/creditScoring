"""
Hugging Face Space Entry Point
This file is required by Hugging Face Spaces
"""
from enhanced_main import app
import uvicorn

if __name__ == "__main__":
    # Hugging Face Spaces uses port 7860 by default
    uvicorn.run(app, host="0.0.0.0", port=7860)

