import requests
import json
import random
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
            print('EXCEPTION - Could not send message, attempting to reset connection')
            self.connect_websocket()
            self.chat_bot.previous_song_name = ''

    def hitbox_chat_receiver(self):
        # self.chat_message("Avoiding hitbox spam security {}".format(random.randint(0, 100)))
        self.chat_message("Huntwieczór wszystkim!")
        while True:
            self.handle_message(self.websocket.recv())

    def handle_message(self, message):
        if message[0] == '1':
            pass
        elif message[0] == '2':
            self.websocket.send(message)
        else:
            message = message[4:].replace('["', '[').replace('"]', ']').replace('\\"', "\"")
            message = json.loads(message)
            message_type = message['args'][0]['method']

            if 'buffer' in message['args'][0]['params']:
                return
            if message_type == 'chatMsg':
                self.handle_user_message(message['args'][0]['params'])
            elif message_type == 'directMsg':
                self.handle_direct_message(message['args'][0]['params'])

    def handle_user_message(self, msg):
        message_text = msg['text']
        user_name = msg['name']
        is_subscriber = msg['isSubscriber']

        if user_name == "HuntaBot":
            return

        print("[CHAT]{}: {}".format(user_name, message_text))
        if message_text[0] == "!":
            self.handle_chat_command(message_text[1:], user_name, is_subscriber)

    def handle_chat_command(self, msg, user, sub):
        if msg == 'dubtrack':
            if self.chat_bot.current_song_name != "":
                self.chat_message('@{} teraz gra {}'.format(user, self.chat_bot.current_song_name))
            else:
                self.chat_message('@{} aktualnie na dubtracku nie leci żadna piosenka.'.format(user))

    def handle_direct_message(self, msg):
        message_text = msg['text']
        user_name = msg['from']
        channel = msg['channel']

        self.chat_message('@{} {}'.format(channel, message_text))
