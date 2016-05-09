from requests import get
import json
import os
from time import sleep

# os.environ["REQUESTS_CA_BUNDLE"] = 'cacert.pem'
prev_song = ''

while True:
    r = get('https://api.dubtrack.fm/room/huntownicy')
    json_data = json.loads(r.text)

    current_song = json_data['data']['currentSong']

    if current_song is not None:
        current_name = current_song['name']

        if not current_name == prev_song:
            f = open('dubtracksong.txt', 'w')
            print(current_name, file=f)
            print(current_name)
            prev_song = current_name
            f.close()
            sleep(60)

    sleep(1)



