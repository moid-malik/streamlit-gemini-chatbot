import os
from streamlit import secrets

from PIL import Image
import google.generativeai as genai
from credentials import GEMINI_API_KEY

genai.configure(api_key="AIzaSyCcfR2YJWevc1Dd-zLbE4-OyrHoTkeGwbY")


def load_gemini_pro(model_name: str) -> genai.GenerativeModel:
    """Returns the Gemini Pro Generative mod    el."""
    model: genai.GenerativeModel = genai.GenerativeModel(model_name=model_name)
    return model


def img_caption(image: Image.Image) -> str:
    """Returns the response for image captioning prompt."""
    model: genai.GenerativeModel = load_gemini_pro("gemini-1.5-flash")
    caption: str = model.generate_content(
        ["Write a short caption for this image.", image]).text or ""
    return caption

def llm_response(user_prompt: str) -> str:
    """Returns the response from the Gemini Pro LLM for a given user prompt."""
    llm_model: genai.GenerativeModel = load_gemini_pro("gemini-pro")
    result: str = llm_model.generate_content(user_prompt).text
    return result
