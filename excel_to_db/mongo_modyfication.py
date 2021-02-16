from helpers import connect_to_mongo_db


client, db = connect_to_mongo_db()

for i,city in enumerate(db.cities.find()):
    print(i)
