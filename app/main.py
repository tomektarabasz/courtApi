import http
from starlette.requests import Request
from starlette.responses import Response
from .mongo_queries.mongo_queries import check_nick_availablity_db, create_user_db, find_user_id_db, statistic_info, all_cities, find_city_by_city_id, find_city_by_query, find_court_by_city_id, update_user_keytrack_id
from .my_types.my_types import CheckNickNameResponse, CheckUserIdentity, CheckUserIdentityResponse, CityEntity, CreateUserRequest, File, CourtEntity, UserCreationResponse, UserEntity
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
    "http://89.65.210.136:*",
    "http://89.65.210.136:8000",
    "*",
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

@app.get("/user/checknick/{nick}", response_model=CheckNickNameResponse)
def check_nick_availability(nick, request:Request):
    print(nick)
    isAvailable = check_nick_availablity_db(db,nick)
    result = CheckNickNameResponse()
    result.isNickAvailable=isAvailable
    return result

import requests
import json
@app.post("/user/create/", response_model=UserCreationResponse)
def create_user(request:CreateUserRequest):
    nick = request.nick
    password = request.password
    samples = request.sample
    result = UserCreationResponse()
    isAvailable = check_nick_availablity_db(db,nick)
    if not isAvailable:
        result.isCreated =False
        return result
    headers  = {"Authorization":"3c8a2da2-0a61-4684-99c7-ba39f976fe24"}
    response:Response = requests.post('https://api.keytrac.net/users', headers=headers)
    if not response.ok:
        result.isCreated =False
        return result 
    body=json.loads(response.text)
    id = body["id"]
    create_user_db(db,nick,id,password,samples)
    data={
        "user_id":id,
        "samples":samples
    }
    headers  = {"Authorization":"3c8a2da2-0a61-4684-99c7-ba39f976fe24","Content-Type": "application/json","Accept": "application/json"}
    # headers  = {"Authorization":"3242342423423","Content-Type": "application/json","Accept": "application/json"}
    response:Response = requests.post('https://api.keytrac.net/anytext/enrol', headers=headers, data=json.dumps(data))

    if not response.ok:
        result.isCreated =False
        return result 
    body=json.loads(response.text)
    result.isCreated=body["OK"]
    print(result)
    return result

@app.post("/user/login/", response_model=CheckUserIdentityResponse)
def check_user_identity(request:CheckUserIdentity):
    nick = request.nick
    password = request.password
    samples = request.sample
    result = CheckUserIdentityResponse()
    user:UserEntity = find_user_id_db(db,nick)
    if not user:
        result.authenticated =False
        result.score = -100
        return result
    headers  = {"Authorization":"3c8a2da2-0a61-4684-99c7-ba39f976fe24"}
    data={
        "user_id":user["keyTrackId"],
        "samples":samples
    }
    headers  = {"Authorization":"3c8a2da2-0a61-4684-99c7-ba39f976fe24","Content-Type": "application/json","Accept": "application/json"}
    response:Response = requests.post('https://api.keytrac.net/anytext/authenticate', headers=headers, data=json.dumps(data))

    if not response.ok:
        result.authenticated = False
        result.score = -200
        return result 
    body:CheckUserIdentityResponse = json.loads(response.text)
    result = body
    return result

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
