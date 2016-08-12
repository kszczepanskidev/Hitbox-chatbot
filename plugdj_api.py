import requests
import json
import time
import codecs

from clear_song_name import clear_song_name

# TODO:
#   Login and room joining error handling


def get_current_song_name(chat_bot):
    with requests.session() as s:
        r = s.get('https://plug.dj/')
        csrf = r.text.split('_csrf="')[1].split("\"")[0]
        # print("CSRF: " + csrf)

        r = s.post('https://plug.dj/_/auth/login', json={'csrf': csrf, 'email': chat_bot.plugdj_email, 'password': chat_bot.plugdj_password})
        # print("Login: \n" + r.text)

        r = s.post('https://plug.dj/_/rooms/join', json={'slug': chat_bot.plugdj_room})
        # print("RoomJoin: \n" + r.text)

        r = s.get('https://plug.dj/_/rooms/state')

        try:
            response = json.loads(r.text)['data'][0]['playback']['media']
            current_song = '{} - {}'.format(response['author'], response['title'])
            return clear_song_name(current_song)
        except:
            return ''


def get_plugdj_song_name(chat_bot):
    chat_bot.current_song_name = get_current_song_name(chat_bot)
    if not chat_bot.current_song_name == chat_bot.previous_song_name and chat_bot.current_song_name != "":
        print('{} {}'.format(chr(9835), chat_bot.current_song_name))
        chat_bot.hitbox_api.chat_message("{} Na plugdju gra {}".format(chr(9835), chat_bot.current_song_name))
        chat_bot.previous_song_name = chat_bot.current_song_name


def save_plugdj_name_to_file(chat_bot):
    while True:
        get_plugdj_song_name(chat_bot)
        with codecs.open('plugdjsong.txt', 'w', 'utf-8') as f:
            print(chat_bot.current_song_name, file=f)
        time.sleep(5)
