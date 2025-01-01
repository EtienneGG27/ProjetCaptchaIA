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

captchas = {
    "mnt/data/captcha1.png": "Td4eVa",
    "mnt/data/captcha2.png": "263S2V",
    "mnt/data/captcha3.png": "palaubits",
    "mnt/data/captcha4.png": "8514582",
    "mnt/data/captcha5.png": "AAXUE",
    "mnt/data/captcha6.png": "RUNAJIX",
    "mnt/data/captcha8.png": "JIC22U",
    "mnt/data/captcha9.png": "mwxe2",
    "mnt/data/captcha10.png": "eps10vector",
}

captcha1 = "mnt/data/captcha1.png"

if __name__ == "__main__":
    for captcha_path, solution in captchas.items():
        print(solution + " : " + resoudreCaptchaEasyOcr(captcha_path))

    for captcha_path, solution in captchas.items():
        print(solution + " : " + resoudreCaptchaPyTesseract(captcha_path))

    for captcha_path, solution in captchas.items():
        print(
            solution
            + " : "
            + resoudreCaptchaGemini("gemini-1.5-pro", captcha_path, prompt)
        )

    for captcha_path, solution in captchas.items():
        print(
            solution + " : " + resoudreCaptchaGPT("gpt-4o-mini", captcha_path, prompt)
        )
