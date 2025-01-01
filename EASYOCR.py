import easyocr


def resoudreCaptchaEasyOcr(image_path: str) -> str:
    reader = easyocr.Reader(["en"])
    result = reader.readtext(image_path)
    textCaptcha = ""
    for bbox, text, prob in result:
        textCaptcha += text
    return textCaptcha
