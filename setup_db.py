db.drop_all()
db.create_all()

user1 = User('yixin', 'hellohello123', 'asdf@gmail.com')
user2 = User('tom', 'hellohello123', 'fdsa@gmail.com')


db.session.add(user1)
db.session.add(user2)

db.session.commit()

transaction = Transaction(user1, user2, 804149, 'lol nice transaction', user2.address)


db.session.add(transaction)


user1.payment_transactions.append(transaction)

db.session.commit()

db.session.query(User).first()

alias1 = Alias("lol1alias", user1)
alias2 = Alias("lol2alias", user1)

db.session.add(alias1)
db.session.add(alias2)
db.session.commit()

# 

user1 = User.query.all()[0]
user2 = User.query.all()[1]
transaction = Transaction(user1, user2, 804149, 'lol nice transaction', user2.address)
transaction.commit_transaction()



