#Python
from json import load, loads, dump

#Custom
from typing import Dict, List, NoReturn
from unittest import result
from models import Tweet, User, UserRegister

#Fast api
from fastapi import Body, FastAPI, Path
from fastapi import status

app = FastAPI()

# Path operations

@app.get(path='/')
def home() -> Dict[str, str]:
    return {'Twitter API': 'Active'}

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
    with open('users.json','r+', encoding='utf-8') as f:
        results: list = load(f)
        results.append(loads(user.json()))
        f.seek(0)
        dump(results, f, indent=2)
    return user

### Authentica the user
@app.post(
    path='/auth/login',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Login with user',
    tags=['Auth', 'Users']
)
def login() -> User:
    pass

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
    user_id: int = Path(gt=0, title='User ID', description='The ID of the user to retrieve', example=1)
    ) -> User:
    pass

### Update a user
@app.put(
    path='/users/{user_id}',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Update a user',
    tags=['Users']
)
def update_user(
    user_id: int = Path(gt=0, title='User ID', description='The ID of the user to update', example=1)
    ) -> User:
    pass

### Delete a user
@app.delete(
    path='/users/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete a user',
    tags=['Users']
)
def delete_user(
    user_id: int = Path(gt=0, title='User ID', description='The ID of the user to delete', example=1)
    ) -> NoReturn:
    pass

## Tweets

### Create a tweet
@app.post(
    path='/tweet',
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary='Create a new tweet',
    tags=['Tweets']
)
def create_tweet() -> Tweet:
    pass

### Show all tweets
@app.get(
    path='/tweet',
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary='List all tweets',
    tags=['Tweets']
)
def list_tweet() -> List[Tweet]:
    pass

### Show a tweet
@app.get(
    path='/tweet/{tweet_id}',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='Show a tweet',
    tags=['Tweets']
)
def get_tweet(
    tweet_id: int = Path(gt=0, title='Tweet ID', description='Retrieve a tweet', example=1)
    ) -> Tweet:
    pass

### Update a tweet
@app.put(
    path='/tweet/{tweet_id}',
    response_model=Tweet,
    status_code=status.HTTP_202_ACCEPTED,
    summary='Update a tweet',
    tags=['Tweets']
)
def update_tweet(
    tweet_id: int = Path(gt=0, title='Tweet ID', description='Retrieve a tweet', example=1)
    ) -> Tweet:
    pass

### Delete a tweet
@app.delete(
    path='/tweet/{tweet_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete a tweet',
    tags=['Tweets']
)
def delete_tweet(
    tweet_id: int = Path(gt=0, title='Tweet ID', description='Retrieve a tweet', example=1)
    ) -> NoReturn:
    pass