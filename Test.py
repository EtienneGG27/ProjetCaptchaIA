import json
import os
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


def save_cookies(driver, output_file):
    """
    Sauvegarde les cookies actuels du navigateur dans un fichier au format JSON.
    :param driver: Instance du navigateur Selenium
    :param output_file: Fichier JSON où sauvegarder les cookies
    """
    cookies = driver.get_cookies()
    with open(output_file, "w") as file:
        json.dump(cookies, file, indent=4)
    print(f"Cookies sauvegardés dans {output_file}")


def load_cookies(driver, input_file):
    """
    Charge les cookies depuis un fichier JSON dans le navigateur.
    :param driver: Instance du navigateur Selenium
    :param input_file: Fichier JSON contenant les cookies
    """
    with open(input_file, "r") as file:
        cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
    print("Cookies chargés dans le navigateur.")


def simulate_mouse_movement(driver, element):
    """
    Simule un mouvement réaliste de la souris vers un élément.
    :param driver: Instance du navigateur Selenium
    :param element: Élément cible
    """
    actions = ActionChains(driver)
    for _ in range(random.randint(3, 6)):
        # Mouvement aléatoire autour de l'élément
        actions.move_to_element_with_offset(
            element, random.uniform(-50, 50), random.uniform(-50, 50)
        ).pause(random.uniform(0.1, 0.3))
    actions.move_to_element(element).pause(random.uniform(0.5, 1.0)).click().perform()
    print("Clic simulé avec mouvement réaliste.")


# Fichiers de cookies
cookies_file = "cookies.json"

# Script principal
try:
    # Initialiser Selenium WebDriver avec options
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)

    # Accéder au site Web cible
    demo_url = "https://www.google.com/recaptcha/api2/demo"
    driver.get(demo_url)

    # Si les cookies n'existent pas encore, les extraire et les sauvegarder
    if not os.path.exists(cookies_file):
        print("Extraction des cookies...")
        save_cookies(driver, cookies_file)

    # Charger les cookies dans le navigateur
    load_cookies(driver, cookies_file)

    # Rafraîchir la page pour appliquer les cookies
    driver.refresh()
    time.sleep(random.uniform(2, 4))

    # Basculer dans l'iframe contenant le reCAPTCHA
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)

    # Localiser la case reCAPTCHA
    recaptcha_checkbox = driver.find_element(By.CLASS_NAME, "recaptcha-checkbox-border")

    # Simuler un mouvement réaliste de la souris et cliquer
    simulate_mouse_movement(driver, recaptcha_checkbox)

    # Revenir au contexte principal
    driver.switch_to.default_content()

    # Localiser et cliquer sur le bouton "Afficher"
    submit_button = driver.find_element(By.ID, "recaptcha-demo-submit")
    simulate_mouse_movement(driver, submit_button)

    print("Formulaire soumis avec succès.")

    # Pause pour observer
    time.sleep(random.uniform(5, 7))

except Exception as e:
    print(f"Une erreur est survenue : {e}")

finally:
    # Fermer le navigateur
    if "driver" in locals():
        driver.quit()
