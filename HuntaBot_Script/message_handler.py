from ghost import Ghost
from bs4 import BeautifulSoup

g = Ghost()

with g.start() as session:
    page, extra_resources = session.open('https://plug.dj/huntownicy')
    result, resources = session.evaluate('API;')
    print(result)
    result, resources = session.evaluate('API.getMedia();')
    print(result)

    # with open('plugdj.txt', 'w') as f:
    #     print(page.content, file=f)
    # song = html.find('div', attrs={'id':'now-playing-media'}).text
    # print(song)