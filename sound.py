#! python
# -✳- coding: utf-8 -✳- 
import time
import pygame
import json
import requests
import sys
import shutil
import os.path

def requestPoint(x,y):
    # https://ty88avpuhl.execute-api.ap-northeast-1.amazonaws.com/prod/?x=1&y=2
    # https://kasahi.net/hd14/camera/touch.php?x=1&y=2
    url = "https://kasahi.net/hd14/camera/touch.php"
    # url = "https://ty88avpuhl.execute-api.ap-northeast-1.amazonaws.com/prod/"
    payload = {'x': x, 'y': y}
    headers = {"content-type": "application/json"}
    res = requests.get(url, params=payload,headers=headers)

    json = res.json()
    url = json["soundUrl"]
    download(url=url)
    
def download(url=None):
    print "url= %s" % url
    filename = url.rsplit('/', 1)[1].split('?')[0]
    filename = "./music/%s" % filename
    res = requests.get(url, stream=True)
    res.raw.decode_content = True
    save_binary(filename=filename, bin=res.raw)

def save_binary(filename, bin):
    if not os.path.isfile(filename):
        with open(filename, "wb") as fout:
            shutil.copyfileobj(bin, fout)
            # fout.write(bin)
            # fout.close()
    playMusic(filename)

def playMusic(filename):
    print "play start"
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(1)
    PLAY_END = pygame.USEREVENT
    pygame.mixer.music.set_endevent(PLAY_END)

    time.sleep(5) 
    print "play end"
if __name__ == '__main__':
        args = sys.argv
        requestPoint(x=args[1], y=args[2])
