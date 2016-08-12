import requests
import json
import random
import threading
import re

from datetime import datetime
from websocket import create_connection

__author__ = 'Krysztal'


class HitboxAPI:
    login = ''
    user_token = ''

    chat_bot = None
    websocket = None

    regex_url = re.compile(r'(?i)(http|ftp|https)?(:\/\/)?([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])?')

    def __init__(self, chatbot):
        self.chat_bot = chatbot
        self.hitbox_login()
        self.connect_websocket()
        self.chat_login()

    def hitbox_login(self):
        request = requests.post(self.chat_bot.url + 'auth/token', data=json.dumps(
            {'login': self.chat_bot.login, 'pass': self.chat_bot.password, 'rememberme': 'true'}))
        self.user_token = request.text.split('\"')[3]

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
        self.chat_message('Huntwieczór wszystkim huntKasa /')
        while True:
            self.handle_message(self.websocket.recv())

    def handle_message(self, message):
        if message[0] == '1':
            pass
        elif message[0] == '2':
            self.websocket.send(message)
        else:
            try:
                self.log_messages(message)
                message = message[4:].replace('["', '[').replace('"]', ']').replace('\\"', '\"')
                message = json.loads(message)
                message_type = message['args'][0]['method']
            except:
                return

            if 'buffer' in message['args'][0]['params']:
                return
            if message_type == 'chatMsg':
                self.handle_user_message(message['args'][0]['params'])
            elif message_type == 'directMsg':
                self.handle_direct_message(message['args'][0]['params'])
            elif message_type == 'chatLog':
                self.handle_chat_log(message['args'][0]['params']['text'])

    def handle_user_message(self, msg):
        message_text = msg['text']
        user_name = msg['name']
        is_subscriber = msg['isSubscriber']

        if user_name == 'HuntaBot':
            return

        if msg['role'] == 'anon' and self.check_timeout(message_text, user_name):
            print('[TIME]{}: {}'.format(user_name, message_text))
            return

        print('[CHAT]{}: {}'.format(user_name, message_text))

        if message_text[0] == '!':
            self.handle_chat_command(message_text[1:], user_name, is_subscriber)

    def handle_chat_command(self, msg, username, sub):
        if msg not in self.chat_bot.commands:
            msg = 'komendy'

        try:
            command = self.chat_bot.commands[msg]
        except:
            return

        if command.subonly and not sub:
            return

        temp = []
        for p in command.parameters:
            try:
                temp.append(eval(p))
            except:
                try:
                    temp.append(eval('self.' + p))
                except:
                    temp.append(eval('self.chat_bot.' + p))
        command.parameters = temp

        if command.message == '@{} teraz gra {}' and temp[1] == '':
            command.message = '@{} aktualnie nic nie gra'

        self.chat_message(command.message.format(*command.parameters))

    def handle_direct_message(self, msg):
        message_text = msg['text']
        # user_name = msg['from']
        channel = msg['channel']

        self.chat_message('@{} {}'.format(channel, message_text))

    def handle_chat_log(self, msg):
        if 'subscribed' in msg:
            username = msg[msg.index('>') + 1:msg[msg.index('>') + 1:].index('>')]

            self.chat_message(':metal: SUB HYPE :metal: Witamy nowego suba @{} :metal:'.format(username))


    def message_repeater(self):
        threading.Timer(120, self.message_repeater).start()
        self.chat_message(self.chat_bot.repeatable_message)

    def check_timeout(self, msg, user):
        if self.check_timeout_huntaedition(msg, user):
            return True

        if self.regex_url.search(msg):
            self.timeout_user(user, 60)
            self.chat_message('Proszę o nie wrzucanie linków na chat @{} [60s]'.format(user))
            return True

        if (sum(1 for c in msg if c.isupper()) / len(msg.strip().replace(' ', ''))) > 0.65 and len(msg.strip().replace(' ', '')) > 5:
            self.timeout_user(user, 30)
            self.chat_message('Proszę o nie pisanie CAPSEM @{} [30s]'.format(user))
            return True

        return False

    def check_timeout_huntaedition(self, msg, user):
        if user == 'Venans' and (msg[-1] == '.' or 'venans' in msg.lower()):
            self.timeout_user(user, 10)
            # self.chat_message('Anti-Venans Script Activated [10s]'.format(user))
            return True

        if user in ['SzaroBuryPies', 'Venans'] and any(x in msg.lower().replace('.', '') for x in ['szafa', 'szafeczka', 'szafunia']):
            self.timeout_user(user, 10)
            # self.chat_message('Anti-Szafa Script Activated [10s]'.format(user))
            return True

        return False


    def timeout_user(self, user, time=30):
        self.websocket.send('5:::{{"name":"message","args":[{{"method":"kickUser",'
                            '"params":{{"channel":"{}","name":"{}","token":"{}","timeout":"{}"}}}}]}}'.
                            format(self.chat_bot.channel_name, user, self.user_token, time))

    @staticmethod
    def log_messages(msg):
        now = datetime.now()
        try:
            with open('log_{}_{}_{}.txt'.format(now.day, now.month, now.year), 'a') as f:
                print(msg, file=f)
        except:
            return
