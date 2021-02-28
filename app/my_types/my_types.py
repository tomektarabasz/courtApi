from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

class File(BaseModel):
    name:str
    date:str
    path:str
    id:int
    pass

class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

# class CourtEntity(BaseModel):
#     id: Optional[PyObjectId] = Field(alias='_id')
#     name:str
#     level: str
#     coverCitys:Optional[List[str]]
#     coverRegions:Optional[List[str]]
#     coverCityParts:Optional[List[str]]

#     class Config:
#         arbitrary_types_allowed = True
#         json_encoders = {
#             ObjectId: str
#         }

class CourtEntity(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    name:str
    coverArea:Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class CityEntity(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    name:str
    key: str
    gmina:Optional[str]
    powiat:Optional[str]
    wojewodztwo:Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
