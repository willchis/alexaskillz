import os
from flask import Flask
from flask_ask import Ask, statement

app = Flask(__name__)
ask = Ask(app, '/')

@ask.intent('GiveRandomInfo')
def hello():
    speech_text = "Neoconservatism is a branch of conservatism"
    return statement(speech_text)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
