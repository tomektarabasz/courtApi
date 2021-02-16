def all_cities(db_ctx):
    all_cities=[]
    # iteams=[]
    # for iteam in db_ctx.courtCollection.find():
    #     iteams.append(iteam)
    for city in db_ctx.cities.find():
        all_cities.append(city)
    return all_cities
    # return iteams


# def find_city_or_region(query_text,db,collection):
    
