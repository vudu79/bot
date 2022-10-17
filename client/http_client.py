import requests


def random_req(subj):
    sess = requests.Session()
    url = f'https://aiogram-bot-golang-server.herokuapp.com/random/{subj}'
    resp = sess.get(url)
    res = resp.json()

    return res

def search_req(subj, num, lang):

    sess = requests.Session()
    url = f'https://aiogram-bot-golang-server.herokuapp.com/search/{subj}/{num}/{lang}'
    print(url)
    resp = sess.get(url)
    res = resp.json()
    print(type(res))
    return res

def translate_req(subj):
    sess = requests.Session()
    url = f'https://aiogram-bot-golang-server.herokuapp.com/translate/{subj}'
    resp = sess.get(url)
    res = resp.json()
    print(res)
    return res

def trend_req():
    sess = requests.Session()
    url = f'https://aiogram-bot-golang-server.herokuapp.com/trend'
    resp = sess.get(url)
    res = resp.json()
    dic = dict()
    key = 0
    for g in res:
        key= key+1
        dic[str(key)] = g
    return dic

