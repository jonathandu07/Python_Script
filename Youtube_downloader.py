from pytube import YouTube
from moviepy.editor import *
import os

def telecharger_et_convertir(url, chemin_sortie, codecs):
    try:
        # Téléchargement
        yt = YouTube(url)
        
        # Sélection du meilleur flux vidéo en 4K (sans audio)
        video_stream = yt.streams.filter(progressive=False, file_extension='mp4', resolution="2160p").first()
        if not video_stream:
            print("Vidéo 4K non disponible, téléchargement de la meilleure qualité disponible.")
            video_stream = yt.streams.filter(progressive=False, file_extension='mp4').order_by('resolution').desc().first()

        # Sélection du meilleur flux audio
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

        # Téléchargement des flux
        video_path = video_stream.download(output_path=chemin_sortie, filename="video_temp")
        audio_path = audio_stream.download(output_path=chemin_sortie, filename="audio_temp")

        # Fusion de la vidéo et de l'audio
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        final_clip = video_clip.set_audio(audio_clip)

        # Conversion avec différents codecs
        for codec in codecs:
            output_filename = f"{chemin_sortie}/video_convertie_{codec}_4K.mov"
            # Redimensionnement en 4K si nécessaire
            final_clip_resized = final_clip.resize(height=2160)
            final_clip_resized.write_videofile(output_filename, codec=codec)
            print(f"Conversion terminée avec le codec {codec} en 4K.")

        # Supprimer les fichiers temporaires
        os.remove(video_path)
        os.remove(audio_path)
    except Exception as e:
        print(f"Une erreur est survenue avec le codec {codec}:", e)

# Liste des codecs à utiliser
codecs = ["libx264", "mpeg4"] # Ajoutez d'autres codecs si nécessaire

# Utilisation de la fonction
url_video = "https://www.youtube.com/watch?v=S3tgmV-YmA8&ab_channel=GloriousLouange"
chemin_sortie = r"G:\Descargado"
telecharger_et_convertir(url_video, chemin_sortie, codecs)
