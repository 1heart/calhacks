db.drop_all()
db.create_all()

user1 = User('yixin', 'hellohello123', 'someemail1@gmail.com')
user2 = User('tom', 'hellohello123', 'someemail2@gmail.com')


db.session.add(user1)
db.session.add(user2)

db.session.commit()

db.session.add(transaction)

transaction = Transaction(user1, user2, 10, 'lol nice transaction', 'asdfasdf')

user1.payment_transactions.append(transaction)

db.session.commit()

db.session.query(User).first()