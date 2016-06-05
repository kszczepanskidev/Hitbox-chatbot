import _thread
import os
import getpass
import time

import dubtrack_api
import hitbox_api

__author__ = 'Krysztal'

class ChatBot:
    url = 'https://api.hitbox.tv/'

    login = ''
    password = ''
    channel_name = ''
    test = 1

    current_song_name = ''
    previous_song_name = ''

    hitbox_api = None

    def __init__(self):
        if os.path.isfile('settings.data'):
            self.load_settings_from_file()
        else:
            self.prompt_user_settings()

        self.hitbox_api = hitbox_api.HitboxAPI(self)
        time.sleep(3)

        os.environ["REQUESTS_CA_BUNDLE"] = 'cacert.pem'
        # os.system('chcp 65001')
        os.system('cls')
        print("Welcome to huntaBot by Kryształ\t\tv0.2 pre-alpha\n")

        _thread.start_new_thread(dubtrack_api.save_dubtrack_name_to_file, (self,))
        _thread.start_new_thread(self.hitbox_api.hitbox_chat_receiver, ())

    def save_settings_to_file(self):
        with open('settings.data', 'w') as f:
            print(self.login, file=f)
            print(self.password, file=f)
            print(self.channel_name, file=f)

    def load_settings_from_file(self):
        with open('settings.data', 'r') as f:
            self.login = f.readline().replace('\n', '')
            self.password = f.readline().replace('\n', '')
            self.channel_name = f.readline().replace('\n', '')

    def prompt_user_settings(self):
        self.login = input('Login: ')
        self.password = input('Password: ')   # getpass.getpass('Password: ')
        self.channel_name = input('Channel: ')
        self.save_settings_to_file()


if __name__ == '__main__':
    bot = ChatBot()

    while True:
        pass
