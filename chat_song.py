import requests, _thread, json, time, os, random, getpass
from websocket import create_connection

__author__ = 'Krysztal'

# os.environ["REQUESTS_CA_BUNDLE"] = 'cacert.pem'
url = 'https://api.hitbox.tv/'
login = 'HuntaBot'  # input('Login: ')
password = 'dupa1234' # getpass.getpass()
channel_name = 'hantaa' # input('Enter channel name: ')
previous_song = ''


def ws_response():
        websocket = create_connection('ws://' + server_address + 'websocket/' + websocket_id)
        while True:
            try:
                response = websocket.recv()
                if response[0] == '2':
                    websocket.send(response)
                time.sleep(1)
            except:
                print('EXCEPTION')
                list = json.loads(requests.get(url + 'chat/servers').text)
                server = list[random.randint(0, len(list) - 1)]['server_ip'] + '/socket.io/1/'
                ws_id = requests.get('http://' + server_address).text.split(':')[0]
                websocket = create_connection('ws://' + server + 'websocket/' + ws_id)
                websocket.recv()
                time.sleep(5)


def chat_message(msg):
    try:
        ws.send('5:::{"name":"message","args":[{"method":"chatMsg","params":{"channel":"' + channel_name + '","name":"' + login + '","nameColor":"FF0000","text":"' + msg + '"}}]}')
    except:
        print('EXCEPTION')
        list = json.loads(requests.get(url + 'chat/servers').text)
        server = list[random.randint(0, len(list) - 1)]['server_ip'] + '/socket.io/1/'
        ws_id = requests.get('http://' + server_address).text.split(':')[0]
        websocket = create_connection('ws://' + server + 'websocket/' + ws_id)
        previous_song = ''
        websocket.recv()

def clear_song_name(song):
    song = song.replace('&apos;', '\'')
    song = song.replace('[OFFICIAL]', '')
    song = song.replace('[OFFICIAL VIDEO]', '')
    song = song.replace('[OFFICIAL MUSIC VIDEO]', '')
    song = song.replace('[Official]', '')
    song = song.replace('[Official Video]', '')
    song = song.replace('[Official Music Video]', '')
    song = song.replace('[Lyrics]', '')
    song = song.replace('[Lyrics Video]', '')
    song = song.replace('[Lyrics]', '')
    song = song.replace('[Lyrics video]', '')
    song = song.replace('- Lyrics', '')
    song = song.replace('[ORIGINAL]', '')
    song = song.replace('[ORIGINAL VIDEO]', '')
    song = song.replace('[ORIGINAL MUSIC VIDEO]', '')
    song = song.replace('[Original]', '')
    song = song.replace('[Original Video]', '')
    song = song.replace('[Original Music Video]', '')
    song = song.replace('[Uncensored]', '')
    song = song.replace('(OFFICIAL)', '')
    song = song.replace('(OFFICIAL VIDEO)', '')
    song = song.replace('(OFFICIAL MUSIC VIDEO)', '')
    song = song.replace('(Official)', '')
    song = song.replace('(Official Video)', '')
    song = song.replace('(Official Music Video)', '')
    song = song.replace('(Lyrics)', '')
    song = song.replace('(Lyrics Video)', '')
    song = song.replace('(Lyrics)', '')
    song = song.replace('(Lyrics video)', '')
    song = song.replace('(ORIGINAL)', '')
    song = song.replace('(ORIGINAL VIDEO)', '')
    song = song.replace('(ORIGINAL MUSIC VIDEO)', '')
    song = song.replace('(Original)', '')
    song = song.replace('(Original Video)', '')
    song = song.replace('(Original Music Video)', '')
    song = song.replace('(Uncensored)', '')
    return song


login_data = {'login': login, 'pass': password, 'rememberme': 'true'}

r = requests.post(url + 'auth/token', data=json.dumps(login_data))
token = r.text.split("\"")[3]

chat_servers = json.loads(requests.get(url + 'chat/servers').text)
server_address = chat_servers[random.randint(0, len(chat_servers) - 1)]['server_ip'] + '/socket.io/1/'

websocket_id = requests.get('http://' + server_address).text.split(':')[0]
ws = create_connection('ws://' + server_address + 'websocket/' + websocket_id)
ws.recv()

_thread.start_new_thread(ws_response, ())

chat_login = '5:::{"name":"message","args":[{"method":"joinChannel","params":{"channel":"' + channel_name + '","name":"' + login + '", "token":"' + token + '","isAdmin":false}}]}'
ws.send(chat_login)
time.sleep(5)

os.system('cls')
print("Welcome to huntaBot by Kryształ\t\t\tv0.1 pre-alpha build 0666\n\n")
chat_message('Huntwieczór wszystkim :D //')

while True:
    r = requests.get('https://api.dubtrack.fm/room/huntownicy').text
    dubtrack_json = json.loads(r)

    current_json = dubtrack_json['data']['currentSong']

    if current_json is not None:
        current_song = clear_song_name(current_json['name'])

        if not current_song == previous_song:
            chat_message('Teraz na dubtracku gra: ' + current_song)
            print('Teraz na dubtracku gra ' + current_song)
            previous_song = current_song

    time.sleep(5)

ws.close()

#Characters to fix
#AC/DC - Rock &apos;n Roll Train (FULL HD)
# ąę (probably all polish characters)