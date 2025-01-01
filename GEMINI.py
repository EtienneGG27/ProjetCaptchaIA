import os

import google.generativeai as genai
import PIL.Image
from dotenv import load_dotenv


def resoudreCaptchaGemini(model: str, captcha_path, prompt: str) -> str:
    load_dotenv()
    api_key = os.getenv("CLE_GEMINI")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model)
    response = model.generate_content([prompt, PIL.Image.open(captcha_path)])
    return response.text
