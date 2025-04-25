ASTUCE_LANGUES = """💡 *Astuce* : Vous pouvez choisir la langue de sortie de la transcription en utilisant la commande /languages."""

#############################################################################################################
ACCUEIL_MESSAGE = """
🧾 *Présentation du bot YT Helper*

Bienvenue sur *YT Helper* — votre assistant intelligent pour résumer rapidement les vidéos et *shorts* YouTube à partir d’un simple lien.  
Ce bot utilise une *intelligence artificielle avancée* pour vous fournir des résumés clairs, utiles et bien structurés, en quelques secondes.

⚙️ *Commandes disponibles*

- 📥 `/start`  
  Démarre le bot et affiche un message d’accueil.

- 🌐 `/languages`  
  Choisissez votre langue pour afficher les résumés en votre langue préférée.

- 📘 `/tutoriel`  
  Affiche un tutoriel pour apprendre à utiliser toutes les fonctionnalités du bot, étape par étape.

- 😋 `/offres`  
  Affiche les offres disponibles pour l'application.

- 😎 `/about`  
  Affiche vos informations personnelles.

- ☺️ `/payer`  
  S'abonner à une offre dans l'application.

💡 *Astuce* : Il vous suffit d’envoyer un lien YouTube pour recevoir un résumé ! C’est aussi simple que ça.
"""

#############################################################################################################
TUTORIEL_MESSAGE = """
📘 *Tutoriel : Utilisation de YT Helper*

Bienvenue dans le tutoriel de *YT Helper*, votre assistant pour résumer facilement les vidéos YouTube !

🧭 *Étapes principales :*

1. *Choisir la langue d’affichage (optionnel)*  
Utilisez la commande `/languages` pour définir la langue dans laquelle vous souhaitez recevoir les résumés.  
Cela vous permet d’interagir dans votre langue préférée, mais n’influence *pas* la transcription de la vidéo.

2. *Envoyer un lien YouTube*  
Collez simplement un lien vers une vidéo ou un *short* YouTube. Le bot va analyser le contenu automatiquement.


3. *Recevoir le résumé*  
Après avoir envoyé le lien de la vidéo, l'application vous affichera un résumé clair, utile et structuré, grâce à une IA performante, en quelques secondes.

💡 *Astuce* : Vous pouvez recommencer à tout moment avec `/start`, ou changer votre langue d’affichage avec `/languages`.
"""

GAME_OVER_MESSAGE = """
⚠️ *Tu as utilisé tous tes crédits YT Helper ce mois-ci !*

🔓 **Free** – *Plan actuel*  
Tu disposes de *10 crédits par mois*, te permettant de transcrire et résumer des vidéos grâce à notre intelligence artificielle. Tu as atteint ta limite.

🚀 **Pro – 5€/mois**  
Pour les utilisateurs réguliers :  
Tout ce qui est dans le plan *Free* + **50 crédits par mois**

🧠 **Avancée – 12€/mois**  
Pour les *power users* et professionnels :  
Tout ce qui est dans le plan *Pro* + **150 crédits par mois**

👉 Passe à un plan supérieur `/payer`

Merci d’utiliser *YT Helper* ❤️

"""

def ABOUT_MESSAGE(type, credits, payement) :
  return f"""
    👤 *Informations de ton compte YT Helper*

💳 **Type de compte** : {type}  
💰 **Crédits restants** : {credits}  
📅 **Dernier paiement** : {payement}

🔄 Tu peux passer à un plan supérieur pour débloquer plus de crédits et de fonctionnalités.

👉 Voir les offres `/offres`

  """


OFFRES_MESSAGE = """
📦 *Nos offres disponibles* :

🔓 **Free** – *Gratuit à vie*  
• 10 crédits/mois  
• Transcription **dans toutes les langues**  
• Résumé avec intelligence artificielle

🚀 **Pro – 5€/mois**  
• Tout ce qui est dans le plan Free  
• 50 crédits/mois  
• Résumé plus détaillé (bullet points)

🧠 **Avancée – 12€/mois**  
• Tout ce qui est dans le plan Pro  
• 150 crédits/mois  
• Résumé vocal en plus du texte (Bientot disponible) 
    """
