import base64
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def telechargerCaptchaSelenium(driver, captcha_path: str) -> str:
    try:
        # Localiser l'image CAPTCHA par son ID
        captcha_img = driver.find_element(By.ID, "demoCaptcha_CaptchaImage")

        # Récupérer le contenu de l'image encodée en Base64 ou l'URL
        captcha_src = captcha_img.get_attribute("src")
        if captcha_src.startswith("data:image"):
            # Décoder l'image encodée en Base64
            base64_data = captcha_src.split(",")[
                1
            ]  # Supprimer le préfixe "data:image/jpeg;base64,"
            with open(captcha_path, "wb") as f:
                f.write(base64.b64decode(base64_data))
            print(f"CAPTCHA téléchargé et enregistré en tant que '{captcha_path}'.")
        else:
            print("CAPTCHA introuvable ou non encodé en base64.")
    except Exception as e:
        print(f"Erreur lors du téléchargement du CAPTCHA : {e}")

    return captcha_path


def envoieValeurCaptchaEtRecupereResultatSelenium(driver, captcha_value: str) -> str:
    try:
        # Localiser le champ d'entrée pour le CAPTCHA
        captcha_input = driver.find_element(By.ID, "captchaCode")

        # Entrer la valeur du CAPTCHA
        captcha_input.clear()
        captcha_input.send_keys(captcha_value)

        # Soumettre le formulaire
        captcha_input.send_keys(Keys.RETURN)

        # Attendre la mise à jour de la page (ajustez le délai si nécessaire)
        time.sleep(2)

        # Récupérer le résultat dans le champ 'validationResult'
        validation_result = driver.find_element(By.ID, "validationResult").text

        if validation_result:
            return validation_result
        else:
            return "Aucun résultat trouvé sur la page."
    except Exception as e:
        print(f"Erreur lors de la soumission ou de la récupération du résultat : {e}")
        return "Erreur"
