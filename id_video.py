import re
from urllib.parse import urlparse, parse_qs

def extract_youtube_id(url: str) -> str:
    """
    Extrait l'ID d'une vidéo YouTube à partir d'une URL.
    Gère les formats watch, youtu.be et shorts.
    """
    parsed_url = urlparse(url)

    if "youtu.be" in parsed_url.netloc:
        # Format court : youtu.be/VIDEO_ID
        return parsed_url.path.lstrip("/")

    elif "youtube.com" in parsed_url.netloc or "www.youtube.com" in parsed_url.netloc:
        if parsed_url.path.startswith("/watch"):
            # Format long : youtube.com/watch?v=VIDEO_ID
            query = parse_qs(parsed_url.query)
            return query.get("v", [None])[0]
        elif parsed_url.path.startswith("/shorts/"):
            # Format shorts : youtube.com/shorts/VIDEO_ID
            return parsed_url.path.split("/")[2]

    return None  # URL non valide ou ID introuvable
