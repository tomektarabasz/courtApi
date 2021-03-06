from datetime import datetime
from bson.objectid import ObjectId
import json

from pymongo.pool import is_ip_address

def all_cities(db_ctx):
    all_cities=[]
    for city in db_ctx.cities.find().limit(10):
        all_cities.append(city)
    return all_cities

def find_city_by_query(db_ctx, cityQuery):
    all_cities=[]
    for city in db_ctx.cities.find({"name":{ "$regex": cityQuery, "$options": 'i' }}).limit(150):
        all_cities.append(city)
    return all_cities

def find_city_by_city_id(db_ctx, city_id):
    for city in db_ctx.cities.find({"_id":ObjectId(city_id)}).limit(1):
        return(city)
    return None

def find_court_by_city_id(db_ctx, city_id):
    all_courts=[]
    city = db_ctx.cities.find_one({"_id":ObjectId(city_id)})
    if(not city):
        return all_courts
    courts = db_ctx.court.find({"$or":[{"coverArea":{"$regex": city["name"], "$options": 'i' }},{"coverArea":{"$regex": city["gmina"], "$options": 'i' }}]})
    if(courts):
        for court in courts:
            coverArea = court["coverArea"]
                
        all_courts.append(court)
    print(all_courts)
    return all_courts

def statistic_info(db_ctx, ip_adress, **kwargs):
    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    json_ip_adress = json.dumps(ip_adress)
    ip_user = db_ctx.ip_statistic.find_one({"ip_adress":json_ip_adress})
    json_kwargs = json.dumps({**kwargs})
    if(ip_user):
        db_ctx.ip_statistic.update_one({"ip_adress":ip_adress},{"$push":{"requests":{"time":now,"params":json_kwargs}}})
    else:
        db_ctx.ip_statistic.insert_one({"ip_adress":ip_adress,"requests":[{"time":now,"params":json_kwargs}]})
    print(ip_adress)
    print(ip_user)
    return ip_user

# def find_city_or_region(query_text,db,collection):
    
