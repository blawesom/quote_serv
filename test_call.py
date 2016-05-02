# encoding: utf-8

import requests

site = 'http://127.0.0.1:8008'

allthems = requests.get(url='{0}/api/themes'.format(site))
print(allthems.json())

quote = requests.get(url='{0}/api/random'.format(site))
print(quote.json())

nquote = requests.post(url='{0}/api/quote'.format(site), json={'theme': 'Absence'})
print(nquote.json())
