from typing import List
from pydantic.types import PyObject
from pymongo import MongoClient


def generateId(s: str):
    splited = s.split(";")
    w_num = splited[0]
    p_num = splited[1]
    g_num = splited[2]
    if(w_num == ''):
        w_num = 0
    if(p_num == ''):
        p_num = 0
    if(g_num == ''):
        g_num = 0
    return int(g_num) + 100*int(p_num)+100**2*int(w_num)


def retriveName(s: str, name_position: int):
    if s == "\n":
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
    with open(path, "r") as file:
        for line in file.readlines():
            yield line


def connect_to_mongo_db():
    client = MongoClient("192.168.1.143", 27017)
    db = client.dbs
    return [client, db]


def split_string_of_cover_area(cover_area: str):
    city_area_index = safe_find_index(cover_area, "obszaru")
    city_area_index2 = safe_find_index(cover_area, "pomocniczych")
    city_index = safe_find_index(cover_area, "miasta")
    gmin_index = safe_find_index(cover_area, "gmin")
    index_array = [{"name": "city_area_index", "index": city_area_index}, {
        "name": "city_index", "index": city_index}, {"name": "gmin_index", "index": gmin_index}, {"name": "pomocnicze", "index": city_area_index2}]
    index_array.sort(key=lambda x: x.get("index"))
    extracted_strings = extract_substrings(
        string=cover_area, indexs=index_array)
    city_area = ""
    city = ""
    gmina = ""
    for item in extracted_strings:
        if(item["name"] == "city_area_index"):
            city_area = item["value"]
        elif(item["name"] == "city_index"):
            city = item["value"]
        elif(item["name"] == "gmin_index"):
            gmina = item["value"]
    return({"city_area": city_area, "city": city, "gmina": gmina})
    pass


def safe_find_index(string: str, query_string: str):
    try:
        index = string.index(query_string)
    except:
        index = -1
    return index
    pass


def extract_substrings(string: str, indexs):
    array = []
    for i, obj in enumerate(indexs):
        if(obj["index"] < 0):
            array.append({"name": obj["name"], "value": ""})
        else:
            start_index = obj["index"]
            try:
                end_index = indexs[i+1]["index"]
            except:
                end_index = -1
            array.append(
                {"name": obj["name"], "value": string[start_index:end_index]})
    return array
    pass
