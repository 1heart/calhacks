# for heroku
from os import environ

import sqlite3 as lite
import sys

from sqlalchemy import *

from flask import Flask
from flask import render_template, flash, redirect, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import (LoginManager, login_required, 
					login_user, logout_user, current_user)

import datetime

app = Flask(__name__)

WTF_CSRF_ENABLED = True
app.secret_key='u_can_do_this'

DATABASE_URL= 'postgres://ieenbbnixbzymg:hj-gOvHaZzt-j1omubQAfglW3m@ec2-54-225-201-25.compute-1.amazonaws.com:5432/d9k47r8f72smi'
api_code = '9cb12b7c-e9bd-4bf8-b7ff-64b26d85a895'

# IF it's heroku, try will work
try:
	app.config['SQLALCHEMY_DATABASE_URI'] = environ['HEROKU_POSTGRESQL_GOLD_URL']
	db = SQLAlchemy(app)
	SQLALCHEMY_DATABASE_URI = 'HEROKU_POSTGRESQL_GOLD_URL'

# Otherwise use SQLite locally
except KeyError:
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/info.db'
	db = SQLAlchemy(app)
	SQLALCHEMY_DATABASE_URI = 'sqlite:///db/info.db'
	print("using sqlite")
print( "success connect to db ")

# login manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

from models import *
from forms import *

@app.route('/index', methods=["GET", "POST"])
@app.route('/', methods=["GET", "POST"])
def index():
	# render the forms
	register_form= RegisterForm()
	login_form = LoginForm()

	if request.method=='POST':
		# registration
		if register_form.validate_on_submit():

			if len(register_form.password.data) < 10:
				flash('Password is not long enough')
				return redirect('/')

			print('register_form validated')

			# create a new user object
			user = User(register_form.name.data, 
						register_form.email.data, 
						register_form.password.data)

			existing_user = User.query.filter_by(email=login_form.email.data).first()
			if existing_user:
				flash("This email has already been registered")
				return redirect( '/' )
			user.make_wallet(user.password)
			# add user to db
			db.session.add(user)
			db.session.commit()

			# login this new user
			login_user(user)
			print( "logged in user" )

			return redirect('/home')

		# logging in form validation
		if login_form.validate_on_submit():

			print('Attempt login')

			#check for user in db
			user = User.query.filter_by(email=login_form.email.data).first()
			
			# if the passwords match
			if (user and login_form.password.data == user.password):
				
				# login the user
				login_user(user)

				print('logged in user: ')
				print(current_user)

				return redirect('/home')

			# user is not in our db! turn him baaaack
			elif not user:
				flash('Wrong Email/Password Combination')
				return redirect('/index')
		
		flash('All fields are required')
		return redirect('/index')

	return render_template('index.html',
							title='Hello',
							form=register_form,
							login_form=login_form,
							current_user=current_user)

@app.route('/profile')
def profile():
	likes = 0
	aliases = Alias.query.filter_by(user_id=current_user.id)
	for alias in aliases:
		likes = likes + alias.points
	return render_template( 'profile.html',
							likes=likes,
							current_user=current_user)

@app.route('/charge')
def charge():
	return render_template( 'charge.html')

@app.route('/pay', methods=['GET', 'POST'])
def pay():
	if request.method == 'POST':
		recipientId = request.form['recipientId']
		amount = request.form['amount']
		description = request.form['description']
		# transaction = Transaction()
		payer = current_user
		receiver = Alias.query.filter_by(alias_string=recipientId).first().user
		transaction = Transaction(payer, receiver, amount, description, receiver.address)
		try:
			db.session.add(transaction)
			db.session.commit()
			transaction.commit_transaction()
			return 'lol nice'
		except Exception as e:
			print(e)
			return 'transaction failed'
	return render_template( 'pay.html')

transactionUserDict = {}

@app.route('/vote', methods=['POST'])
def vote():
	if request.method == 'POST':
		if request.form['transactionId']:
			transactionId = request.form['transactionId']
			if transactionId not in transactionUserDict:
				transactionUserDict[transactionId] = []
			if current_user in transactionUserDict[transactionId]:
				return 'nah'
			else:
				transactionUserDict[transactionId].append(current_user)
				currTransaction = Transaction.query.filter_by(id=int(transactionId)).first()
				currTransaction.likes += 1
				db.session.commit()
				return 'lol nice'


@app.route('/aliases')
def alias():
	return json.dumps(map(lambda x: x.alias_string, Alias.query.all()))


@app.route('/settings')
def settings():
	return render_template( 'settings.html',
							current_user=current_user)

@app.route('/current_aliases')
@login_required
def current_aliases():
	aliases = Alias.query.filter_by(user_id=current_user.id)

	return render_template( 'aliases.html',
							title="Aliases",
							current_user=current_user,
							aliases=aliases)






@app.route('/home', methods=["GET", "POST"])
@login_required
def home():
	# render the forms
	register_form = RegisterForm()
	login_form = LoginForm()

	transaction_list = Transaction.query.all()
	for x in transaction_list:
		currDate = datetime.datetime.fromtimestamp(x.timestamp).strftime('%Y/%m/%d, %H:%M:%S')
		x.btc = x.amount // 400000.0
		x.time = currDate
	print(transaction_list)

	return render_template( 'home.html',
							title="Home",
							transaction_list=transaction_list,
							form=register_form,
							login_form=login_form,
							current_user=current_user)

@app.route("/logout")
def logout():
    logout_user()
    flash("You are now logged out.")
    return redirect('/')
    
# deals with unauthorized page access
@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    flash("You'll need to log in or sign up to access that page")
    return redirect('/')
