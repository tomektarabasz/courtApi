from starlette.routing import request_response
from .mongo_queries.mongo_queries import all_cities, find_city_by_query, find_court_by_city_id
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
    "http://localhost:4200"
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
def prezent_all():
    return all_cities(db)

@app.get("/{cityName}", response_model=List[CityEntity])
def find_city(cityName):
    return find_city_by_query(db,cityName)

@app.get("/court/{cityId}", response_model=List[CourtEntity])
def find_court(cityId):
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
