from typing import List, Union
from json import load, loads, dump

from pydantic import SecretStr

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
            print(user)
            if user['email'] == email and user['password'] == pwd.get_secret_value():
                return user
    
    def update(self):
        pass
    
class TweetMan(JsonMan):
    def __init__(self) -> None:
        super().__init__('tweets.json')