from urllib.request import urlopen
import json

def read_json_internet(url):
    data = []
    try:
        url_respone = urlopen(url)
        data = json.loads(url_respone.read().decode())
    except Exception as ex:
        print(ex)
    return data
