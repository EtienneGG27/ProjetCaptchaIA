from GEMINI import resoudreCaptchaGemini
from OPENAI import resoudreCaptchaGPT
from PYTESSERACT import resoudreCaptchaPyTesseract

# Prompt :
prompt = (
    "Voici un texte déformé issu d'un CAPTCHA. "
    "Veuillez me fournir le texte ou les chiffres exacts "
    "après avoir interprété l'image. "
    "Assurez-vous de bien distinguer les caractères : "
)

if __name__ == "__main__":
    print(resoudreCaptchaPyTesseract("mnt/data/captcha1.png"))
    print(resoudreCaptchaGemini("gemini-1.5-pro", "mnt/data/captcha1.png", prompt))
    print(resoudreCaptchaGPT("gpt-4o-mini", "mnt/data/captcha1.png", prompt))
