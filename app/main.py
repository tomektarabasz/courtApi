from .mongo_queries.mongo_queries import all_cities
from .my_types.my_types import CityEntity, File, MongoFile
from .helpers import connect_to_mongo_db
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

client, db = connect_to_mongo_db()
app = FastAPI()

@app.get("/")
def index():
    return({"id":"This is incrediable"})

@app.get("/all", response_model=List[CityEntity])
def prezent_all():
    return all_cities(db)

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
