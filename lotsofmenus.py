
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User

engine = create_engine('sqlite:///categoryitemlist.db')
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

User1 = User(name="Sagar Gidde", email="sagar@gmail.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Menu for UrbanBurger
category1 = Category(user_id=1, category_name="Soccer")

session.add(category1)
session.commit()

category2 = Category(user_id=1, category_name="BasketBall")

session.add(category2)
session.commit()

category3 = Category(user_id=1,category_name="Baseball")

session.add(category3)
session.commit()

category4 = Category(user_id=1,category_name="Frisbee")

session.add(category4)
session.commit()

category5 = Category(user_id=1,category_name="Snowboarding")

session.add(category5)
session.commit()

category6 = Category(user_id=1,category_name="Rock Climbing")

session.add(category6)
session.commit()

category7 = Category(user_id=1,category_name="Foosball")

session.add(category7)
session.commit()

category8 = Category(user_id=1,category_name="Skating")

session.add(category8)
session.commit()

category9 = Category(user_id=1,category_name="Hockey")

session.add(category9)
session.commit()



item1 = Item(user_id=1, item_name="Footwear", description="""Soccer players should play in turf shoes or cleats special                  footwear made exclusively for soccer.These shoes provide better traction on grass, which increases players                  ability to stay on their feet.The footwear material makes kicking a ball painless and provides some protection              against getting stepped on.Younger kids are usually limited to turf shoes but when a player gets older he or              she is allowed to wear cleats.""", category=category1)

session.add(item1)
session.commit()

#item2 = Item(user_id=1, item_name="Goggles", description="Juicy grilled veggie patty with tomato mayo and lettuce",
#                     category=category5)
#
#session.add(item2)
#session.commit()
#
#item3 = Item(user_id=1, item_name="Snowboard", description="Juicy grilled veggie patty with tomato mayo and lettuce",
#                     category=category5)
#
#session.add(item3)
#session.commit()
#
#item4 = Item(user_id=1, item_name="Two shinguards", description="Juicy grilled veggie patty with tomato mayo and lettuce",
#                     category=category1)
#
#session.add(item4)
#session.commit()
#
#item5 = Item(user_id=1, item_name="Shinguards", description="Juicy grilled veggie patty with tomato mayo and lettuce",
#                     category=category1)
#
#session.add(item5)
#session.commit()
#
#item6 = Item(user_id=1, item_name="Frisbee", description="Juicy grilled veggie patty with tomato mayo and lettuce",
#                     category=category4)
#
#session.add(item6)
#session.commit()
#
#item7 = Item(user_id=1, item_name="Bat", description="Juicy grilled veggie patty with tomato mayo and lettuce",
#                     category=category3)
#
#session.add(item7)
#session.commit()
#
#item8 = Item(user_id=1, item_name="Jersey", description="Juicy grilled veggie patty with tomato mayo and lettuce",
#                     category=category1)
#
#session.add(item8)
#session.commit()
#
#item9 = Item(user_id=1, item_name="Soccer Cleats", description="Juicy grilled veggie patty with tomato mayo and lettuce",
#                     category=category1)
#
#session.add(item9)
#session.commit()


