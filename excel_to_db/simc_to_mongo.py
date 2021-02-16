import re
import os

from helpers import connect_to_mongo_db, generateId, readFile

path = os.path.join(os.path.expanduser('~'), 'Downloads','SIMC_Adresowy_2021-02-09', 'SIMC_Adresowy_2021-02-09.csv')


def createObjToInsert(line):
    if line.find("SYMPOD")>0 or line=="\n":
        return None
    else:
        key = generateId(line)
        split_text = line.split(";")
        name = split_text[6]
        return {"key":key,"name":name}
    pass

client, db = connect_to_mongo_db()
def createInputToMongoDb():
    for line in readFile(path):
        obj=createObjToInsert(line)
        print(obj)
        if not obj == None:
            db.cities.insert_one(obj)
            pass
    pass

createInputToMongoDb()
# print(createObjToInsert())