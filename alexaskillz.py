import os
import urllib, json
from random import randint

from flask import Flask
from flask_ask import Ask, statement

app = Flask(__name__)
ask = Ask(app, '/')

@ask.intent('GiveRandomInfo')
def politics_fact():

    #TODO add headers to ensure wiki api allows access

    title = get_random_politics_title()
    title = urllib.quote(title)

    wiki_api = 'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles='
    json_reponse = read_from_url(wiki_api + title)


    pages = json_reponse['query']['pages']

    introduction = ''

    try:
        for key in pages.keys():
            print key
            introduction = pages[key]['extract']

    except:
        print 'error thrown when using title: ' + title
        politics_fact()
        return

    print introduction.encode('utf-8')

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
    politics_fact()

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
