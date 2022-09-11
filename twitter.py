#Python
from datetime import date, datetime
from json import load, loads, dump

#Custom
from models import Tweet, User, UserBase, UserRegister
from backends import TweetMan, UserMan

#Pydantic
from typing import Dict, List, NoReturn
from pydantic import EmailStr, Json, SecretStr

#Fast api
from fastapi import Body, FastAPI, Form, Path
from fastapi import status, HTTPException

app = FastAPI()
tm = TweetMan()
um = UserMan()

# Path operations

@app.get(
    path='/',
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="List all tof the tweets in the site",
    tags=["Tweets"])
def home() -> List[Tweet]:
    """This path operation show all of the tweets

    Returns:
        json: json containing all the tweets, features:
          - tweet_id: UUID
          - content: str
          - created_at: date
          - updated_at: Optional[date]
          - by: User
    """
    return tm.readOrUpdate()

## Users

### Create a user
@app.post(
    path='/auth/signup',
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary='Register a user',
    tags=['Auth','Users']
)
def signup(user: UserRegister = Body()) -> User:
    """This path opeation creates a new user
    
    args:
      - Resques body parameters
        - user: UserRegister

    Returns:
      - User: a json with those features 
        - user_id: UUID
        - email: str
        - first_name: str
        - last_name: str
        - birth_date: str
    """
    um.readOrUpdate(user)
    return user

### Authentica the user
@app.post(
    path='/auth/login',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Login with user',
    tags=['Auth', 'Users']
)
def login(
    email: str = Form(),
    pwd: SecretStr = Form()) -> User:
    user_db = um.login(email, pwd)
    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='This person doesn\'t exist'
        )
    return user_db
    

### Get all users
@app.get(
    path='/users',
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary='Show all users',
    tags=['Users']
)
def list_users() -> List[User]:
    """This path opeation return a json with the user information of all the registered users
    
    args:

    Returns:
      - List[User]: a json with those features 
        - user_id: UUID
        - email: str
        - first_name: str
        - last_name: str
        - birth_date: str
    """
    with open('users.json','r+', encoding='utf-8') as f:
        results: list = load(f)
    return results

### Get a user
@app.get(
    path='/users/{user_id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Get a users by id',
    tags=['Users']
)
def retrieve_user(
    user_id: str = Path(title='User ID', description='The ID of the user to retrieve', example='3fa85f64-5717-4562-b3fc-2c963f66afa6')
    ) -> User:
    user_db = um.getUserbyID(user_id)
    if user_db is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='This person doesn\'t exist'
            )
    return user_db

### Update a user
@app.put(
    path='/users/{user_id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Update a user',
    tags=['Users']
)
def update_user(
    user_id: str = Path(title='User ID', description='The ID of the user to update', example='3fa85f64-5717-4562-b3fc-2c963f66afa7'),
    email: EmailStr = Form(),
    old_password: SecretStr = Form(),
    new_password: SecretStr = Form(),
    repeat_new_password: SecretStr = Form(),
    first_name: str = Form(),
    last_name: str = Form(),
    #birth_date: date = Form()
    ) -> User:
    update_status = um.updateUser(user_id, old_password, new_password, repeat_new_password, first_name, last_name, email, birth_date='')
    if 'error' in update_status:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=update_status['error']
            )
    return update_status
    

### Delete a user
@app.delete(
    path='/users/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete a user',
    tags=['Users']
)
def delete_user(
    user_id: str = Path(title='User ID', description='The ID of the user to delete', example=1)
    ) -> NoReturn:
    res = um.delete_user(user_id)
    if 'error' in res:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=res['error']
            )

## Tweets

### Create a tweet
@app.post(
    path='/tweet',
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary='Create a new tweet',
    tags=['Tweets']
)
def create_tweet(tweet: Tweet = Body()) -> Tweet:
    """This path opeation creates a new tweet
    
    args:
      - Resques body parameters
        - tweet: Tweet

    Returns:
      - tweet: a json with those features 
          - tweet_id: UUID
          - content: str
          - created_at: date
          - updated_at: Optional[date]
          - by: User
    """
    print(tweet)
    with open('tweets.json','r+', encoding='utf-8') as f:
        results: list = load(f)
        results.append(loads(tweet.json()))
        f.seek(0)
        dump(results, f, indent=2)
    return tweet

### Show all tweets
@app.get(
    path='/tweet',
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary='List all tweets',
    tags=['Tweets']
)
def list_tweet() -> List[Tweet]:
    return tm.readOrUpdate()

### Show a tweet
@app.get(
    path='/tweet/{tweet_id}',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='Show a tweet',
    tags=['Tweets']
)
def get_tweet(
    tweet_id: str = Path(title='Tweet ID', description='Retrieve a tweet', example='3fa85f64-5717-4562-b3fc-2c963f66afa7')
    ) -> Tweet:
    tweet = tm.get_tweet_by_id(tweet_id)
    if tweet is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='tweet not found'
            )
    return tweet

### Update a tweet
@app.put(
    path='/tweet/{tweet_id}',
    response_model=Tweet,
    status_code=status.HTTP_202_ACCEPTED,
    summary='Update a tweet',
    tags=['Tweets']
)
def update_tweet(
    tweet_id: str = Path(title='Tweet ID', description='Retrieve a tweet', example='3fa85f64-5717-4562-b3fc-2c963f66afa8'),
    content: str = Form()
    ) -> Tweet:
    tweet = tm.update_tweet(tweet_id, content)
    if tweet is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='tweet not found'
            )
    return tweet

### Delete a tweet
@app.delete(
    path='/tweet/{tweet_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete a tweet',
    tags=['Tweets']
)
def delete_tweet(
    tweet_id: str = Path(title='Tweet ID', description='Retrieve a tweet', example='3fa85f64-5717-4562-b3fc-2c963f66afa8')
    ) -> NoReturn:
    res = tm.delete_tweet(tweet_id)
    if 'error' in res:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='tweet not found'
            )