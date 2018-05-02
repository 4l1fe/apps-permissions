import requests
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, wait as wait_fs
from config import ICONS_DIR


def _save_category_icon(category, link):
    try:
        response = requests.get(link+'=s20-rw')
        with open(ICONS_DIR + '/' + category, 'wb') as file:
            file.write(response.content)
        print('icon is written', category)
    except:
        from traceback import print_exc
        print_exc()


def save_icons(links, wait=False):
    p = Path(ICONS_DIR)
    p.mkdir(exist_ok=True)

    for file in p.iterdir():
        if file.name in links:
            links.pop(file.name)

    with ThreadPoolExecutor() as executor:
        fs = [executor.submit(_save_category_icon, c,l) for c,l in links.items()]

    if wait:
        wait_fs(fs, timeout=5)


def get_permissions(id_, hl):
    link = 'https://play.google.com/_/PlayStoreUi/data?ds.extension=163726509&f.sid=-7680408152843123462&hl={}' \
           '&soc-app=121&soc-platform=1&soc-device=1&authuser=0&_reqid=257542&rt=c'.format(hl)
    data = {'f.req': '[[[163726509,[{"163726509":[[null,["'+id_+'",7],[]]]}],null,null,0]]]',  # KeyError 163726509
            'at': 'AFdERMI8toQXkWI5A-OTOaE2f6F4:1525165140887'}

    response = requests.post(link, data=data)
    perms = response.text
    perms = perms[perms.find('{'):perms.rfind('}')+1]
    perms = (json.loads(perms))
    data, links = {}, {}
    for perm in perms['163726509'][0]:
        if perm:
            category = perm[0]
            data[category] = [item[1] for item in perm[2]]
            links[category] = perm[1][3][2]

    save_icons(links)

    return data


# get_permissions('org.telegram.messenger', 'en')