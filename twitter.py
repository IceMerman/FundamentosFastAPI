#Python

#Custom
import models

#Fast api
from fastapi import FastAPI

app = FastAPI()

@app.get(path='/')
def home():
    return {'Twitter API': 'Active'}