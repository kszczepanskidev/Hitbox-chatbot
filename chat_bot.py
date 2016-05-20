import requests
import _thread
import json
import time, os
import random
import getpass
from websocket import create_connection

import dubtrack_api

class ChatBot:
    url = 'https://api.hitbox.tv/'

    login = ''
    password = ''
    channel_name = ''

    current_song_name = ''
    previous_song_name = ''

    def __init__(self):
        if os.path.isfile('settings.data'):
            self.load_settings_from_file()
        else:
            self.prompt_user_settings()
        os.environ["REQUESTS_CA_BUNDLE"] = 'cacert.pem'
        _thread.start_new_thread(self.save_dubtrack_name_to_file, ())

        os.system('cls')
        print("Welcome to huntaBot by Kryształ\t\t\tv0.2 pre-alpha\n")

    def save_settings_to_file(self):
        with open('settings.data', 'w') as f:
            print(self.login, file=f)
            print(self.password, file=f)
            print(self.channel_name, file=f)

    def load_settings_from_file(self):
        with open('settings.data', 'r') as f:
            self.login = f.readline()
            self.password = f.readline()
            self.channel_name = f.readline()

    def prompt_user_settings(self):
        self.login = input('Login: ')
        self.password = input('Password: : ')   # getpass.getpass('Password: ')
        self.channel_name = input('Channel: ')
        self.save_settings_to_file()

    def get_dubtrack_song_name(self):
        self.current_song_name = dubtrack_api.get_current_song_name()
        if not self.current_song_name == self.previous_song_name:
            print('#' + self.current_song_name)
            self.previous_song_name = self.current_song_name

    def save_dubtrack_name_to_file(self):
        while True:
            self.get_dubtrack_song_name()
            with open('dubtracksong.txt', 'w') as f:
                print(self.current_song_name, file=f)
            time.sleep(1)

if __name__ == '__main__':
    bot = ChatBot()

    while True:
        pass