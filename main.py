from selenium import webdriver

from EASYOCR import resoudreCaptchaEasyOcr
from GEMINI import resoudreCaptchaGemini
from HTTPREQUEST import (
    envoieValeurCaptchaEtRecupereResultatSelenium,
    telechargerCaptchaSelenium,
)
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
    url = "https://captcha.com/demos/features/captcha-demo.aspx"
    captcha_path = "mnt/data/captchaDemo.jpg"

    driver = webdriver.Chrome()
    driver.get(url)

    try:
        telechargerCaptchaSelenium(driver, captcha_path)
        print(f"CAPTCHA enregistré à : {captcha_path}")

        # captcha_value = input("Veuillez entrer la réponse du CAPTCHA : ")
        # captcha_value = resoudreCaptchaEasyOcr(captcha_path)
        captcha_value = resoudreCaptchaGemini(
            model="gemini-1.5-pro", captcha_path=captcha_path, prompt=prompt
        )
        print(f"Valeur du CAPTCHA détectée : {captcha_value}")

        resultat = envoieValeurCaptchaEtRecupereResultatSelenium(driver, captcha_value)
        print(f"Résultat retourné par la page : {resultat}")
    finally:
        driver.quit()


def test_captcha():
    for captcha_path, solution in captchas.items():
        print(solution + " : " + resoudreCaptchaEasyOcr(captcha_path=captcha_path))

    for captcha_path, solution in captchas.items():
        print(solution + " : " + resoudreCaptchaPyTesseract(captcha_path=captcha_path))

    for captcha_path, solution in captchas.items():
        print(
            solution
            + " : "
            + resoudreCaptchaGemini(
                model="gemini-1.5-pro", captcha_path=captcha_path, prompt=prompt
            )
        )

    for captcha_path, solution in captchas.items():
        print(
            solution
            + " : "
            + resoudreCaptchaGPT(
                model="gpt-4o-mini", captcha_path=captcha_path, prompt=prompt
            )
        )
