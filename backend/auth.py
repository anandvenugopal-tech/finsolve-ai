from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import os
from dotenv import load_dotenv
load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret')
ALGORITHM = 'HS256'
TOKEN_EXPIRE_MINUTES = 60

#create object of password hashing
pwd_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')

#user database
USER_DB = {
    'anand': {
        'password': pwd_context.hash('anand123'), 
        'role': 'c_level'
        },
    'arjun': {
        'password': pwd_context.hash('arjun123'), 
        'role': 'finance'
        },
    'nila': {
        'password': pwd_context.hash('nila123'),
        'role': 'marketing'
        },
    'aswathi': {
        'password': pwd_context.hash('aswathi123'),
        'role': 'hr'
        },
    'devan': {
        'password': pwd_context.hash('devan123'),
        'role': 'engineering'
        },
    'vijay': {
        'password': pwd_context.hash('vijay123'),
        'role': 'employee'
    }
}

class TokenData(BaseModel):
    username: str
    role: str

def authenticate_user(username: str, password: str):
    user = USER_DB.get(username)
    if not user or not pwd_context.verify(password, user['password']):
        return None
    return {
        'username': username,
        'role': user['role']
        }

def create_access_token(data: dict):
    payload = data.copy()
    payload['exp'] = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)

def decode_token(token: str) -> TokenData:
    payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
    return TokenData(username = payload['username'], role = payload['role']) 


