from EASYOCR import resoudreCaptchaEasyOcr
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

captcha1 = "mnt/data/captcha1.png"

if __name__ == "__main__":
    print(resoudreCaptchaEasyOcr(captcha1))
    print(resoudreCaptchaPyTesseract(captcha1))
    print(resoudreCaptchaGemini("gemini-1.5-pro", captcha1, prompt))
    print(resoudreCaptchaGPT("gpt-4o-mini", captcha1, prompt))
