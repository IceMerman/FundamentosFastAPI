from datetime import datetime
import secrets
from typing import List, Union
from json import load, loads, dump

from pydantic import EmailStr, SecretStr

from models import Tweet, User, UserBase, UserRegister

class JsonMan():
    
    def __init__(self, filename: str) -> None:
        self.__filename = filename

    def readOrUpdate(
        self,
        obj: Union[Tweet, User, UserBase, UserRegister, None] = None
        ) -> list:
        """This function manages the json files used as db for this project
        is obj argument is None, then the function only read, else append the obj

        Args:
        - filename (str): Name of the file to read/write
        - mode (str, optional): _description_. Defaults to 'r+'.
        - obj (Union[Tweet, User, UserBase, UserRegister, None], optional): _description_. Defaults to None.

        Returns:
        - list: a list of dictionaries (json processed)
        """
        with open(self.__filename, 'r+', encoding='utf-8') as f:
            results: list = load(f)
            if not obj is None:
                results.append(loads(obj.json()))
                f.seek(0)
                dump(results, f, indent=2)
        return results

    def write(self, data: Union[list, dict], force=False) -> None:
        """This function write data to the json file

        Args:
            data (Union[list, dict]): Data
        """
        mode = 'a' if not force else 'w'
        with open(self.__filename, mode, encoding='utf-8') as f:
            dump(data, f, indent=2)

class UserMan(JsonMan):
    def __init__(self) -> None:
        super().__init__('users.json')

    def login(self, email: str, pwd: SecretStr) -> dict:
        dbUsers = self.readOrUpdate()
        for user in dbUsers:
            if user['email'] == email and user['password'] == pwd.get_secret_value():
                return user
    
    def getUserbyID(self, user_id: str):
        user_db = self.readOrUpdate()
        for user in user_db:
            if user['user_id'] == user_id:
                return user
            
    def updateUser(self, user_id: str, old_pwd: secrets, new_pwd: secrets, rep_new_pwd: secrets, 
        first_name: str, last_name: str, email: EmailStr,
        birth_date: datetime):
        
        user_db = self.readOrUpdate()
        
        found = False
        for user_u in user_db:
            if user_u['user_id'] == user_id:
                found = True
                
                if new_pwd.get_secret_value() != rep_new_pwd.get_secret_value():
                    return {'error': 'New password doesnt match'}
                if old_pwd.get_secret_value() != user_u['password']:
                    return {'error': 'Old password doesnt match'}
                
                if new_pwd != '':
                    user_u['password'] = new_pwd.get_secret_value()
                if first_name != '':
                    user_u['first_name'] = first_name
                if last_name != '':
                    user_u['last_name'] = last_name
                if birth_date != '':
                    user_u['birth_date'] = birth_date
                if email != '':
                    user_u['email'] = email

                self.write(user_db, force=True)
                return user_u
        if not found:
            return {'error': 'User not found'}
        
    def delete_user(self, user_id: str):
        user_db = self.readOrUpdate()
        print(user_db)
        found = False
        for idx, user_u in enumerate(user_db):
            if user_u['user_id'] == user_id:
                found = True
        if not found:
            return {'error': 'User not found'}
        del user_db[idx]
        
        self.write(user_db, force=True)
        return {'status': 'Done'}
        
    
class TweetMan(JsonMan):
    def __init__(self) -> None:
        super().__init__('tweets.json')
        
    def get_tweet_by_id(self, tweet_id: str):
        tweet_db = self.readOrUpdate()
        print(tweet_id)
        for tweet in tweet_db:
            if tweet['tweet_id'] == tweet_id:
                return tweet
            
    def update_tweet(self, tweet_id: str, content: str):
        tweet_db = self.readOrUpdate()
        print(tweet_id)
        for tweet in tweet_db:
            if tweet['tweet_id'] == tweet_id:
                if content != '':
                    tweet['content'] = content
                    tweet['updated_at'] = str(datetime.utcnow())
                    self.write(tweet_db, force=True)
                return tweet
    
    def delete_tweet(self, tweet_id: str):
        tweet_db = self.readOrUpdate()
        found = False
        for idx, tweet in enumerate(tweet_db):
            if tweet['tweet_id'] == tweet_id:
                found = True
                break
        
        if found:
            del tweet_db[idx]
            self.write(tweet_db, force=True)
            return {'status': 'done'}
        return {'error': 'not found'}