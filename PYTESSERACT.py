import os

import cv2
import numpy as np
import pytesseract


def preprocess_image(image_path):
    # Charger l'image
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Convertir en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Appliquer un seuil adaptatif pour binariser
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    # Éliminer le bruit avec un filtre médian
    denoised = cv2.medianBlur(binary, 3)

    # Optionnel : Dilatation et érosion pour améliorer le contraste
    kernel = np.ones((2, 2), np.uint8)
    processed = cv2.dilate(denoised, kernel, iterations=1)
    processed = cv2.erode(processed, kernel, iterations=1)

    # Sauvegarder l'image prétraitée pour vérifier
    temp_path = "processed_captcha.png"
    cv2.imwrite(temp_path, processed)

    return temp_path


def solve_captcha(image_path):
    # Prétraiter l'image
    temp_path = preprocess_image(image_path)

    try:
        # Extraire le texte avec pytesseract
        custom_config = r"--oem 3 --psm 6"
        text = pytesseract.image_to_string(temp_path, config=custom_config)

        # Nettoyer le texte pour enlever les artefacts
        clean_text = "".join(
            filter(str.isalnum, text)
        )  # Garde uniquement les caractères alphanumériques
    finally:
        # Supprimer le fichier temporaire
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return clean_text


# Fonction pour tester plusieurs CAPTCHA
def resoudreCaptchaPyTesseract(captcha_path):
    try:
        result = solve_captcha(captcha_path)
        return result
    except Exception as e:
        print(f"Erreur pour {captcha_path}: {e}")
        return ""
