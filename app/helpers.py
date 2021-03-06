def generateId(s:str):
    splited = s.split(";")
    w_num = splited[0]
    p_num = splited[1]
    g_num = splited[2]
    if(w_num==''):
            w_num = 0
    if(p_num==''):
            p_num = 0
    if(g_num==''):
            g_num = 0
    return int(g_num)+ 100*int(p_num)+100**2*int(w_num)

def retriveName(s:str, name_position: int):
    if s =="\n":
        return ""
    splited = s.split(";")
    return splited[name_position]

def findObjectByKey(key, object_to_search):
    return_to_list = []
    for i in object_to_search:
        if i["key"] == key:
            return_to_list.append(i)
    return return_to_list

def readFile(path):
    with open(path,"r") as file:
        for line in file.readlines():
            yield line

from app.mongo_queries.mongo_queries import statistic_info
from pymongo import MongoClient
def connect_to_mongo_db():
    client = MongoClient("192.168.1.143", 27017)
    db = client.dbs
    return [client,db]