import streamlit as st
import google.generativeai as genai
import pyttsx3
from PIL import Image
from dotenv import load_dotenv
import os
load_dotenv()  # Load environment variables from .env file

# Retrieve the API key from the environment variable
api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found! Set the environment variable GENAI_API_KEY.")

genai.configure(api_key=api_key)


class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.8)

    def speak(self, text):
        """Convert text to speech"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            st.error(f"Text-to-Speech error: {e}")

class VisualAssistant:
    def __init__(self):
        self.vision_model = genai.GenerativeModel('models/gemini-1.5-flash')
        self.tts = TextToSpeech()
        
    def describe_scene(self, image):
        """Generate detailed scene description"""
        try:
            response = self.vision_model.generate_content([
                "Provide a comprehensive and detailed description of the scene. "
                "Focus on key elements, colors, objects, and spatial relationships. "
                "Describe the scene as if explaining it to a visually impaired person.",
                image
            ])
            return response.text
        except Exception as e:
            return f"Error in scene description: {str(e)}"
    
    def extract_text(self, image):
        """Extract text from image using Gemini"""
        try:
            response = self.vision_model.generate_content([
                "Extract all readable text from this image. Provide the text exactly as it appears.",
                image
            ])
            return response.text
        except Exception as e:
            return f"Text extraction error: {str(e)}"
    
    def detect_objects(self, image):
        """Detect and describe objects in the image"""
        try:
            response = self.vision_model.generate_content([
                "Identify and list all distinct objects in this image. "
                "For each object, provide its location and potential significance. "
                "Prioritize objects that might impact navigation or safety.",
                image
            ])
            return response.text
        except Exception as e:
            return f"Object detection error: {str(e)}"

def main():
    st.title("🌟 AI Visual Assistant for Visually Impaired")
    st.markdown("Upload an image to get comprehensive visual assistance")
    
    if "scene_desc" not in st.session_state:
        st.session_state.scene_desc = ""
    if "text_content" not in st.session_state:
        st.session_state.text_content = ""
    if "object_info" not in st.session_state:
        st.session_state.object_info = ""

    uploaded_file = st.file_uploader(
        "Choose an image", 
        type=['jpg', 'jpeg', 'png'],
        help="Upload an image for scene analysis"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        
        assistant = VisualAssistant()
        
        features = st.multiselect(
            "Select Assistance Features",
            [
                "Scene Understanding", 
                "Text Extraction", 
                "Object Detection"
            ]
        )
        
        if st.button("Get Assistance"):
            if "Scene Understanding" in features:
                st.session_state.scene_desc = assistant.describe_scene(image)
            if "Text Extraction" in features:
                st.session_state.text_content = assistant.extract_text(image)
            if "Object Detection" in features:
                st.session_state.object_info = assistant.detect_objects(image)
        
        if st.session_state.scene_desc:
            with st.expander("Scene Description"):
                st.write(st.session_state.scene_desc)
                if st.button("Read Scene Description"):
                    assistant.tts.speak(st.session_state.scene_desc)
        
        if st.session_state.text_content:
            with st.expander("Extracted Text"):
                st.write(st.session_state.text_content)
                if st.button("Read Extracted Text"):
                    assistant.tts.speak(st.session_state.text_content)
        
        if st.session_state.object_info:
            with st.expander("Object Analysis"):
                st.write(st.session_state.object_info)
                if st.button("Read Object Analysis"):
                    assistant.tts.speak(st.session_state.object_info)

if __name__ == "__main__":
    main()
