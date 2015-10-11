import requests
from app import api_code 
from app import db
from blockchain import createwallet
from IPython import embed

import json

class User(db.Model):

	"""The database for current users"""
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), unique=True)
	email = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(80), unique=True)
	wallet_password = db.Column(db.String(80))
	guid = db.Column(db.String(80)) 
	link = db.Column(db.String(80)) 
	address = db.Column(db.String(80)) 


	def __init__(self, name, email, password):

		print( "Generating user" )

		self.name = name
		self.email = email
		self.password = password

	def is_authenticated(self):
		return True

	def make_wallet(self, password, private_key = None, label = None, email = None):
		self.wallet_password = password
		data = {'password':password, 'api_code':api_code}
		if (private_key):
			self.private_key = private_key
			data['priv'] = private_key
		if (label):
			self.label = label
			data['label'] = label
		if (email):
			self.email = email
			data['email'] = email

		headers = {'Content-Type':'application/x-www-form-urlencoded'}
		
		try:
			requested = requests.post(
				'https://blockchain.info/api/v2/create_wallet', 
				data=data,
				headers=headers)
			request_dict = json.loads(requested.text)
			self.guid = request_dict['guid']
			self.address = request_dict['address']
			self.link = request_dict['link']
			print("wallet successfully made")
			return json.dumps(requested.json())

		except Exception as e:
			print("Here is the exception, make_wallet")
			print(e)

		print("wallet successfully made")
		return json.dumps(request.json())

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.id)

	def __repr__(self):
		return '<User %r>' % self.email

