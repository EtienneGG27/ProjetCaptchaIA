import os

import cv2
import easyocr
import numpy as np


def preprocess_image(captcha_path: str) -> str:
    """
    Prétraiter l'image pour améliorer la reconnaissance de caractères.
    Sauvegarde l'image prétraitée et retourne son chemin.
    """
    # Charger l'image en couleur
    image = cv2.imread(captcha_path, cv2.IMREAD_COLOR)

    # Vérifier si l'image est chargée correctement
    if image is None:
        raise FileNotFoundError(f"Impossible de charger l'image : {captcha_path}")

    # Convertir en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Appliquer un filtre gaussien pour réduire le bruit
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Binarisation adaptative pour augmenter le contraste
    binary = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )

    # Optionnel : dilater et éroder pour améliorer les contours
    kernel = np.ones((2, 2), np.uint8)
    processed = cv2.dilate(binary, kernel, iterations=1)
    processed = cv2.erode(processed, kernel, iterations=1)

    # Sauvegarder l'image prétraitée
    processed_path = "processed_captcha.png"
    cv2.imwrite(processed_path, processed)

    return processed_path


def resoudreCaptchaEasyOcr(captcha_path: str) -> str:
    """
    Résoudre un CAPTCHA en utilisant EasyOCR avec prétraitement d'image.
    Supprime l'image prétraitée à la fin.
    """
    # Prétraiter l'image
    processed_image_path = preprocess_image(captcha_path)

    try:
        # Initialiser le lecteur EasyOCR
        reader = easyocr.Reader(["en"])

        # Effectuer la reconnaissance OCR
        result = reader.readtext(processed_image_path)

        # Extraire le texte détecté
        text_captcha = "".join(text for _, text, _ in result)
    finally:
        # Supprimer l'image prétraitée
        if os.path.exists(processed_image_path):
            os.remove(processed_image_path)

    return text_captcha
