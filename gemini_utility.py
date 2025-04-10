import os
import json
import google.generativeai as genai
from PIL import Image
import io
from google.generativeai.types import content_types

# Get current working directory
working_directory = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(working_directory, "config.json")

# Load API key from config.json
try:
    with open(config_file_path, 'r') as file:
        config_data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError) as e:
    raise Exception(f"Error reading config.json: {e}")

GOOGLE_API_KEY = config_data.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("API Key missing in config.json")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Load Gemini Chat model
def load_gemini():
    return genai.GenerativeModel('gemini-1.5-pro-latest')

# Load Gemini Vision model


def load_geminiimage(prompt, image):
    if not isinstance(image, Image.Image):
        raise ValueError("Expected a PIL Image.")

    # Directly pass the PIL image and prompt
    vision_model = genai.GenerativeModel('gemini-1.5-flash')

    # Generate content using Gemini Vision
    response = vision_model.generate_content([prompt, image])

    return response.text


# Load embedding model
def embedding_model(input_text):
    embedding_model_id = 'models/embedding-001'
    embedding = genai.embed_content(
        model=embedding_model_id,
        content=input_text,
        task_type='retrieval_document'
    )
    return embedding['embedding']

# Simple prompt response for "Ask Me Anything"
def gemini_response(user_prompt):
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content(user_prompt)
    return response.text