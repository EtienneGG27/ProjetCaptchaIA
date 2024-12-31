import base64
import os

from dotenv import load_dotenv
from openai import OpenAI

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Prompt :
prompt = (
    "Voici un texte déformé issu d'un CAPTCHA. "
    "Veuillez me fournir le texte ou les chiffres exacts "
    "après avoir interprété l'image. "
    "Assurez-vous de bien distinguer les caractères : "
)

# Accéder à la variable CLE_OPENAI
api_key = os.getenv("CLE_OPENAI")

# Utiliser la clé API pour initialiser le client OpenAI
client = OpenAI(api_key=api_key)


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


base64_image = encode_image("captcha1.png")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64," f"{base64_image}"},
                },
            ],
        }
    ],
    max_tokens=300,
)


print(response.choices[0])
