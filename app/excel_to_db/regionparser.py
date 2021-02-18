import re
import os

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


def readFile():
    path = os.path.join(os.path.expanduser('~'), 'Downloads','TERC_Adresowy_2021-02-09', 'TERC_Adresowy_2021-02-09.csv')
    with open(path,"r") as file:
        for line in file.readlines():
            yield line

def readFileMista():
    path = os.path.join(os.path.expanduser('~'), 'Downloads','SIMC_Adresowy_2021-02-09', 'SIMC_Adresowy_2021-02-09.csv')
    with open(path,"r") as file:
        for line in file.readlines():
            yield line

gminy = []
city = []
for i in readFile():
    if i.find("gmina")>0:
        split_text = i.split(";")
        w_num = split_text[0]
        p_num = split_text[1]
        g_num = split_text[2]
        name = split_text[4]
        category = split_text[5]
        number = int(g_num)+ 100*int(p_num)+100**2*int(w_num)
        gminy.append({"key":number,"name":name})
    if i.find("miasto")>0:
        split_text = i.split(";")
        w_num = split_text[0]
        p_num = split_text[1]
        g_num = split_text[2]
        name = split_text[4]
        category = split_text[5]
        if(w_num==''):
            w_num = 0
        if(p_num==''):
            p_num = 0
        if(g_num==''):
            g_num = 0
        number = int(g_num)+ 100*int(p_num)+100**2*int(w_num)
        city.append({"key":number,"name":name, "gmina":""})
pass


miasta = []
for i in readFileMista():
    if i.find("SYMPOD") > 0 or i=="\n":
        pass
    else:
        id = generateId(i)
        name = retriveName(i,6)
        gm = findObjectByKey(id,gminy)
        miasta.append({"key":id, "name":name, "gmina":gm})
    pass



# for iteam in city:
#     keys =[ i["key"] for i in gminy]
#     if iteam["key"] in keys :
#         name = ""
#         for i in gminy:
#             if i["key"]==iteam["key"]:
#                 name = i["name"]
#                 print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#             break
#         iteam["gmina"] = name

print(gminy)
