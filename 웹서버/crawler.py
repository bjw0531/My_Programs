import requests


def gethtml(html):
    response = requests.get(html)
    return response.text
