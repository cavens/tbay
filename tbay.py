import random
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import logging
logging.basicConfig(filename="tbay.log", level=logging.DEBUG)


engine = create_engine('postgresql://action:action@localhost:5432/tbay')
Session = sessionmaker (bind=engine)
session = Session()
Base = declarative_base()

from datetime import datetime


#intermediary_table_1 = Table('table_name', Base.metadata,
#    Column('name', Integer, ForeignKey('name.id')),
#    Column('name', Integer, ForeignKey('name.id'))
#)


# Create items table
class Item(Base):
  __tablename__ = "items"
  
  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  description = Column(String)
  start_time = Column(DateTime, default=datetime.utcnow)
  
  user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
  bids = relationship("Bid", backref ="items")  
  
# Create users table
class User(Base):
  __tablename__="users"
  
  id = Column(Integer, primary_key=True)
  username = Column(String, nullable=False)
  password = Column(String, nullable=False)
  
  bids = relationship("Bid", backref ="users")
  items = relationship("Item", backref ="users")
  
# Create bids table
class Bid(Base):
  __tablename__="bids"
  
  id = Column(Integer, primary_key=True)
  price = Column(Float, nullable=False)
  
  user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
  item_id = Column(Integer, ForeignKey('items.id'), nullable=False)

  
Base.metadata.create_all(engine)



user1 = User(username="User1",password="Password1")
user2 = User(username="User2",password="Password2")
user3 = User(username="User3",password="Password3")

baseball = Item(name="Baseball",description="This is a white baseball", users=user1)


users = [user1, user2, user3]

logging.debug("pre for")
for user in users:
  bid = random.randint(50,200)
  logging.debug(bid)
  logging.debug(user.username)
  bid_now = Bid(price=bid)
  user.bids.append(bid_now)
  baseball.bids.append(bid_now)

session.add_all([user1, user2, user3, baseball])
session.commit()

logging.debug("pre highest")
highest = session.query(Bid.user_id).order_by(Bid.price.desc()).first()
logging.debug(highest)
print session.query(User.username).filter(User.id == highest).all()
print session.query(Bid.price).order_by(Bid.price.desc()).first()





