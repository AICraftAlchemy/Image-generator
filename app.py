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
import uuid

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
        .auto-download-link {
            display: none !important;
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

def get_image_download_link(img, filename):
    try:
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        download_id = f"download-{uuid.uuid4()}"
        
        # Creating HTML with both visible and auto-download links
        html = f"""
            <div>
                <a href="data:file/png;base64,{img_str}" 
                   class="auto-download-link"
                   id="{download_id}"
                   download="{filename}">Download Image</a>
                <script>
                    (function() {{
                        const downloadLink = document.getElementById('{download_id}');
                        if (downloadLink) {{
                            downloadLink.click();
                            console.log("Auto download triggered");
                        }} else {{
                            console.error("Download link not found");
                        }}
                    }})();
                </script>
            </div>
        """
        return html
    except Exception as e:
        logger.error(f"Error creating download link: {str(e)}")
        return f"<div class='error-message'>Error preparing download: {str(e)}</div>"

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
                        
                        # Generate unique filename
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        file_name = f"generated_image_{timestamp}.png"
                        
                        # Inject download component and auto-trigger script
                        st.markdown(get_image_download_link(image, file_name), unsafe_allow_html=True)
                        
                        # Manual download button
                        buffered = io.BytesIO()
                        image.save(buffered, format="PNG")
                        st.download_button(
                            label="Click to download manually",
                            data=buffered.getvalue(),
                            file_name=file_name,
                            mime="image/png"
                        )
                        
                        logger.info(f"Image generated successfully for prompt: {prompt}")
                        st.success("Image generated successfully! Download should start automatically.")
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
