from youtube_transcript_api import YouTubeTranscriptApi

from id_video import extract_youtube_id

def list_available_transcript_languages(youtube_url: str):
    video_id = extract_youtube_id(youtube_url)
    if not video_id:
        #print("❌ Impossible d'extraire l'ID de la vidéo.")
        return

    try:
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        liste = []
        #print(f"\n🌍 Langues disponibles pour la vidéo {video_id} :\n")
        for t in transcripts:
            auto = " (auto-généré)" if t.is_generated else ""
            print(f"🔹 {t.language_code} ➜ {t.language}{auto}")
            liste.append([t.language_code, t.language])
        return liste
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des langues : {e}")

