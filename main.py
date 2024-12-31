from OPENAI import resoudreCaptchaGPT

# Prompt :
prompt = (
    "Voici un texte déformé issu d'un CAPTCHA. "
    "Veuillez me fournir le texte ou les chiffres exacts "
    "après avoir interprété l'image. "
    "Assurez-vous de bien distinguer les caractères : "
)


print(resoudreCaptchaGPT("gpt-4o-mini", "captcha1.png", prompt))
