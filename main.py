#Python
from doctest import Example
from typing import Optional
from enum import Enum
#Pydantic
from pydantic import BaseModel, Field, EmailStr
# Fast api
from fastapi import FastAPI, Body, Query, Path
from fastapi import status

app = FastAPI()

# Enums
class HairColors(Enum):
     white: str = 'White'
     brown: str = 'Brown'
     black: str = 'Black'
     yellow: str = 'Yellow'
     red: str = 'Red'

# Models 

class PersonBase(BaseModel):
    first_name: str = Field(
        min_length=3,
        max_length=30,
        example='Miguel'
    )
    last_name: str = Field(
        min_length=3,
        max_length=30,
        example='Arena'
    )
    age: int = Field(
        gt=0,
        le=115,
        example=35
    )
    hair_color: Optional[HairColors] = Field(None, example=HairColors.brown)
    is_married: Optional[bool] = Field(None, example=False)
    email: EmailStr = Field(title='Email', example='juanes@cigre.com')
        
class Person(PersonBase):
    password: str = Field(min_length=8, example='IA123Jk"%P2')
    
class PersonOut(PersonBase):
    ...
    
    
class Location(BaseModel):
    city: str = Field(min_length=5, max_length=20, example="Medellin")
    state: str = Field(min_length=5, max_length=20, example="Antioquia")
    country: str = Field(min_length=5, max_length=20, example="Colombia")

@app.get(
    path='/', 
    status_code=status.HTTP_200_OK)
def home():
    return {'Hello': 'World'}

# Resquest and response body

@app.post(
    path='/person', 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED)
def crate_person(person: Person = Body()):
    return person

# Validation query parameters
@app.get(
    path='/person/detail',
    status_code=status.HTTP_200_OK)
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=3, 
        max_length=30,
        title='Person name',
        description='This is the person name, len [3, 30]',
        example='Juan'),
    age: str = Query(
        title='Person age',
        description='This is the person age, mandatory',
        example=32
    )):
    return {'name': name, 'age': age}

# Validations path parameters
@app.get(
    path='/person/detail/{person_id}',
    status_code=status.HTTP_200_OK)
def show_person(
    person_id: int = Path(
        gt=0,
        title='Person age',
        description='The age of the person you want to see detaitls',
        example=98)):
    return {person_id: 'Exists'}

# Validations: reques body

@app.put(
    path='/person/{person_id}',
    status_code=status.HTTP_200_OK)
def update_person(
    person_id: int = Path(
        title='Person to update',
        description='This is person id',
        gt=0,
        example=122
    ),
    person: Person = Body(),
    location: Location = Body()):
    
    return {'person': person, 'location': location}

@app.put(
    path='/personData/{person_id}',
    status_code=status.HTTP_200_OK)
def update_person(
    person_id: int = Path(
        title='Person to update',
        description='This is person id',
        gt=0,
        example=33
    ),
    person: Person = Body()):
    
    return person

@app.put(
    path='/location/{location_id}',
    status_code=status.HTTP_200_OK)
def update_location(
    location_id: int = Path(
        title='Location to update',
        description='Location to update',
        gt=0,
        example=45
    ),
    location: Location = Body()):
    return location