import os
from mistralai import Mistral

from dotenv import load_dotenv

load_dotenv()  # Charger les variables d'environnement (.env)

api_key_ = os.environ["MISTRAL_API_KEY"]
api_key = os.getenv("MISTRAL_API_KEY")
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

def summarize_youtube_script_with_mistral(script: str, lng : str) -> dict:
    """
    Résume un script de vidéo YouTube avec Mistral AI en Markdown structuré.

    Args:
        script (str): Transcription complète de la vidéo.

    Returns:
        dict: Résumé structuré en Markdown.
    """

    system_prompt = (
        "Tu es un assistant intelligent qui lit des transcriptions de vidéos YouTube.\n"
        "Ta tâche est de produire un **résumé structuré en Markdown**.\n\n"
        "- Divise le contenu en parties claires avec des *titres ou sous-titres*.\n"
        "- Résume chaque partie de façon **concise, fidèle et bien rédigée**.\n"
        "- Utilise une structure lisible, avec `##` pour les sections, `-` pour les points importants, sachant que le résumé est destiné à être lu sur Telegram.\n"
        "- Dans ton résumé, n'insère pas l'introduction de la vidéo, ni les commentaires du début ou de la fin. Utilise les emoji de Telegram si necessaire mais n'abuse pas.\n"
        #"- Si possible, indique les moments clés ou transitions de sujet.\n"
        "- Tu fais le résumé en : " + lng
    )

    chat_response = client.chat.complete(
        model=model,
        messages = [
            {'role':"system", 'content':system_prompt},
            {'role':"user", 'content':script}
        ]
    )


    result = chat_response.choices[0].message.content

    return {
        "markdown_summary": result,
    }
