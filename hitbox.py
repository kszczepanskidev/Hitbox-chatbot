import requests, thread, json, time, random
from websocket import create_connection

__author__ = 'Krysztal'

colors = ['FF00FF','0000FF','00FFFF','00FF00','FFFF00','FF0000',]

def ws_response():
    websocket = create_connection('ws://' + server_address + 'websocket/' + websocket_id)
    while True:
        response = websocket.recv()
        if response[0] == '2':
            websocket.send(response)
        time.sleep(30)

def chat_message(msg):
    ws.send('5:::{"name":"message","args":[{"method":"chatMsg","params":{"channel":"' + channel_name + '","name":"WcaleNieKrysztal", "nameColor":"' + random.choice(colors) + '","text":"' + msg + '"}}]}')

url = 'https://api.hitbox.tv/'
login_data = {'login': 'WcaleNieKrysztal', 'pass': 'dupa1234', 'rememberme': 'true'}


r = requests.post(url + 'auth/token', data=json.dumps(login_data))
token = r.text.split("\"")[3]

chat_servers = requests.get(url + 'chat/servers').text
chat_servers = json.loads(chat_servers)
server_address = chat_servers[0]['server_ip'] + '/socket.io/1/'

websocket_id = requests.get('http://' + server_address).text.split(':')[0]
ws = create_connection('ws://' + server_address + 'websocket/' + websocket_id)
ws.recv()

thread.start_new_thread(ws_response, ())


channel_name = raw_input('Enter channel name: ')

chat_login = '5:::{"name":"message","args":[{"method":"joinChannel","params":{"channel":"' + channel_name + '","name":"WcaleNieKrysztal", "token":"' + token + '","isAdmin":false}}]}'
ws.send(chat_login)

while True:
    msg = raw_input('#')
    if msg == 'exit':
        break
    else:
        chat_message(msg)

ws.close()