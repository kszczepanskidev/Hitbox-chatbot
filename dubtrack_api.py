from requests import get
import json
import time
import codecs

from clear_song_name import clear_song_name


def get_current_song_name():
    request = get('https://api.dubtrack.fm/room/huntownicy').text
    json_data = json.loads(request)

    current_song = json_data['data']['currentSong']

    if current_song is not None:
        return clear_song_name(current_song['name'])
    else:
        return ''


def get_dubtrack_song_name(chat_bot):
    chat_bot.current_song_name = get_current_song_name()
    if not chat_bot.current_song_name == chat_bot.previous_song_name:
        print('{} {}'.format(chr(9835), chat_bot.current_song_name))
        chat_bot.previous_song_name = chat_bot.current_song_name


def save_dubtrack_name_to_file(chat_bot):
    while True:
        get_dubtrack_song_name(chat_bot)
        with codecs.open('dubtracksong.txt', 'w', 'utf-8') as f:
            print(chat_bot.current_song_name, file=f)
        time.sleep(1)
