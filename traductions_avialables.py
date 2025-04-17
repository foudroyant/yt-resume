from youtube_transcript_api import YouTubeTranscriptApi

from id_video import extract_youtube_id

def list_available_transcript_languages(youtube_url: str):
    video_id = extract_youtube_id(youtube_url)
    
    if not video_id:
        return None

    try:
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        langues = []

        for t in transcripts:
            langues.append((t.language_code, t.language))  # Tuple: (code, nom)

        return langues

    except Exception as e:
        print(f"❌ Erreur lors de la récupération des langues : {e}")
        return None

print(list_available_transcript_languages("https://youtu.be/UIH0nvDgxw0?si=MQVlYdr8b_744heO"))
#list_available_transcript_languages("https://youtu.be/UIH0nvDgxw0?si=MQVlYdr8b_744heO")