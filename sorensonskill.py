import os
import urllib, json
from random import randint

from flask import Flask
from flask_ask import Ask, statement, question

app = Flask(__name__)
ask = Ask(app, '/')


@ask.launch
def launched():
    return question("Welcome to the Sorenson skill.  From here you can trigger Bamboo builds or deployments.  Would you like to hear a list of possible build plans?")

@ask.intent('YesOrNoFIrstIntent', mapping={ 'answer': 'yesorno' })
def yes_or_no(answer):
    statement('Okay')
    if(answer == 'yes'):  
        return politics_fact()
    else:
        return

@ask.intent('RunBambooPlan', mapping={ 'plan', 'Plan' })
def run_plan():

    #TODO add headers to ensure wiki api allows access

    title = get_random_politics_title()
    statement(title.encode('utf-8'))

    title = urllib.quote(title) # encode to include in url

    wiki_api = 'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles='
    json_reponse = read_from_url(wiki_api + title)

    introduction = ''
        
    try:
        pages = json_reponse['query']['pages']
        for key in pages.keys():
            print 'wiki page ref: ' + key
            introduction = pages[key]['extract']

    except:
        print 'Error thrown when using title: ' + title
        politics_fact()
        return
        
    return statement(introduction.encode('utf-8'))

def read_from_url(url):
    response = urllib.urlopen(url)
    return json.loads(response.read())

def get_available_build_plans():
    return [ 'integration', 'unit', 'smoke']

if __name__ == '__main__':
    politics_fact()

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
