import re
import os

from helpers import connect_to_mongo_db, generateId, readFile

path = os.path.join(os.path.expanduser('~'), 'Downloads','TERC_Adresowy_2021-02-09', 'TERC_Adresowy_2021-02-09.csv')


def createObjToInsert(line):
    if line.find("NAZWA_DOD")>0 or line=="\n":
        return None
    else:
        key = generateId(line)
        split_text = line.split(";")
        name = split_text[4]
        category = split_text[5]
        return {"key":key,"name":name, "category":category}
    pass

client, db = connect_to_mongo_db()
def createInputToMongoDb():
    for line in readFile(path):
        obj=createObjToInsert(line)
        print(obj)
        if not obj == None:
            db.administrationStructure.insert_one(obj)
    pass

createInputToMongoDb()
# print(createObjToInsert())