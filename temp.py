#https://n8n.bambyno.xyz/webhook-test/69e8301c-2b28-48a2-94e2-a0d3113b369a

import requests

video = 'https://youtu.be/yNbGwnaa7Io?si=8DiuMv8lAZVgQpkB'

payload  = {
    "video_id": video,
    "format": True
}

params = {
    "video_id": video
}

response =  requests.get('https://n8n.bambyno.xyz/webhook-test/69e8301c-2b28-48a2-94e2-a0d3113b369a', params=params)
print(response.text)