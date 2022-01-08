import re
import os

def readFile():
    path = os.path.join(os.path.expanduser('~'), 'listaSadow', 'listaSadow.txt')
    with open(path,"r") as file:
        for line in file.readlines():
            yield line

def writeMongoCommand(listaCommand):
    path = os.path.join(os.path.expanduser('~'), 'listaSadow', 'dbPopulate.txt')
    with open(path,"w") as file:
        for i in listaCommand:
            file.write(i)
            file.write("\n")


court_name = "TT"
s = "Sąd Rejonowy w Wysokiem Mazowieckiem dla miasta Skarżysko-Kamienna oraz gmin: Bliżyn, Łączna, Skarżysko Kościelne i Suchedniów"

def takeBiggerIndex(index, list_of_indexes):
    for item in list_of_indexes:
        if index < item:
            return item
    return None

def takeString(s,start,stop):
    if stop:
        return s[start:stop]
    else:
        return s[start:]

def getCourtName(s:str):
    index_for = s.find("dla")
    court_name = takeString(s, 0,index_for)
    return court_name

def separate(s:str):
    index_city = s.find("miasta")
    index_region = s.find("gmina")
    index_city_part = s.find("dzielnic")
    indexes = [index_city,index_region,index_city_part]
    city = takeString(s,index_city,takeBiggerIndex(index_city,indexes))
    region = takeString(s,index_region,takeBiggerIndex(index_region,indexes))
    city_parts = takeString(s,index_city_part,takeBiggerIndex(index_city_part,indexes))
    # for item in twoString:
    #     if item.find("miast")>0:
    #         city=item
    #     elif item.find("dzielnic")>0:
    #         region = item
    #     else:
    #         dzielnic = item
    #     print(dzielnica)
    return {"city":city,"region":region, "city_parts": city_parts}

def generateListOfResults(s:str):
    strings= separate(s)
    citys = regexCreateArray(strings["city"])
    regions = regexCreateArray(strings["region"])
    city_parts = regexCreateArray(strings["city_parts"])
    return {"citys":citys,"regions":regions, "city_parts":city_parts}
    

def regexCreateArray(s):
    return re.findall(r"\b[A-ZŚĆĘŻŹ]\w+",s)

def createMongoCommand(s):
    name = getCourtName(s)
    generatedResults=generateListOfResults(s)
    citys = generatedResults["citys"]
    regions = generatedResults["regions"]
    city_parts = generatedResults["city_parts"]
    template = 'db.courtCollection.insert({{name:"{}", level:"rejonowy", coverCitys:{} coverRegions:{}, coverCityParts:{}}})'.format(name,citys,regions,city_parts)
    return template

def createObjToInsert(s):
    name = getCourtName(s)[0:-1]
    generatedResults=generateListOfResults(s)
    citys = generatedResults["citys"]
    regions = generatedResults["regions"]
    city_parts = generatedResults["city_parts"]
    obj = {"name":name, "level":"rejonowy", "coverCitys":citys, "coverRegions":regions, "coverCityParts":city_parts}
    return obj


# createMongoCommand(s)

# separate(s)

# readFile()
from random import randint
from pymongo import MongoClient

# client = MongoClient("192.168.1.143", 27017)
client = MongoClient("172.17.0.2", 27017)

db = client.dbs
def createInputToMongoDb():
    arrayWithCommands = []
    for line in readFile():
        comand = createMongoCommand(line)
        arrayWithCommands.append(comand)
        obj=createObjToInsert(line)
        print(obj)
        db.courtCollection.insert_one(obj)
    writeMongoCommand(arrayWithCommands)
    pass

# createInputToMongoDb()
# print(createObjToInsert(s))

def createCourtCollection():
    for i,line in enumerate(readFile()):
        # print(line)
        index = line.find(";")
        court_name = line[:index]
        wlasciwosc = line[index+5:]
        print(court_name)
        print(wlasciwosc)
        updateResult=db.court.update_one({"name":court_name},{"$set":{"coverArea":wlasciwosc}})
        print(updateResult)

        # if(i>10):
        #     return "koniec"
    pass

createCourtCollection()