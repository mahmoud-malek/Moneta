#!/usr/bin/python3

import models
from models.base import BaseModel, Base
from models.user import User
from models.category import Category
from models.transaction import Transaction

# reload
models.storage.reload()

# delete everthing
for k, v in models.storage.all().items():
    models.storage.delete(v)

models.storage.save()

# create a user
u1 = User()
u1.name = "okokok"
u1.email = "okokok@gmail.com"
u1.password = "password"

# save the user
u1.save()

# create a category
c1 = Category()
c1.name = "food"
c1.user_id = u1.id

# save the category
c1.save()

# create a transaction

t1 = Transaction(amount=1000, description="test transaction")
t2 = Transaction(amount=1000, description="test transaction")
t3 = Transaction(amount=1000, description="test transaction")
t4 = Transaction(amount=1000, description="test transaction")

u1.add_transaction(t1, c1)
u1.add_transaction(t2, c1)
u1.add_transaction(t3, c1)
u1.add_transaction(t4, c1)

c1.save()

print(c1.transactions)
# save the transaction

c1.delete()
print(c1.transactions)
# check if they are deleted
print('--------------- deleting -------------------')

# print(models.storage.all(User))
# print(models.storage.all(Category))
# print(models.storage.all(Transaction))


# save changes
models.storage.save()
