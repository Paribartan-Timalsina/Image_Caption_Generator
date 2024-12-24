import streamlit as st
import requests
from PIL import Image
import io
from dotenv import load_dotenv
import os

load_dotenv('.env')

# Hugging Face API details
API_URL_custom: str = os.getenv("API_URL_custom")
API_URL: str = os.getenv("API_URL")
TOKEN: str = os.getenv("HUGGING_FACE_TOKEN")
headers = {"Authorization": f"{TOKEN}"}

import io
import base64
import requests

def query_custom_api(image):
    """Send image to Hugging Face model and get the generated caption."""
    # Convert image to bytes
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")  # Ensure the format is JPEG
    buffered.seek(0)
    
    # Convert buffered image to a base64 string
    image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Prepare the data to send (if your API supports base64 input directly)
    data = {'image': image_base64}
    
    # Send POST request with the image base64 string
    response = requests.post(API_URL_custom, headers=headers, json=data)
    
    return response.json()

def query_huggingface_api(image):
    """Send image to Hugging Face model and get the generated caption."""
    # Convert image to bytes
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")  # Ensure the format is JPEG
    buffered.seek(0)
    
    # Convert buffered image to a base64 string
    image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Prepare the data to send (if your API supports base64 input directly)
    data = {'image': image_base64}
    
    # Send POST request with the image base64 string
    response = requests.post(API_URL, headers=headers, json=data)
    
    return response.json()


# Streamlit app
st.title("Gen Caption")
st.sidebar.title("Model Selection")
model_choice = st.sidebar.radio("Choose a model:", ["Custom API (ViT-GPT2)", "Hugging Face API (GIT-Base)"])

st.header("Upload an Image")
uploaded_image = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    # Show the uploaded image
    image = Image.open(uploaded_image).convert("RGB")
    st.image(image, caption="Uploaded Image Preview", width=300)

    # Generate button
    if st.button("Generate Caption"):
        with st.spinner("Generating caption..."):
            if model_choice == "Custom API (ViT-GPT2)":
                result = query_custom_api(image)
            elif model_choice == "Hugging Face API (GIT-Base)":
                result = query_huggingface_api(image)

            # Extract and display the caption
            try:
                st.write(f"### {result[0]['generated_text']}")
            except (KeyError, IndexError):
                st.write("### Error: Unable to generate caption.")