import time
import requests


def random_req(subj):
    sess = requests.Session()
    url = f'https://safe-island-73854.herokuapp.com/random/{subj}'
    resp = sess.get(url)
    res = resp.json()

    return res

def search_req(subj, num):
    sess = requests.Session()
    url = f'https://safe-island-73854.herokuapp.com/search/{subj}/{num}/en'
    resp = sess.get(url)
    res = resp.json()
    print(type(res))
    return res

def translate_req(subj):
    sess = requests.Session()
    url = f'https://safe-island-73854.herokuapp.com/translate/{subj}'
    resp = sess.get(url)
    res = resp.json()
    print(res)
    return res

def trend_req():
    sess = requests.Session()
    url = f'https://safe-island-73854.herokuapp.com/trend'
    resp = sess.get(url)
    res = resp.json()
    dic = dict()
    key = 0
    for g in res:
        key= key+1
        dic[str(key)] = g
    return dic

