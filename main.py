#Python
from doctest import Example
from typing import Optional
from enum import Enum
#Pydantic
from pydantic import BaseModel, Field, EmailStr
# Fast api
from fastapi import FastAPI, Body, Query, Path

app = FastAPI()

# Enums
class HairColors(Enum):
     white: str = 'White'
     brown: str = 'Brown'
     black: str = 'Black'
     yellow: str = 'Yellow'
     red: str = 'Red'

# Models 
class Person(BaseModel):
    first_name: str = Field(
        min_length=3,
        max_length=30
    )
    last_name: str = Field(
        min_length=3,
        max_length=30
    )
    age: int = Field(
        ...,
        gt=0,
        le=115
    )
    hair_color: Optional[HairColors] = Field(None)
    is_married: Optional[bool] = Field(None)
    email: EmailStr = Field(title='Email')
    
    class Config:
        schema_extra = {
            'example': {
                'first_name': 'Juan',
                'last_name': 'Snow',
                'age': 29,
                'hair_color': HairColors.brown,
                'is_married': False,
                'email': 'juanes@cigre.com'
            }
        }
    
class Location(BaseModel):
    city: str = Field(min_length=5, max_length=20, example="Medellin")
    state: str = Field(min_length=5, max_length=20, example="Antioquia")
    country: str = Field(min_length=5, max_length=20, example="Colombia")

@app.get('/')
def home():
    return {'Hello': 'World'}

# Resquest and response body

@app.post('/person/new')
def crate_person(person: Person = Body()):
    #print(person)
    return person

# Validation query parameters
@app.get('/person/detail')
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=3, 
        max_length=30,
        title='Person name',
        description='This is the person name, len [3, 30]'),
    age: str = Query(
        title='Person age',
        description='This is the person age, mandatory'
    )):
    return {'name': name, 'age': age}

# Validations path parameters
@app.get('/person/detailt/{person_id}')
def show_person(
    person_id: int = Path(
        gt=0,
        title='Person age',
        description='The age of the person you want to see detaitls')):
    return {person_id: 'Exists'}

# Validations: reques body

@app.put('/person/{person_id}')
def update_person(
    person_id: int = Path(
        title='Person to update',
        description='This is person id',
        gt=0
    ),
    person: Person = Body(),
    location: Location = Body()):
    
    return {'person': person, 'location': location}

@app.put('/personData/{person_id}')
def update_person(
    person_id: int = Path(
        title='Person to update',
        description='This is person id',
        gt=0
    ),
    person: Person = Body()):
    
    return person

@app.put('/location/{location_id}')
def update_location(
    location_id: int = Path(
        title='Location to update',
        description='Location to update',
        gt=0
    ),
    location: Location = Body()):
    return location