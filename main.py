#Python
from typing import Optional
#Pydantic
from pydantic import BaseModel
# Fast api
from fastapi import FastAPI, Body, Query, Path

app = FastAPI()

# Models 
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

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