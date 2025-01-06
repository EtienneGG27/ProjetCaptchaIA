import easyocr


def resoudreCaptchaEasyOcr(captcha_path: str) -> str:
    try:
        # Initialiser le lecteur EasyOCR
        reader = easyocr.Reader(["en"])

        # Effectuer la reconnaissance OCR
        result = reader.readtext(captcha_path)

        # Extraire le texte détecté
        text_captcha = "".join(text for _, text, _ in result).replace(" ", "")
    except Exception as e:
        print(f"Erreur lors de la résolution du CAPTCHA : {e}")
        text_captcha = "Erreur"

    return text_captcha
