# coding: utf-8

import warnings
import os
import json
from flask import Flask, request

import chatbot
import messenger

app = Flask(__name__)

FACEBOOK_TOKEN = os.environ['FACEBOOK_TOKEN']
bot = dict() # bot as key and fbid as value
dont_know_id_flag = false

@app.route('/', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token', '') == os.environ['scotty_asks_project_2016']:
        return request.args.get('hub.challenge', '')
    else:
        return 'Error, wrong validation token'

def bot_exists(sender_id):
    # checks if the bot exists in the database
    if (sender_id in bot):
        return true
    return false

@app.route('/', methods=['POST'])
def webhook():
    payload = request.get_data()
    for sender, message in messenger.messaging_events(payload):
        print ("Incoming from %s: %s") % (sender, message)
        user_info_dict = check_andrew_ID(sender)
        curr_user_andrew_ID = user_info_dict["andrewID"]
        if (bot_exists(sender)):
            # find existing bot set bot to it 
            curr_bot = bot(sender)
            curr_bot.text = message
        else:
        # create new bot with info received from get
            bot[sender].add(Bot(message,sender))
            curr_bot = bot[sender]
            curr_bot.user.first_name = user_info_dict["first_name"]
            curr_bot.user.last_name = user_info_dict["last_name"]

        curr_bot.andrewID = curr_user_andrew_ID     
        curr_bot.user.btc_value = user_info_dict["btc_value"]
        curr_bot.user.btc_address = user_info_dict["btc_address"]

        if curr_user_andrew_ID == "" && !dont_know_id_flag:
            response = "We don't know you. What is your Andrew ID?"
            dont_know_id_flag = true
        elif dont_know_id_flag:
            curr_user_andrew_ID = str(message)

            if(send_unknown_id(sender,curr_user_andrew_ID) == ""):
                curr_user_andrew_ID = ""
                dont_know_id_flag = true
            else:
                curr_bot.andrewID = curr_user_andrew_ID
                user_info_dict["andrewID"] = curr_user_andrew_ID
                dont_know_id_flag = false
        else:
            response = curr_bot.respond_to(message)

        print ("Outgoing to %s: %s") % (sender, response)
        messenger.send_message(FACEBOOK_TOKEN, sender, response)

    return "ok"



if __name__ == '__main__':
    app.run(port=5000, debug=True)

def check_andrew_ID(fbid):
    r = requests.get(URL + "/users/fb" + fbid)
    user_info_dict = {};
    if r.text == "":
        return {"andrewID":""}
    else:
        user_info_dict = json.loads(str(r.text))
    if r.status_code != requests.codes.ok:
        print (r.text)
    return user_info_dict

def send_unknown_id(fbid,andrewID):
    r = requests.post(URL + "/users/fb" + fbid,params = {"andrewID":andrewID})
    if r.status_code != requests.codes.ok:
        print r.text