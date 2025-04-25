from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes,  MessageHandler, filters
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os
import logging
from directus import create_article, get_user_by_telegram, update_article
from id_video import extract_youtube_id
from langues import les_langues
from main import get_youtube_transcript_from_url
from mistral import summarize_youtube_script_with_mistral
from textes import ABOUT_MESSAGE, ACCUEIL_MESSAGE, ASTUCE_LANGUES, GAME_OVER_MESSAGE, OFFRES_MESSAGE, TUTORIEL_MESSAGE
from traductions_avialables import list_available_transcript_languages
import requests

# Charger les variables d'environnement
load_dotenv()
logging.basicConfig(level=logging.INFO)

TOKEN_BOT = os.getenv("TELEGRAM_TOKEN")
URL_KOME = os.getenv("URL_KOME")
URL_WEBHOOK_N8N = os.getenv("URL_WEBHOOK_N8N")


async def send_long_message(text: str, update: Update):
    chunk_size = 4000  # Limite de Telegram < 4096

    # Récupérer l'objet message selon le contexte
    if update.message:
        target = update.message
    elif update.callback_query:
        target = update.callback_query.message
    else:
        return  # Aucun message cible

    # Envoyer le texte par morceaux
    for i in range(0, len(text), chunk_size):
        await target.reply_text(
            text[i:i+chunk_size], 
            parse_mode="Markdown"
        )
    #await update.message.reply_text(ASTUCE_LANGUES, parse_mode="Markdown")


def create_language_keyboard(video: str):
    langs = list_available_transcript_languages(video)
    print(langs)
    keyboard = []
    for lang_code, lang_name in langs:
        keyboard.append([
            InlineKeyboardButton(f"{lang_name} ({lang_code})", callback_data=f"lang_{lang_code}")
        ])
    return InlineKeyboardMarkup(keyboard)


def get_language_keyboard(languages):
    keyboard = []
    
    # Grouper les langues deux à deux
    for i in range(0, len(languages), 2):
        row = []
        for j in range(2):
            if i + j < len(languages):
                code, name = languages[i + j]
                row.append(InlineKeyboardButton(
                    text=name, 
                    callback_data=f"lang#{name}"
                ))
        keyboard.append(row)
    
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    account = update.message.from_user.id
    # Vérifier si l'utilisateur existe dans la base de données
    user = get_user_by_telegram(account)
    print(user)
    if user:
        # L'utilisateur existe, vous pouvez le traiter ici
        context.user_data["user"] = user
        print("Utilisateur trouvé :", user)
    else:
        # L'utilisateur n'existe pas, vous pouvez l'enregistrer ici
        _create = create_article("users", {
            "account_telegram": account,
            "fullname": update.message.from_user.first_name + update.message.from_user.last_name,
            "username": update.message.from_user.username,
            "link": update.message.from_user.link,
            "type_account" : "Free",
            "credits" : 10
        })
        context.user_data["user"] = _create["data"]
        #print("Utilisateur non trouvé mais il a &t& ajouté:", _create)

    await update.message.reply_text(ACCUEIL_MESSAGE, parse_mode="Markdown")


async def tutoriel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TUTORIEL_MESSAGE, parse_mode="Markdown")


