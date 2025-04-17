from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
import sys

from id_video import extract_youtube_id
from mistral import summarize_youtube_script_with_mistral
from traductions_avialables import list_available_transcript_languages

LINK = "https://youtu.be/X--4L2y997k?si=rniUcNnWZnvI3teU"
"""video_id = "IG7Q4i0daC4"  # Remplace par ton ID
video_id = extract_youtube_id()

try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['fr']) #Transcription avec les times-code
    full_text = " ".join([entry['text'] for entry in transcript]) #Transcription du script uniquement
    #print(full_text)
except Exception as e:
    print(f"Erreur : {e}")
    sys.exit()"""


def get_youtube_transcript_from_url(url: str, lang_code : str, with_timestamps=False):
    video_id = extract_youtube_id(url)
    
    if not video_id:
        print("❌ Impossible d'extraire l'ID de la vidéo.")
        sys.exit(1)

    try:
        try:
            # Essaye avec la langue spécifiée
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang_code])
        except NoTranscriptFound:
            #print(f"⚠️ Pas de transcription en '{lang_code}', tentative dans la langue d'origine...")
            # Si la langue n'existe pas, récupère la première dispo
            transcript = YouTubeTranscriptApi.list_transcripts(video_id).find_manually_created_transcript(['en', 'auto'])
            transcript = transcript.fetch()
            return None

        return {
            'transcript' : transcript,
            'full_text' : " ".join([entry['text'] for entry in transcript])
            }

    except (VideoUnavailable, TranscriptsDisabled, Exception) as e:
        print(f"❌ Erreur : {e}")
        return None
        #sys.exit(1)

#script = get_youtube_transcript_from_url(LINK)
#traductions = list_available_transcript_languages(LINK)
#print(traductions)

#resume = summarize_youtube_script_with_mistral(script["full_text"], lng="français")
#print(resume["markdown_summary"])