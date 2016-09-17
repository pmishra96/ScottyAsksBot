import random
import requests
import re
import json
# import nltk

URL = "http://ac958344.ngrok.io"
class Bot(object):
	def __init__(self):
		self.andrewID = None
		self.fbid = None
		self.user = User()

	def respond_to(self, message):
		print "RESPOND TO STARTS"
		if self.user.question_id != None:
			return self.send_answer(message)
		listOfProfile = []
		for word in message:
			if word.startswith("#"):
				listOfProfile.append(word)
		if listOfProfile!=[]:
			self.send_hashtags(listOfProfile)
			return "Thank you for the information!"
		if  (self.andrewID==""):
			return "Welcome to ScottyAsks :) Please enter your AndrewID to begin."
		if re.search(r'^\$+$|^money$|^btc$|^bitcoin$',message):
			return self.handle_btc()
		if re.search(r'^withdraw$',message):
			return self.widthraw()
		match = re.findall(r'address (\w+)',message)
		if len(match) > 0:
			return self.change_address(address)
		if re.search(r'^#',message):
			return self.handle_hastag(message)
		if re.search(r'AskMe|Ask Me|ask me|askme',message):
			return self.ask_question()

	def send_hashtags(self, hashtags):
		"""Send the message text to recipient with id recipient.
		"""
		r = requests.post(URL + "/users/fb/" + self.fbid + "/update",
			params={},
			data=json.dumps({
				"hashtags": hashtags
			}), headers={'Content-type': 'application/json'})
		print (r.text)

	def handle_btc(self):
		self.user.btc_value = "0.1235"
		self.user.first_name = "Ryan"
		return "Hi " + self.user.first_name + ". You have " + self.user.btc_value + " BTC in your wallet.\n" + "Would you like to widthdraw or change BTC address?\nTo widthraw, type withdraw\nTo change address, type address <new-address>"

	def withdraw(self):
		r = rquests.post(URL + "/users/fb/:" + fbid + "/update",
			params={},
			data=json.dumps({
				"btc_value": 0
			}),
		headers={'Content-type': 'application/json'})
		return "You have successfully withdrawn " + self.user.btc_value + " BTC to the address: " + self.user.btc_address

	def change_address(self, btc_address):
		r = rquests.post(URL + "/users/fb/:" + fbid + "/update",
			params={},
			data=json.dumps({
				"btc_address": btc_address
			}),
		headers={'Content-type': 'application/json'})
		return "You have successfully changed your btc address to " + btc_address

	def ask_question(self):
		r = requests.get(URL + "/users/fb/" + self.fbid + "/question")
		question_dict = json.loads(str(r.text))
		self.user.question_id = question_dict["id"]
		self.user.question_text = question_dict["text"]
		return self.user.question_text

	def send_answer(self,message):
		r = requests.post(URL + "/users/fb/" + self.fbid + "/question",
			params = {"question_id" : self.user.question_id,"answer_text" : self.user.question_text})
		#if r.status_code != requests.codes.ok:
			#print (r.text)
		self.user.question_id = None
		self.user.question_txt = None
		return "Thanks!"

class User(object):
	def __init__(self):
		self.first_name = None
		self.last_name = None
		self.btc_value = None
		self.btc_address = None
		self.question_id = None
		self.question_text = None


#     def _format_response(self, content):
#         def to_	unicode(x):
#             if isinstance(x, str):
#                 return x.decode('utf-8')
#             return x

#         s = u' '.join([to_unicode(c) for c in content])
#         s = re.sub(r' ([\?,\.:!])', r'\1', s)  # Remove spaces before separators
#         return s
#     def _format_response(self, content):
#         def to_unicode(x):
#             if isinstance(x, str):
#                 return x.decode('utf-8')
#             return x

#         s = u' '.join([to_unicode(c) for c in content])
#         s = re.sub(r' ([\?,\.:!])', r'\1', s)  # Remove spaces before separators
#         return s
