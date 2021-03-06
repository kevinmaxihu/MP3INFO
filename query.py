#!/usr/bin/env python3

from urllib.request import urlopen, urlretrieve
from pathlib import Path
from bs4 import BeautifulSoup as bs

URL = 'http://mp3pn.info/search/s/f/'


def main(query):
	'''
    Main phase (calls to functions in namespace)
    '''
    _url = get_search_results(query)
    download(_url)


def get_search_results(query):
	'''
    Search results gathering phase
    '''
    query_to_url = URL + query.replace(' ', '+') + '/'
    query_opened = urlopen(query_to_url)
    html = bs(query_opened, "html.parser")
    _d = {}

    artists = html.findAll("i", {"class": "cplayer-data-sound-author"})
    songs = html.findAll("b", {"class": "cplayer-data-sound-title"})
    print(len(songs))
    print(len(artists))
    for i, item in enumerate(songs):
	    if i != 0 and i % 10 == 0:
		    print('Show 10 more?(y/n)')
	    response = input()
	    if response == 'n':
		    break

	_a = str(artists[i])
	_a = _a[37:][:-4]
	id_url = str(artists[i].find_next())[15:]
	id_tag = ''
	for character in id_url:
		if character != '/':
			id_tag += character
	    else:
		    break

	result = html.findAll("li", {"data-sound-id": id_tag})
	print()
	download_url = result[0]['data-download-url']
	print(str(i + 1) + ' - ' + _a)
	_s = str(songs[i])
	_s = _s[36:][:-4].replace('&amp;', '&')
	_d[str(i + 1)] = (download_url, "{} - {}.mp3".format(_a, _s))
	print('\t{}'.format(_s))
	print()

    print('END.')
    print()
    print('Item to download: ')
    item = input()

    return _d[item]


def download(url):
	'''
    Download phase
    '''
    found = False
    while found is False:
	    print()
	print()
	print('Destination directory: ')
	destination = input()
	print()
	destination = destination.replace("~/", str(Path.home()) + '/')
	if destination[len(destination) - 1] != '/':
		destination += '/'
	print()
	try:
		print('DOWNLOADING')
	    print()
	    urlretrieve(url[0], destination + url[1])
	    print("DOWNLOADED")

	    print('\t--> {}'.format(destination + url[1]))
	    found = True
	except FileNotFoundError:
		print('''Destination not found.
	    \nDoes directory {} exist?'''.format(destination))
