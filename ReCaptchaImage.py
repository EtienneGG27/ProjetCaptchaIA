import base64
import os

import openai
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


openai.api_key = os.getenv("CLE_OPENAI")


def detect_image_type_with_openai(image_path):
    """
    Utilise l'API OpenAI pour détecter si l'image est une seule grande image ou une grille.
    """
    print("Détection du type d'image via ChatGPT...")
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    prompt = (
        "Regarde cette image que je t'envoie. Réponds uniquement par 'grille 3x3' si elle contient une grille "
        "de 9 images distinctes ou par 'image 4x4' si elle est une seule grande image à découper en 16 parties. "
        "Ne fais aucun commentaire supplémentaire."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            },
                        },
                    ],
                }
            ],
        )

        result = response["choices"][0]["message"]["content"].strip().lower()
        print(f"Réponse API pour le type d'image : {result}")
        if "grille 3x3" in result:
            return "3x3"
        elif "image 4x4" in result:
            return "4x4"
        else:
            raise ValueError("Réponse inattendue de l'API.")
    except Exception as e:
        print(f"Erreur lors de l'appel à l'API pour détecter le type d'image : {e}")
        raise


def split_image_into_tiles(image_path, output_folder="images"):
    print("Division de l'image en sous-images...")
    rows, cols = 3, 3
    result = detect_image_type_with_openai(image_path)
    if result == "3x3":
        rows, cols = 3, 3
    elif result == "4x4":
        rows, cols = 4, 4
    os.makedirs(output_folder, exist_ok=True)
    image = Image.open(image_path)
    width, height = image.size
    tile_width = width // cols
    tile_height = height // rows

    tile_paths = []
    for row in range(rows):
        for col in range(cols):
            left = col * tile_width
            top = row * tile_height
            right = left + tile_width
            bottom = top + tile_height
            tile = image.crop((left, top, right, bottom))
            tile = tile.resize((64, 64))  # Réduction de la taille
            tile_path = os.path.join(output_folder, f"tile_{row}_{col}.png")
            tile.save(tile_path)
            tile_paths.append(tile_path)

    print(f"{len(tile_paths)} sous-images extraites.")
    return tile_paths


def download_images(driver, image_selector, folder="images"):
    print("Téléchargement de l'image regroupée...")
    os.makedirs(folder, exist_ok=True)
    tiles = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, image_selector))
    )
    image_path = os.path.join(folder, "grouped_image.png")

    for i, tile in enumerate(tiles):
        try:
            img = tile.find_element(By.TAG_NAME, "img")
            src = img.get_attribute("src")
            if not src:
                continue
            if src.startswith("data:image"):
                base64_data = src.split(",")[1]
                image_data = base64.b64decode(base64_data)
            elif src.startswith("http"):
                response = requests.get(src, stream=True)
                if response.status_code != 200:
                    continue
                image_data = response.content
            else:
                continue
            with open(image_path, "wb") as f:
                f.write(image_data)
            break
        except Exception as e:
            print(f"Erreur lors du téléchargement de l'image {i}: {e}")

    if not os.path.exists(image_path):
        raise ValueError("Impossible de télécharger l'image regroupée.")
    return split_image_into_tiles(image_path)


def solve_captcha_images_with_openai(image_paths, prompt):
    print("Analyse des images via ChatGPT...")
    relevant_indices = []

    for index, image_path in enumerate(image_paths):
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")

        # Création de la consigne envoyée à l'API
        enriched_prompt = (
            f"Consigne : cette image montre une {prompt}. "
            "Réponds uniquement par 'oui' ou 'non'. Si la réponse est 'oui', "
            "assure-toi que la probabilité dépasse 50%."
        )

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": enriched_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64," f"{image_data}"
                                },
                            },
                        ],
                    },
                ],
            )

            result = response["choices"][0]["message"]["content"].strip().lower()
            print(f"Réponse API pour l'image {index + 1} : {result}")
            if "oui" in result:
                relevant_indices.append(index)
        except Exception as e:
            print(f"Erreur lors de l'appel à l'API pour l'image {index + 1} : {e}")

    print(f"Indices pertinents : {relevant_indices}")
    return relevant_indices


def find_prompt(driver):
    selectors = [
        ".rc-imageselect-desc-no-canonical",
        ".rc-imageselect-desc",
        ".rc-imageselect-desc-wrapper",
    ]
    for selector in selectors:
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            if element and element.text.strip():
                prompt = element.text.strip().replace("\n", " ")
                print(f"Consigne détectée : {prompt}")
                return prompt
        except Exception as e:
            print(f"Erreur lors de la récupération de la consigne : {e}")
            continue
    raise ValueError("Impossible de trouver la consigne.")


def download_updated_images(driver, image_selector, folder="updated_images"):
    print("Téléchargement des images mises à jour après le clic...")
    return download_images(driver, image_selector, folder)


def process_captcha_cycle(
    driver, image_selector, prompt, is_clicked, clicked_indices=[]
):
    print("Début du cycle de traitement du CAPTCHA...")
    relevant_indices = []

    # Étape 1 : Télécharger l'image globale et la découper
    image_paths = download_images(driver, image_selector)
    relevant_indices = solve_captcha_images_with_openai(image_paths, prompt)

    # Étape 2 : Cliquer sur les images pertinentes
    tiles = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, image_selector))
    )
    for index in relevant_indices:
        try:
            ActionChains(driver).move_to_element(tiles[index]).click().perform()
        except Exception as e:
            print(f"Erreur lors du clic sur l'image {index} : {e}")

    print("Validation en cours...")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "recaptcha-verify-button"))
    ).click()

    print(f"Images sélectionnées : {relevant_indices}")
    return relevant_indices


def interact_with_captcha(driver):
    print("Bascule vers l'iframe du reCAPTCHA...")
    iframe = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//iframe[@title='reCAPTCHA']"))
    )
    driver.switch_to.frame(iframe)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))
    ).click()
    driver.switch_to.default_content()

    captcha_iframe = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, "//iframe[contains(@src, 'recaptcha/api2/bframe')]")
        )
    )
    driver.switch_to.frame(captcha_iframe)

    tile_selector = ".rc-imageselect-tile"
    selected_indices = set()

    while True:
        prompt = find_prompt(driver)
        # Étape 1 : Effectuer un cycle complet
        relevant_indices = process_captcha_cycle(
            driver, tile_selector, prompt, is_clicked=False
        )
        selected_indices.update(relevant_indices)

        # Étape 2 : Valider ou re-télécharger les images mises à jour
        # Vérifiez si le CAPTCHA est terminé
        try:
            WebDriverWait(driver, 5).until(
                lambda d: d.execute_script(
                    "return document.getElementById('g-recaptcha-response').value !== '';"
                )
            )
            print("Captcha résolu.")
            break
        except Exception:
            print("De nouvelles images sont apparues. Recommencer le processus...")
            prompt = find_prompt(driver)
            download_images(driver, tile_selector, folder="updated_images")
            relevant_indices_after_click = process_captcha_cycle(
                driver,
                tile_selector,
                prompt,
                is_clicked=True,
                clicked_indices=list(selected_indices),
            )
            selected_indices.update(relevant_indices_after_click)


def resolutionReCaptchaV2Image():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    url = "https://www.google.com/recaptcha/api2/demo"
    driver.get(url)
    try:
        interact_with_captcha(driver)
        input("Appuyez sur Entrée pour quitter...")
    finally:
        driver.quit()
