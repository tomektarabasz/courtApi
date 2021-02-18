import math
from pymongo.common import _CaseInsensitiveDictionary
from helpers import connect_to_mongo_db
client, db = connect_to_mongo_db()

def tt():
    for i,city in enumerate(db.cities.find()):
        if i<97000 :    
            name = city["name"]
            key=city["key"]
            provinceId = math.floor(key/(100**2))*100**2
            powiatId = math.floor(key/100)*100
            gminaId = key

            provinceName = db.administrationStructure.find_one({"key":provinceId})["name"]
            powiatName = db.administrationStructure.find_one({"key":powiatId})["name"]
            gminaName = db.administrationStructure.find_one({"key":key})["name"]

            #update 
            # print(city)
            print(provinceName)
            city2 = db.cities.update_one({"_id":city["_id"]},{"$set":{"wojewodztwo":provinceName,"powiat":powiatName, "gmina":gminaName}})
            # print(city2)

            if gminaId == 146511 or True:
                print("city")
                print(city)
                print(city["_id"])
                print(provinceId)
                print(powiatId)
                print(gminaId)
                print(provinceName)
                print(powiatName)
                print(gminaName)
                print("//////")
            # print(i)
