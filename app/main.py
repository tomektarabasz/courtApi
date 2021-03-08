from starlette.requests import Request
from .mongo_queries.mongo_queries import statistic_info, all_cities, find_city_by_city_id, find_city_by_query, find_court_by_city_id
from .my_types.my_types import CityEntity, File, CourtEntity
from .helpers import connect_to_mongo_db
from fastapi import FastAPI, params
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware

client, db = connect_to_mongo_db()
app = FastAPI()
origins = [
    "https://localhost:4200",
    "http://localhost:4200",
    "http://192.168.1.143:8000",
    "http://192.168.1.17:4200",
    "http://192.168.1.17:80",
    "http://192.168.1.17:8000",
    "http://89.65.210.136/*",
    ]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return({"id":"This is incrediable"})

@app.get("/all", response_model=List[CityEntity])
def prezent_all(request:Request):
    statistic_info(db,ip_adress=request.client.host, url="/all")
    return all_cities(db)

@app.get("/{cityName}", response_model=List[CityEntity])
def find_city(cityName, request:Request):
    statistic_info(db,ip_adress=request.client.host, queryCityName=cityName, url="/{cityName}")
    return find_city_by_query(db,cityName)

@app.get("/city/{cityId}", response_model=CityEntity)
def find_court(cityId, request:Request):
    statistic_info(db,ip_adress=request.client.host,cityId=cityId,url="/city/{cityId}")
    return find_city_by_city_id(db,cityId)    

@app.get("/court/{cityId}", response_model=List[CourtEntity])
def find_court(cityId, request:Request):
    statistic_info(db,ip_adress=request.client.host,cityId=cityId,url="/court/{cityId}")
    return find_court_by_city_id(db,cityId)


# @app.post("/add/")
# def add_file(file: File):
#     db.append(file)
#     return(db[-1])

# @app.post("/add/{id}")
# def add_file(file: File, id):
#     file.id=id
#     db.append(file)
#     return(db[-1])

# @app.get("/test")
# def show_all_data():
#     db = client.filesTT
#     data = db.details.find()
#     datatt:tt.MongoFile = []
#     for i in data:
#         datatt.append(MongoFile(**i))
#     return({"data":datatt})
