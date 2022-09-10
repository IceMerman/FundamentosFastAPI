#Python
from datetime import date, datetime, timedelta
from typing import Optional
from uuid import UUID, uuid4
from dateutil import tz

#Pydantic
from pydantic import BaseModel, EmailStr, Field, SecretStr, validator


# User models
class UserBase(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    email: EmailStr = Field(..., example='jhon.snow@winterfall.com')    
class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=32,
        regex='^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#_-])[A-Za-z\d@$!%*?&#_-]{8,32}$',
        description='Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number and one special character.')
class User(UserBase):
    first_name: str = Field(..., min_length=3, max_length=50, example='Jhon')
    last_name: str = Field(..., min_length=3, max_length=50, example='Snow')
    birth_date: Optional[date] = Field(None, example=date.today() - timedelta(weeks=19*52))
    
    @validator('birth_date')
    def is_adult(cls, v: date):
        today = date.today()
        delta = today - v
        if delta.days/364 < 18:
            raise ValueError('Must be over 18!')
        return v
    
class UserRegister(User, UserLogin):
    ...
    
# Tweet models
class Tweet(BaseModel):
    tweet_id: UUID = Field()
    content: str = Field(..., min_length=1, max_length=300, example='Example tweet')
    created_at: date = Field(default=datetime.utcnow()) #.replace(tzinfo=tz.tzutc())
    updated_at: Optional[date] = Field(default=datetime.utcnow()) #.replace(tzinfo=tz.tzutc())
    by: User = Field(...)