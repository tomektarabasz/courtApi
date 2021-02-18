def all_cities(db_ctx):
    all_cities=[]
    for city in db_ctx.cities.find().limit(10):
        all_cities.append(city)
    return all_cities


# def find_city_or_region(query_text,db,collection):
    