async def About(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'user' not in context.user_data : 
        context.user_data["user"] = get_user_by_telegram(update.message.from_user.id)
    
    _MSG = ABOUT_MESSAGE(context.user_data["user"]["type_account"], context.user_data["user"]["credits"], "Aucun paiement pour le moment")
    await update.message.reply_text(_MSG, parse_mode="Markdown")


async def Offres(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(OFFRES_MESSAGE, parse_mode="Markdown")


async def languages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    languages = les_langues()
    markup = get_language_keyboard(languages)
    sent_message = await update.message.reply_text(
        "🌐 Choisissez une langue pour la transcription :", 
        reply_markup=markup
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    video_id = extract_youtube_id(text)
    context.user_data["VIDEO_ID"] = video_id
    context.user_data["URL"] = text
    script = ""
    codes_langue=[]
    langues = []
    loading_msg = None

    '''transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
    for t in transcripts:
        langues.append((t.language_code, t.language))  # Tuple: (code, nom)

    if len(langues) > 0:
        codes_langue = [code for code, nom in langues]

    selected_langue = codes_langue[0]
    print(selected_langue)'''

    """await update.message.reply_text(
        "🌐 Choisissez la langue du script de la vidéo :",
        reply_markup=create_language_keyboard(text)
    )"""

    if 'user' not in context.user_data : 
        context.user_data["user"] = get_user_by_telegram(update.message.from_user.id)

    if context.user_data["user"]["credits"] > 0 :
        if 'LANGUE' not in context.user_data :
            language_dict = dict(les_langues())
            language_name = language_dict.get(update.message.from_user.language_code, "Français")
            context.user_data["LANGUE"] = language_name
            
        if not context.user_data["VIDEO_ID"]:
            await update.message.reply_text("❌ Ce n’est pas un lien YouTube valide.")
            return

        loading_msg = await update.message.reply_text("📄 Traitement en cours...")
        try:

            params = {
                "video_id": text
            }
            response =  requests.get(URL_WEBHOOK_N8N, params=params)
            #print(response.text)
            script = response.text
            #get_youtube_transcript_from_url(context.user_data["URL"], lang_code=selected_langue)["full_text"]
            if not script:
                await update.message.reply_text(f"⚠️ Pas de transcription")
                return
        except Exception as e:
            await update.message.reply_text(f"⚠️ Erreur : {str(e)}")
            return

        #await loading_msg.delete()
        #loading_msg = await query.edit_message_text("💡 Résumé en cours...")
        summary = summarize_youtube_script_with_mistral(script, context.user_data["LANGUE"])["markdown_summary"]
        # await update.message.reply_text(summary[:4096]) # Telegram limite à 4096 caractères par message

        _updated = update_article("users", context.user_data["user"]["id"], {
            "credits" : context.user_data["user"]["credits"] - 1
        })
        print(_updated)
        context.user_data["user"] = _updated["data"]

        await loading_msg.delete()
        await send_long_message(summary, update)
    else:
        await update.message.reply_text(GAME_OVER_MESSAGE, parse_mode="Markdown")

    

async def handle_language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("lang_"):
        selected_lang = query.data.split("_")[1]

        if 'LANGUE' not in context.user_data :
            language_dict = dict(les_langues())
            language_name = language_dict.get(query.from_user.language_code, "Français")
            context.user_data["LANGUE"] = language_name
        
        if not context.user_data["VIDEO_ID"]:
            await query.edit_message_text("❌ Ce n’est pas un lien YouTube valide.")
            return

        loading_msg = await query.edit_message_text("📄 Traitement en cours...")
        try:
            
            script = get_youtube_transcript_from_url(context.user_data["URL"], lang_code=selected_lang)["full_text"]
            if not script:
                await query.edit_message_text(f"⚠️ Pas de transcription en '{selected_lang}'")
                return
        except Exception as e:
            await query.edit_message_text(f"⚠️ Erreur : {str(e)}")
            return

        #await loading_msg.delete()
        #loading_msg = await query.edit_message_text("💡 Résumé en cours...")
        summary = summarize_youtube_script_with_mistral(script, context.user_data["LANGUE"])["markdown_summary"]
        # await update.message.reply_text(summary[:4096]) # Telegram limite à 4096 caractères par message
        await loading_msg.delete()
        await send_long_message(summary, update)
        
        
    
    elif query.data.startswith("lang#"):
        selected_lang = query.data.split("#")[1]
        context.user_data["LANGUE"] = selected_lang
        await query.message.delete()


def run_bot():
    token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_language_choice))
    app.add_handler(CommandHandler("languages", languages))
    app.add_handler(CommandHandler("tutoriel", tutoriel))
    app.add_handler(CommandHandler("about", About))
    app.add_handler(CommandHandler("offres", Offres))

    app.run_polling()

if __name__ == "__main__":
    run_bot()