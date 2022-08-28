#Python
from ast import For
from doctest import Example
from typing import Optional
from enum import Enum
import fastapi
#Pydantic
from pydantic import BaseModel, Field, EmailStr
from pydantic import SecretStr
# Fast api
from fastapi import FastAPI
from fastapi import Body, Query, Path, Form, Header, Cookie
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
    

class LoginOut(BaseModel):
    username: str = Field(max_length=20, example='Querry2020')
    message: str = Field(example='Login succesfully')
    
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
    )
def update_location(
    location_id: int = Path(
        title='Location to update',
        description='Location to update',
        gt=0,
        example=45
    ),
    location: Location = Body()):
    return location

@app.post(
    path='/login',
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(
    username: str = Form(example='JuanesElMocho123'),
    password: SecretStr = Form(example='Jasda7AS"$JJSP2Ab.')):
    return LoginOut(username=username, message='OK')

# Cookies
@app.post(
    path='/contact',
    status_code=status.HTTP_200_OK
)
def contact(
    first_name: str = Form(max_length=20, min_length=1),
    last_name: str = Form(max_length=20, min_length=1),
    email: EmailStr = Form(),
    message: str = Form(min_length=20),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None),
    
):
    return user_agent