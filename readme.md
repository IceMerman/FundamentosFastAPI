# 📗 Platzi project: Twitter API

📡 This project tries to implement an API based on fast API from [Platzi FastAPI modularization course](https://platzi.com/cursos/fastapi-modularizacion-datos/)

## 📋 Project strucutre

 - 🔧 Code files
   - [twitter.py](twitter.py): Containts the main API
     - For detailts please refer to Swagger docs or ReDoc
   - [models.py](models.py): Containts the models used in this project
     - UserBase(BaseModel)
     - UserLogin(UserBase)
     - User(UserBase)
     - UserRegister(User, UserLogin)
     - Tweet(BaseModel)
   - [backend.py](backends.py): Containts the backend funtions
     - JsonMan: Class to interact with json files
     - UserMan(JsonMan): Class to interact with the user file
     - TweetMan(JsonMan): Class to interact wiht the tweet file
 - 🏬 local store files
   - [users.json](users.json): Containts the user data
   - [tweets.json](tweets.json): Cotaints the tweet data

## ℹ️ Instalation

```bash
git clone
pip install -r requierements.txt
uvicorn twitter:app --reload
```