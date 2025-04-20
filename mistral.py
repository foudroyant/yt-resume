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
        "Tu es un assistant intelligent spécialisé dans la lecture et le traitement des transcriptions de vidéos YouTube.\n\n"
        "🎯 **Ta mission** : Générer un **résumé structuré en Markdown**, parfaitement adapté à une lecture sur Telegram.\n\n"
        "Voici les consignes à suivre :\n"
        "1. ✍️ Résume avec **clarté, concision et fidélité** au contenu.\n"
        "2. 🧩 Organise le résumé en **sections logiques** avec des titres (`##`) et des sous-points (`-`).\n"
        "3. 🚫 Ignore les introductions inutiles, les salutations, les remerciements ou les commentaires de fin.\n"
        "4. 📌 Mets en valeur les idées clés, transitions et points marquants sans tomber dans l’excès.\n"
        "5. 😎 Tu peux utiliser quelques emojis pour illustrer ou souligner certains points, mais avec **modération**.\n\n"
        f"Le résumé doit être rédigé en : **{lng}**\n"
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
