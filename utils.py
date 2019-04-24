import requests
import os
import pickle
from bs4 import BeautifulSoup



def load_commented():
	"""
	load pickled already commented comments and users.
	
	"""

    if not os.path.isfile("commented.pkl"):
        commented = []
    else:
        with open ('commented.pkl', 'rb') as fp:
            commented = pickle.load(fp)

    return commented


def img_url_parser(text):
"""
Img url parser, Returns None if there are no image urls
ugly function, todos: improve url check, less returns , etc.
"""
    # if selftexthtml passed is empty
    if text == None:
        return None

    # cheap check url
    if text.startswith('http'):
        try:
            resp = requests.get(text)

            if 'image/' in resp.headers['content-type']:
                # It is an iamge
                img_url = text
                return img_url

            else:
                # If text is url but not an image
                print('URL but not an image')
                return None
        except:
            print('GET failed')
            return None

    # Here is where we start  if we pass a selftexthtml , let's Find URLs in it
    soup = BeautifulSoup (text, 'html.parser')

    if not soup.find_all('a'): #there are no urls in text
        return None

    for url in soup.find_all('a'):
        # Al loro recursivismos
        img_url = img_url_parser(url.get('href'))

        if img_url != None:
            break

    return img_url