import requests, _thread, json, time, os, random, getpass
from websocket import create_connection

__author__ = 'Krysztal'

# os.environ["REQUESTS_CA_BUNDLE"] = 'cacert.pem'
url = 'https://api.hitbox.tv/'
login = ''  # input('Login: ')
# password = getpass.getpass()
previous_song = ''


def ws_response():
        websocket = create_connection('ws://' + server_address + 'websocket/' + websocket_id)
        while True:
            try:
                response = websocket.recv()
                if response[0] == '2':
                    websocket.send(response)
                time.sleep(5)
            except:
                list = json.loads(requests.get(url + 'chat/servers').text)
                server = list[random.randint(0, len(list) - 1)]['server_ip'] + '/socket.io/1/'
                ws_id = requests.get('http://' + server_address).text.split(':')[0]
                websocket = create_connection('ws://' + server + 'websocket/' + ws_id)
                websocket.recv()
                time.sleep(5)


def chat_message(msg):
    ws.send('5:::{"name":"message","args":[{"method":"chatMsg","params":{"channel":"' + channel_name + '","name": "' + login + '", "text":"' + msg + '"}}]}')
    print('Teraz na dubtracku gra ' + current_song)

login_data = {'login': input('Login: '), 'pass': getpass.getpass(), 'rememberme': 'true'}

r = requests.post(url + 'auth/token', data=json.dumps(login_data))
token = r.text.split("\"")[3]

chat_servers = json.loads(requests.get(url + 'chat/servers').text)
server_address = chat_servers[random.randint(0, len(chat_servers) - 1)]['server_ip'] + '/socket.io/1/'

websocket_id = requests.get('http://' + server_address).text.split(':')[0]
ws = create_connection('ws://' + server_address + 'websocket/' + websocket_id)
ws.recv()

_thread.start_new_thread(ws_response, ())


channel_name = input('Enter channel name: ')

chat_login = '5:::{"name":"message","args":[{"method":"joinChannel","params":{"channel":"' + channel_name + '","name":"' + login + '", "token":"' + token + '","isAdmin":false}}]}'
ws.send(chat_login)
time.sleep(5)

os.system('cls')
print("Welcome to huntaBot by Kryształ\t\t\tv0.1 pre-alpha build 0666\n\n")
chat_message('Huntwieczór widzowie streamu Hantaa')

while True:
    r = requests.get('https://api.dubtrack.fm/room/huntownicy').text
    dubtrack_json = json.loads(r)

    current_json = dubtrack_json['data']['currentSong']

    if current_json is not None:
        current_song = current_json['name']

        if not current_song == previous_song:
            chat_message('Teraz na dubtracku gra: ' + current_song)
            previous_song = current_song

    time.sleep(5)

ws.close()

#Characters to fix
#AC/DC - Rock &apos;n Roll Train (FULL HD)
# ąę (probably all polish characters)