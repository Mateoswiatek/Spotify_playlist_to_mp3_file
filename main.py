# -*- coding: utf-8 -*-

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import requests
from pytube import YouTube
from googleapiclient.discovery import build
import re
import os

api_key = ""

def spotify_to_list(link):
    client_id = ""
    client_secret = ""
    pattern = r'playlist/([a-zA-Z0-9]+)'
    playlist_id = re.findall(pattern, link)[0]
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    access_token = requests.post('https://accounts.spotify.com/api/token', data=data).json()['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}

    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    response = requests.get(url, headers=headers)
    data = response.json()
    tracks = data['items']
    track_names = [track['track']['name'] for track in tracks]
    print(track_names)
    # lista = ["""jesteś ładniejsza niż na zdjęciach""", """Bedoesiara""", """Koloska i szlugi"""]
    return track_names


def main():
    downlanding_path = "./Download"
    spoti_link = input("Link to Spitify playlist: ")
    service = build('youtube', 'v3', developerKey=api_key)
    list_song = spotify_to_list(spoti_link)
    print(f"pobieranie {len(list_song)} utworow")

    list_downloaded_song = [os.path.splitext(file)[0] for file in os.listdir(downlanding_path) if file.endswith('.mp3')]
    for song in list_song:
        if(song in list_downloaded_song):
            print(f"masz już pobrane: {song}")
            continue
        request = service.search().list(
            part="id",
            maxResults=1,
            type='video',
            q=song
        )
        response = request.execute()
        video_id = response['items'][0]['id']['videoId']
        print(f"Download {song} ...")
        YouTube(f"https://www.youtube.com/watch?v={video_id}").streams.get_audio_only().download(output_path=downlanding_path, filename=f"{song}.mp3")
        print(f"utwór {song} został pobrany!")


if __name__ == "__main__":
    main()
