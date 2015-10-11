db.drop_all()
db.create_all()

user1 = User('yixin', 'yixin1996@gmail.com', 'hellohello123')
user2 = User('tom', 'weirdotomli@gmail.com', 'hellohello123')
transaction = Transaction()

user1.payment_transactions.append(transaction)
# user2.receiving_transactions.append(transaction)

db.session.add(user1)
db.session.add(user2)
db.session.add(transaction)

db.session.commit()

db.session.query(User).first()
