import requests
import json
import random
import _thread
from websocket import create_connection

__author__ = 'Krysztal'


class HitboxAPI:
    login = ''
    user_token = ''

    chat_bot = None
    websocket = None

    def __init__(self, chatbot):
        self.chat_bot = chatbot
        self.hitbox_login()
        self.connect_websocket()
        self.chat_login()

    def hitbox_login(self):
        request = requests.post(self.chat_bot.url + 'auth/token', data=json.dumps(
            {'login': self.chat_bot.login, 'pass': self.chat_bot.password, 'rememberme': 'true'}))
        print(request.text)
        self.user_token = request.text.split("\"")[3]

    def connect_websocket(self):
        chat_servers = json.loads(requests.get(self.chat_bot.url + 'chat/servers').text)
        server_address = chat_servers[random.randint(0, len(chat_servers) - 1)]['server_ip'] + '/socket.io/1/'

        websocket_id = requests.get('http://' + server_address).text.split(':')[0]
        self.websocket = create_connection('ws://' + server_address + 'websocket/' + websocket_id)

    def chat_login(self):
        chat_login = '5:::{{"name":"message","args":[{{"method":"joinChannel","params":' \
                     '{{"channel":"{}","name":"{}", "token":"{}","isAdmin":false}}}}]}}'\
                     .format(self.chat_bot.channel_name, self.chat_bot.login, self.user_token)
        self.websocket.send(chat_login)

    def chat_message(self, msg):
        try:
            self.websocket.send('5:::{{"name":"message","args":[{{"method":"chatMsg","params":'
                                '{{"channel":"{}","name":"{}","nameColor":"FF0000","text":"{}"}}}}]}}'
                                .format(self.chat_bot.channel_name, self.chat_bot.login, msg))
        except:
            # print('EXCEPTION')
            self.connect_websocket()
            self.chat_bot.previous_song_name = ''

    def hitbox_chat_receiver(self):
        while True:
            self.handle_message(self.websocket.recv())

    def handle_message(self, message):
        if message[0] == '1':
            pass
        elif message[0] == '2':
            self.websocket.send(message)
        else:
            message_type = json.loads(message[4:].replace('["', '[').replace('"]', ']').replace('\\"', "\""))
            message_type = message_type['args'][0]['method']
            print(message_type)
            pass

    def handle_user_message(self, msg):
        pass


#Characters to fix
# ąę (probably all polish characters)