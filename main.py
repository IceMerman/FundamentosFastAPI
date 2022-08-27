#Python
from typing import Optional
#Pydantic
from pydantic import BaseModel
# Fast api
from fastapi import FastAPI, Body

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