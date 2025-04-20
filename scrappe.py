from yt_dlp import YoutubeDL

url = 'https://youtu.be/X--4L2y997k?si=rniUcNnWZnvI3teU'

with YoutubeDL({'quiet': True}) as ydl:
    info = ydl.extract_info(url, download=False)
    print(info['title'])
    print(info['description'])
    print(info['duration'])  # en secondes
    print(info['subtitles'])  # s’il y a des sous-titres
