import os
import time
import urllib, json
from random import randint

from flask import Flask
from flask_ask import Ask, statement, question

app = Flask(__name__)
ask = Ask(app, '/')

MAGIC_SEAWEED_KEY = 'e96ca9b1f03a627aaab136eafe4f83ee'
SPOT_ID = '1449'

@ask.launch
def launched():
    return question("The is the surf report for rest bay, porth call, South Wales.  Would you like today's surf report?").reprompt("I didn't get that. Would you like the current conditions?")

@ask.intent('YesOrNoFIrstIntent', mapping = { 'answer': 'yesorno' })
def yes_or_no(answer):
    statement('Okay')
    if (answer == 'yes'):  
        return surf_report('today')
    else:
        return

@ask.intent('SwellIntent', mapping = { 'report_time': 'timeofday'})
def current_surf(report_time):

    api_url = 'http://magicseaweed.com/api/%s/forecast/?spot_id=%s&fields=timestamp,swell.minBreakingHeight,swell.maxBreakingHeight,wind.speed, wind.compassDirection' % (MAGIC_SEAWEED_KEY, SPOT_ID)
    print 'Calling Magic Seaweed via API URL: ' + api_url
    json_reponse = read_from_url(api_url)

    unix_now = time.time()
    time_difference = 0
    closest_time = json_reponse[0]

    for item in json_reponse:
        item_time_difference = abs(item['timestamp'] - unix_now)

        if (item_time_difference <= time_difference):
            time_difference = item_time_difference
            closest_time = item

    min_swell = closest_time['swell']['minBreakingHeight']
    max_swell = closest_time['swell']['maxBreakingHeight']
    wind_speed = closest_time['wind']['speed']

    print 'Got swell heights: %d to %d ft and wind speed %d' % (min_swell, max_swell, wind_speed)
    return statement('Currently the swell height is between %d and %d foot at rest bay. The wind speed is %d miles per hour.' \
        % (min_swell, max_swell, wind_speed))

@ask.intent('BuildStatusIntent', mapping = { 'plan': 'Plan'})
def build_status(plan):
    # Use Bamboo API here to get 
    return statement('The latest %s build is red, with 4 failing tests.' % plan)

@ask.intent('CurrentAdvertIntent')
def current_advert():
    # Match advert based on DAR info and return related promo.
    return statement('That was the new Budweiser summer cider, available summer 2017.  Visit the Alexa app for a free sample.') \
    .standard_card(title='Budweiser Summer Cider', text='Claim your free sample..', large_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Bud_and_Budvar.jpg/1200px-Bud_and_Budvar.jpg')

#@ask.intent('GiveRandomInfo')
def politics_fact():

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

def get_random_politics_title():
    options = ['Anarchism',
        'Anarcho-capitalism',
        'Anarcho-primitivism',
        'Anarcho-syndicalism',
        'Anarchist communism',
        'Anti-communism',
        'Antidisestablishmentarianism',
        'Asian values',
        'Authoritarianism',
        'Bioregional democracy',
        'Black populism',
        'Black supremacy',
        'Bolivarian Revolution',
        'Capitalism',
        'Christian democracy',
        'Christian socialism',
        'Classical liberalism',
        'Classical republicanism',
        'Collectivism',
        'Communism',
        'Communitarianism',
        'Conservatism',
        'Corporatocracy',
        'Demarchy',
        'Democracy (varieties)',
        'Democratic egalitarianism',
        'Democratic peace theory',
        'Democratic socialism',
        'Democratic transhumanism',
        'Eco-socialism',
        'Egalitarianism',
        'Fascism',
        'Federalism',
        'Green anarchism',
        'Green politics',
        'Green syndicalism',
        'Hindu nationalism',
        'Individualist anarchism',
        'Integral humanism',
        'Islamism',
        'Isocracy',
        'Kemalist ideology',
        'Leftism',
        'Liberalism',
        'Libertarianism',
        'Libertarian socialism',
        'Localism',
        'Majoritarianism',
        'Marxism',
        'Marxism-Leninism',
        'Marxist philosophy',
        'Meritocracy',
        'Minarchism',
        'Minoritarianism',
        'Miscegenation',
        'Moderate Libertarianism','Monarchism','Nationalism','National Socialism','Neoliberalism','Pacifism','Paleolibertarianism','Patriotism','Political symbolism','Panislamism','Peronism','Populism','Post-Communism','Progressivism','Putinism','Racial purity','Racial segregation','Racialism','Radical centrism','Radical liberalism','Rationalism','Republicanism','Screen theory','Slavophile','Small-l libertarianism','Social Credit','Social democracy','Socialism','Social liberalism','Social philosophy','Sphere of influence','Stalinism','Thatcherism','Third Position','Totalitarianism','Tribalism','Trotskyism',
        'Utilitarianism' ]
    return options[randint(0, len(options) - 1)]

if __name__ == '__main__':
    #politics_fact()
    current_surf('today')

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
