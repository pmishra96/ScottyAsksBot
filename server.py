# coding: utf-8

import warnings
import os
from flask import Flask, request

import chatbot
import messenger

app = Flask(__name__)

FACEBOOK_TOKEN = "EAACuFoER6pQBALD28OyaQcsowXgg5XAgbqj55ONxINleZA20sA87b93NVzwlxjvLUkIPeZB9ZCeDbXZCKZCXSjV5QaLV2gT9lWTdJ7eSiNLB880EyW4inaZCALiXWkZBWDzNgTUjnx7naNhM1OHxtZCScEFJGK7MAaQEZCH1kVPflDQZDZD"
bot = None

@app.route('/verify', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token', '') == "scotty_asks_project_2016":
        return request.args.get('hub.challenge', '')
    else:
        return 'Error, wrong validation token'

@app.route('/verify', methods=['POST'])
def webhook():
    payload = request.get_data()
    for sender, message in messenger.messaging_events(payload):
        print "Incoming from %s: %s" % (sender, message)

        response = bot.respond_to(message)

        print "Outgoing to %s: %s" % (sender, response)
        messenger.send_message(FACEBOOK_TOKEN, sender, response)

    return "ok"

# if __name__ == '__main__':
#     # Suppress nltk warnings about not enough data
#     warnings.filterwarnings('ignore', '.*returning an arbitrary sample.*',)

#     if os.path.exists("corpus.txt"):
#         bot = chatbot.Bot(open("corpus.txt").read())

#     app.run(port=5000, debug=True)
