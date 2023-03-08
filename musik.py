from yandex_music import Client
import config
import time
from threading import Thread, Event

from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtCore import QUrl


client = Client(config.MUS_TOKEN).init()



def play(name, player, a = False, num = 0):
    
    if download(name, a, num) == False:
        return False

    player.setMedia(QMediaContent(QUrl.fromLocalFile('now.mp3')))
    player.play()
   


def download(name, a, num):
    try:
        if not a:
            search = client.search(name, nocorrect = True)
            track = search.tracks.results[num]
        else:
            search = client.search(name, type_ = 'artist')
            track = search.artists.results[0].get_tracks().tracks[num]
        

        track.get_download_info()
       
        track.download(filename = 'now.mp3', bitrate_in_kbps=track.download_info[0]['bitrate_in_kbps'])

    except:
        return False


