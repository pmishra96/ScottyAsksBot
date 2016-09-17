import random
import re
# import nltk

class Bot(object):
    def __init__(self, text, first_name, last_name, btc_value, btc_address):
		self.andrewID = None
		self.fbid = fbid
		self.user = User(first_name,last_name,btc_value,btc_address)

    def respond_to(self, message):
		if self.user.question_id != None:
			return send_answer(message)
		listOfProfile = []
		for word in message:
			if word.startswith("#"):
				listOfProfile.append(word)
		if listOfProfile!=[]:
			send_hashtags(listOfProfile)
			return "Thank you for the information!"
		if  (self.andrewID==""):
			return "Welcome to ScottyAsks :) Please enter your AndrewID to begin."
		if re.search(r'^\$+$|^money$|^btc$|^bitcoin$',message):
			return handle_btc()
		if re.search(r'^withdraw$',message):
			return widthraw()
		match = re.findall(r'address (\w+)',message)
		if len(match) > 0:
			return change_address(address)
		if re.search(r'^#',message):
			handle_hastag(message)
		if re.search(r'AskMe|Ask Me|ask me|askme',message):
			return ask_question()
		
	def send_hashtags(self, hashtags):
    	"""Send the message text to recipient with id recipient.
    	"""
    	r = requests.post(URL + "/users/fb/" + self.fbid + "/update",
        	params={},
        	data=json.dumps({
            	"hashtags": hashtags
        	}),
		print r.text

	def handle_btc(self):
		return "Hi " + self.user.first_name + ". You have " + self.user.bitcoin_value + " BTC in your wallet.\n" + "Would you like to widthdraw or change BTC address?\nTo widthraw, type withdraw\nTo change address, type address <new-address>"

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
		r = requests.get(URL + "/users/fb" + self.fbid + "/question")
		question_dict = json.loads(str(r.text))
		self.user.question_asked = true
    	self.user.question_id = question_dict["question_id"]
		self.user.question_text = question_dict["question_text"]
		return question_dict["question_text"]
	
	def send_answer(self,message)
		r = requests.post(URL + "/users/fb" + fbid + "/question",params = {"question_id" : question_id,"answer_text" = text})
		#if r.status_code != requests.codes.ok:
        	#print (r.text)
		self.user.question_id = None
		self.user.question_txt = None
		return r.text

class User(object):
	def __init__(first_name,last_name,btc_value,btc_address):
		self.first_name = first_name
		self.last_name = last_name
		self.btc_value = btc_value
		self.btc_address = btc_address
		self.question_id = None
		self.question_text = None
	

#     def _format_response(self, content):
#         def to_unicode(x):
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
