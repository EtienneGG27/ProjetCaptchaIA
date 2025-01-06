import base64
import os

import openai
from dotenv import load_dotenv

load_dotenv()


def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def resoudreCaptchaGPT(model: str, captcha_path: str, prompt: str) -> str:
    # Accéder à la variable CLE_OPENAI
    api_key = os.getenv("CLE_OPENAI")

    # Utiliser la clé API pour initialiser le client OpenAI
    openai.api_key = api_key

    base64_image = encode_image(captcha_path)

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64," f"{base64_image}"
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content
