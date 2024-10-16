import os
import streamlit as st
from dotenv import load_dotenv
import requests
import io
from PIL import Image
import logging
import traceback
from datetime import datetime
import time
import base64
import webbrowser

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def set_page_config():
    try:
        st.set_page_config(page_title="AI Image Generator", page_icon="🖼️", layout="wide", menu_items=None)
        st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
            font-family: Arial, sans-serif;
        }
        .main-title {
            color: #4a4a4a;
            text-align: center;
            margin-bottom: 30px;
        }
        .footer {
            text-align: center;
            padding: 20px 0;
            font-size: 14px;
            color: #666;
            border-top: 1px solid #eee;
            margin-top: 40px;
        }
        .error-message {
            color: #721c24;
            background-color: #f8d7da;
            border-color: #f5c6cb;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
        }
        </style>
        """, unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error in set_page_config: {str(e)}")
        st.error("An error occurred while setting up the page. Please try refreshing.")

def generate_image(prompt):
    try:
        API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
        headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}

        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        response.raise_for_status()

        return response.content
    except requests.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        raise Exception("Failed to generate image. Please try again later.")
    except Exception as e:
        logger.error(f"Error in generate_image: {str(e)}")
        raise Exception("An unexpected error occurred while generating the image.")

def auto_download_image(img_data):
    try:
        # Convert image data to base64
        b64 = base64.b64encode(img_data).decode()
        
        # Create the download link with automatic download trigger
        js = f'''
            <script>
                function downloadImage() {{
                    const a = document.createElement('a');
                    a.href = "data:image/png;base64,{b64}";
                    a.download = "generated_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png";
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                }}
                downloadImage();
            </script>
        '''
        st.components.v1.html(js, height=0)
    except Exception as e:
        logger.error(f"Error in auto_download_image: {str(e)}")
        raise Exception("Failed to initiate automatic download.")

def create_streamlit_app():
    try:
        set_page_config()
        
        st.markdown("<h1 class='main-title'>🖼️ AI Image Generator by Ai Craft Alchemy</h1>", unsafe_allow_html=True)

        prompt = st.text_area("Enter your image prompt:", height=100)
        
        if st.button("Generate Image"):
            if prompt:
                logger.info(f"User prompt: {prompt}")
                
                try:
                    progress_placeholder = st.empty()
                    start_time = time.time()
                    engaging_messages = [
                        "Initializing the creative process...",
                        "Gathering inspiration from the digital ether...",
                        "Mixing colors in the virtual palette...",
                        "Bringing your imagination to life...",
                        "Adding final touches to your masterpiece..."
                    ]
                    
                    with st.spinner("Generating image..."):
                        for i, message in enumerate(engaging_messages):
                            if time.time() - start_time > i * 5:
                                progress_placeholder.text(message)
                        
                        image_bytes = generate_image(prompt)
                        image = Image.open(io.BytesIO(image_bytes))
                        st.image(image, caption="Generated Image", use_column_width=True)
                        
                        # Trigger automatic download
                        auto_download_image(image_bytes)
                        
                        logger.info(f"Image successfully generated and auto-downloaded for prompt: {prompt}")
                        st.success("Image generated and downloaded successfully!")
                except Exception as e:
                    st.markdown(f"<div class='error-message'>{str(e)}</div>", unsafe_allow_html=True)
            else:
                st.warning("Please enter a prompt for image generation.")
                logger.warning("User attempted to generate an image without entering a prompt")

        # Footer
        st.markdown("""
        <div class='footer'>
        Developed by <a href='https://aicraftalchemy.github.io'>Ai Craft Alchemy</a><br>
        Connect with us: <a href='tel:+917661081043'>+91 7661081043</a>
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        logger.error(f"Unhandled exception in create_streamlit_app: {str(e)}")
        logger.error(traceback.format_exc())
        st.error("An unexpected error occurred. Please try refreshing the page or contact support if the problem persists.")

if __name__ == "__main__":
    try:
        create_streamlit_app()
    except Exception as e:
        logger.critical(f"Critical error in main app execution: {str(e)}")
        logger.critical(traceback.format_exc())
        st.error("A critical error occurred. Please try again later or contact support.")
