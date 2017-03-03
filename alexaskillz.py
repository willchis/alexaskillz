import os
import urllib, json
from flask import Flask
from flask_ask import Ask, statement

app = Flask(__name__)
ask = Ask(app, '/')

@ask.intent('GiveRandomInfo')
def politics_fact():

    politics_title = 'neoconservatism'

    wiki_api = 'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles='
    json_reponse = read_from_url(wiki_api + politics_title)

    speech_text = json_reponse['extract']    

    return statement(speech_text)

def read_from_url(url):
    response = urllib.urlopen(url)
    return json.loads(response.read())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
