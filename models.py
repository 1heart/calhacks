import requests
from app import api_code 
from app import db
from blockchain import createwallet

import time

import json

class User(db.Model):

	"""The database for current users"""
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), unique=True)
	password = db.Column(db.String(80))
	wallet_password = db.Column(db.String(80))
	guid = db.Column(db.String(80)) 
	email = db.Column(db.String(80)) 
	link = db.Column(db.String(80)) 
	address = db.Column(db.String(80)) 


	aliases = db.relationship('Alias', 
						backref = 'user', 
						lazy='dynamic')

	payment_transactions = db.relationship('Transaction',
								backref='payer',
                                lazy='dynamic')

	def get_receiving_transactions(self):
		return Transaction.query.filter('receiver_id=' + str(self.id)).all()

	def get_payment_transactions(self):
		return Transaction.query.filter('payment_id=' + str(self.id)).all()

	def __init__(self, name, password, email):

		print( "Generating user" )
		self.email = email
		self.name = name
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
			if (requested.status_code == 200):
				print("wallet successfully made")
				request_dict = json.loads(requested.text)
				self.guid = request_dict['guid']
				self.address = request_dict['address']
				self.link = request_dict['link']
				return json.dumps(requested.json())	
			else:
				print("failed to make wallet")
		except Exception as e:
			print(e)


	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.id)

	def __repr__(self):
		return '<User %r>' % self.email

class Transaction(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	amount = db.Column(db.Integer)

	timestamp = db.Column(db.Integer)

	payer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	receiver_id = db.Column(db.Integer)
	
	receiver_address = db.Column(db.String(240))
	description = db.Column(db.String(240)) 

	likes = db.Column(db.Integer)


	def __init__(self, payerUser, receiverUser, amount, description, receiver_address):
		self.payer_id = payerUser.id
		self.receiver_id = receiverUser.id
		self.amount = amount
		self.description = description
		self.receiver_address  = receiver_address
		self.timestamp = time.time()

	def get_payer(self):
		return User.query.filter('id='+str(self.payer_id)).first()

	def get_receiver(self):
		return User.query.filter('id='+str(self.receiver_id)).first()


	def commit_transaction(self):
		data = {'main_password': wallet_password, 'to': receiver_address, 'amount': amount}
		headers = {'Content-Type':'application/x-www-form-urlencoded'}

		try:
			requested = requests.post(
				'https://blockchain.info/merchant/' + self.get_payer.guid + '/', 
				data=data,
				headers=headers)
			if (requested.status_code == 200):
				print("transaction successfull")
				request_dict = json.loads(requested.text)
				return json.dumps(requested.json())	
			else:
				print("failed to make transaction")
		except Exception as e:
			print(e)

class Alias(db.Model): 
	id = db.Column(db.Integer, primary_key=True) 
	alias_string = db.Column(db.String(80), unique=True) 
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	points = db.Column(db.Integer)

	def get_user(self):
		return User.query.filter('id='+str(self.user_id)).first()

	def __init__(self, alias_string, user):
		self.alias_string = alias_string
		self.user_id = user.id
		self.points = 0
		self.get_user().aliases.append(self)


