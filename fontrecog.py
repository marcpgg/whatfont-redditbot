
import requests
import json
from utils import API_KEY_WFI, JSONBIN_URL


def font_recog(img_url):

    try:
        headers = {'Content-Type': 'application/json'}
        data = {
       "FONT": {
          "API_KEY": API_KEY_WFI,
          "P": "1",
          "F": "1",
          "INFO": {
             "urlimage": img_url
             }
            }
        }
        # Jsonbin request
        reqbin = requests.put(JSONBIN_URL, json=data, headers=headers)
        jsonbin = reqbin.json()
        print("jsonbin.io updated, version: {}".format(jsonbin["version"]))
        json_url = JSONBIN_URL + "/" + str(jsonbin["version"])

        # Whatfontis Request
        response = requests.get("https://www.whatfontis.com/api/?file={}&limit=3".format(json_url))
        print ("Response Status code: {} \n".format(response.status_code))
        fonts_data = response.json()

        # returns list of markdown links to fonts.
        recog_fonts = ["[{}]({})".format(item["title"], item["url"])for item in fonts_data]
    except Exception as err:
        print ("\n\n Hey there was an error  {}".format(err))

        print("WhatFontIs API failed")
        recog_fonts = None


    return recog_fonts
