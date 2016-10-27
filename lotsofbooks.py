from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, BookItem, User

engine = create_engine('sqlite:///categorybookwithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Test User", email="testmail@gmail.com",
             picture='https://lh3.googleusercontent.com/-YSAuXnt9FRA/TviaoLUmxII/AAAAAAAAACU/ggL9qoOvsiMDBNG3r3wO6N_DqFJs6203wCEw/w140-h139-p/Photo%2B275.jpg')
session.add(User1)
session.commit()

category1 = Category(user_id=1, name="Biographies")
session.add(category1)
session.commit()


bookItem1 = BookItem(user_id=1,
                     name="The Flea - The Amazing Story of Leo Messi",
                     description="The captivating story of soccer legend Lionel Messi, from his first touch at age five in the streets of Rosario, Argentina, to his first goal on the Camp Nou pitch in Barcelona, Spain. The Flea tells the amazing story of a boy who was born to play the beautiful game and destined to become the world's greatest soccer player.",
                     year="2013",
                     author="Michael Part",
                     category=category1)

session.add(bookItem1)
session.commit()

bookItem2 = BookItem(user_id=1,
                     name="Stephen Curry: The Inspiring Story of One of Basketball's Sharpest Shooters",
                     description="An Amazon Best Seller, Stephen Curry: The Inspiring Story of One of Basketball's Sharpest Shooters, outlines the inspirational story of one of basketball's premier point guards, Stephen Curry. Stephen Curry has had an electrifying basketball career playing in the National Basketball Association. In this Stephen Curry biography, we will learn about how Steph became the star point guard that he is today. Starting first with his childhood and early life, we'll learn about Steph Curry prior to entering the NBA, his time in the NBA, along with his impact on the communities of Davidson College and Golden State. Steph Curry's success is not an accident.",
                     year="2014",
                     author="Clayton Geoffreys",
                     category=category1)

session.add(bookItem2)
session.commit()


category1 = Category(user_id=1, name="Business & Money")
session.add(category1)
session.commit()
category1 = Category(user_id=1, name="Children's Books")
session.add(category1)
session.commit()
category1 = Category(user_id=1, name="Computers")
session.add(category1)
session.commit()
category1 = Category(user_id=1, name="Cookbooks")
session.add(category1)
session.commit()
category1 = Category(user_id=1, name="Hobbies")
session.add(category1)
session.commit()
category1 = Category(user_id=1, name="Education")
session.add(category1)
session.commit()
category1 = Category(user_id=1, name="History")
session.add(category1)
session.commit()
category1 = Category(user_id=1, name="Law")
session.add(category1)
session.commit()
category1 = Category(user_id=1, name="Literature & Fiction")
session.add(category1)
session.commit()
category1 = Category(user_id=1, name="Medical Books")
session.add(category1)
session.commit()
category1 = Category(user_id=1, name="Mystery, Thriller")
session.add(category1)
session.commit()
category1 = Category(user_id=1, name="Parenting & Relationships")
session.add(category1)
session.commit()
category1 = Category(user_id=1, name="Politics")
session.add(category1)
session.commit()
category1 = Category(user_id=1, name="Religion")
session.add(category1)
session.commit()
category1 = Category(user_id=1, name="Science & Math")
session.add(category1)
session.commit()
category1 = Category(user_id=1, name="Science Fiction & Fantasy")
session.add(category1)
session.commit()
category1 = Category(user_id=1, name="Sports")
session.add(category1)
session.commit()
category1 = Category(user_id=1, name="Travel")
session.add(category1)
session.commit()



print "added book items!"
