#!/usr/bin/python3

import models
from models.base import BaseModel, Base
from models.user import User
from models.category import Category
from models.transaction import Transaction
from models import storage
from sqlalchemy import DECIMAL

user = None

for u in storage.all(User).values():
    u.email = 'm@m.com'
    user = u

t1 = Transaction(amount=-1000,
                 description='test transaction',
                 created_at='2024-05-03T00:00:00.000')
t2 = Transaction(amount=-3000,
                 description='test transaction',
                 created_at='2024-10-03T00:00:00.000')
t3 = Transaction(amount=1000,
                 description='test transaction',
                 created_at='2024-04-03T00:00:00.000')
t4 = Transaction(amount=9500,
                 description='test transaction',
                 created_at='2024-12-03T00:00:00.000')

c1 = Category(name="food", description="food category")
c2 = Category(name="Ah media", description="media category")
user.add_category(c1)
user.add_category(c2)

user.add_transaction(t1, c1)
user.add_transaction(t2, c1)

user.add_transaction(t3, c2)
user.add_transaction(t4, c2)

models.storage.save()
print(user)
