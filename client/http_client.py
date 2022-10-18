import os

import requests

server_url = os.getenv("SERVER_URL")

def random_req(subj):
    sess = requests.Session()
    url = f'{server_url}/random/{subj}'
    resp = sess.get(url)
    res = resp.json()

    return res

def search_req(subj, num, lang):

    sess = requests.Session()
    url = f'{server_url}/search/{subj}/{num}/{lang}'
    resp = sess.get(url)
    res = resp.json()
    return res

def translate_req(subj):
    sess = requests.Session()
    url = f'{server_url}/translate/{subj}'
    resp = sess.get(url)
    res = resp.json()
    print(res)
    return res

def trend_req():
    sess = requests.Session()
    url = f'{server_url}/trend'
    resp = sess.get(url)
    res = resp.json()
    dic = dict()
    key = 0
    for g in res:
        key= key+1
        dic[str(key)] = g
    return dic

def categories_tendor_req():
    sess = requests.Session()
    url = f'{server_url}/categories'
    resp = sess.get(url)
    res = resp.json()

    return res

