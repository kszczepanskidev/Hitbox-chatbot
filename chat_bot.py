import _thread
import os
import getpass
import time

import hitbox_api
import command

__author__ = 'Krysztal'


class ChatBot:
    url = 'https://api.hitbox.tv/'

    login = ''
    password = ''
    channel_name = ''

    plugdj_email = ''
    plugdj_password = ''
    plugdj_room = ''

    current_song_name = ''
    previous_song_name = ''

    do_whisper = None
    do_repeat = None
    repeatable_message = open('repeat_msg.data', 'r', encoding='iso-8859-2').readline().replace('\n', '')
    music_service = ''

    commands = {}
    all_commands = []

    hitbox_api = None
    gui = None

    logo = """
     _   _             _       ______       _
    | | | |           | |      | ___ \     | |  \tv0.2 alpha by {}
    | |_| |_   _ _ __ | |_ __ _| |_/ / ___ | |_ 
    |  _  | | | | '_ \| __/ _` | ___ \/ _ \| __|\tChannel:  {}
    | | | | |_| | | | | || (_| | |_/ / (_) | |_ \tUsername: {}
    \_| |_/\__,_|_| |_|\__\__,_\____/ \___/ \__|\n"""

    def __init__(self):
        if os.path.isfile('settings.data'):
            self.load_settings_from_file()
        else:
            self.prompt_user_settings()

        self.commands = command.load_commands()
        self.all_commands = ', '.join(list(self.commands.keys()))

        print('Connecting to Hitbox...')
        self.hitbox_api = hitbox_api.HitboxAPI(self)
        print('Connected')
        time.sleep(3)

        os.environ["REQUESTS_CA_BUNDLE"] = 'cacert.pem'
        os.system('cls' if os.name == 'nt' else 'clear')

        print(self.logo.format(__author__, self.channel_name, self.login))

        if self.music_service == 'dubtrack':
            import dubtrack_api
            _thread.start_new_thread(dubtrack_api.save_dubtrack_name_to_file, (self,))
        elif self.music_service == 'plugdj':
            import plugdj_api
            _thread.start_new_thread(plugdj_api.save_plugdj_name_to_file, (self,))

        _thread.start_new_thread(self.hitbox_api.hitbox_chat_receiver, ())

        if self.do_repeat:
            self.hitbox_api.message_repeater()

    def save_settings_to_file(self):
        with open('settings.data', 'w') as f:
            print('login:' + self.login, file=f)
            print('password:' + self.password, file=f)
            print('channel:' + self.channel_name, file=f)
            print('repeat:' + self.channel_name, file=f)
            print('whisper:' + self.channel_name, file=f)
            print('music_service:' + self.music_service, file=f)
            print('plugdj_email:' + self.plugdj_email, file=f)
            print('plugdj_password:' + self.plugdj_password, file=f)
            print('plugdj_room:' + self.plugdj_room, file=f)

    def load_settings_from_file(self):
        with open('settings.data', 'r') as f:
            self.login = f.readline().replace('\n', '').split(':')[1]
            self.password = f.readline().replace('\n', '').split(':')[1]
            self.channel_name = f.readline().replace('\n', '').split(':')[1]
            self.do_repeat = f.readline().replace('\n', '').split(':')[1] == 'true'
            self.do_whisper = f.readline().replace('\n', '').split(':')[1] == 'true'
            self.music_service = f.readline().replace('\n', '').split(':')[1]
            self.plugdj_email = f.readline().replace('\n', '').split(':')[1]
            self.plugdj_password = f.readline().replace('\n', '').split(':')[1]
            self.plugdj_room = f.readline().replace('\n', '').split(':')[1]

    def prompt_user_settings(self):
        self.login = input('Login: ')
        self.password = getpass.getpass('Password: ')
        self.channel_name = input('Channel: ')
        print('Current msg for repeating: {} (Can change in repeat_msg.data)'.format(self.repeatable_message))
        self.do_repeat = input('Enable repeating message every 2 minutes? (Y|N): ').upper() == 'Y'
        self.do_whisper = input('Enable anonymous whispering? (Y|N): ').upper() == 'Y'
        self.music_service = input('Enter name of music service? (dubtrack|plugdj): ').lower()
        if self.music_service == 'plugdj':
            self.plugdj_email = input('Plugdj email: ')
            self.plugdj_password = getpass.getpass('Plugdj password: ')
            self.plugdj_room = input('Plugdj room: ')
        self.save_settings_to_file()


if __name__ == '__main__':
    bot = ChatBot()

    try:
        while True:
            pass
    except:
        os.system('cls' if os.name == 'nt' else 'clear')
        quit()
