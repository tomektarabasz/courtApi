from bson.objectid import ObjectId
def all_cities(db_ctx):
    all_cities=[]
    for city in db_ctx.cities.find().limit(10):
        all_cities.append(city)
    return all_cities

def find_city_by_query(db_ctx, cityQuery):
    all_cities=[]
    for city in db_ctx.cities.find({"name":{ "$regex": cityQuery, "$options": 'i' }}).limit(15):
        all_cities.append(city)
    return all_cities

def find_court_by_city_id(db_ctx, cityId):
    all_courts=[]
    city = db_ctx.cities.find_one({"_id":ObjectId(cityId)})
    if(not city):
        return all_courts
    print(city)
    print(city["name"])
    print(city["gmina"])
    court = db_ctx.court.find_one({"$or":[{"coverArea":{"$regex": city["name"], "$options": 'i' }},{"coverArea":{"$regex": city["gmina"], "$options": 'i' }}]})
    if(court):
        all_courts.append(court)
    print(all_courts)
    return all_courts

# def find_city_or_region(query_text,db,collection):
    
