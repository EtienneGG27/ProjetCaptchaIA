import os
from dotenv import load_dotenv
from openai import OpenAI

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Accéder à la variable CLE_OPENAI
api_key = os.getenv("CLE_OPENAI")

# Utiliser la clé API pour initialiser le client OpenAI
client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Ceci est un exercice. Je vais te montrer une image sur laquelle un texte avec des lettres est caché. Tu dois trouvé le texte. Tu me donneras la réponse dans le format suivant ;"
                                         ": 'Le texte caché est : [votre réponse]'."},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "",
                    },
                },
            ],
        }
    ],
    max_tokens=300,
)

print(response.choices[0])