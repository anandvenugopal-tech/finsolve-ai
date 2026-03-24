from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from backend.auth import authenticate_user, create_access_token, decode_token
from backend.rag_engine import get_rag_responce

app = FastAPI(title = 'FinSolve RAG API')

security = HTTPBearer()

class LoginRequest(BaseModel):
    username: str
    password: str

class QueryRequest(BaseModel):
    query: str

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        return decode_token(credentials.credentials)
    except:
        raise HTTPException(status_code = 401, detail = 'Invalid or expired token')
    
@app.post('/login')
def login(req: LoginRequest):
    user = authenticate_user(req.username, req.password)

    if not user:
        raise HTTPException(status_code = 401, detail = 'Invalid credentials')
    token = create_access_token(user)
    return {
        'access_token': token,
        'role': user['role'],
        'username': user['username']
    }

@app.post('/query')
def query(req: QueryRequest, user = Depends(get_current_user)):
    result = get_rag_responce(req.query, user.role)
    return {
        'answer': result['answer'],
        'sources': result['sources'],
        'role': user.role,
        'query': req.query
    }

@app.get('/me')
def me(user = Depends(get_current_user)):
    return {
        'username': user.username,
        'role': user.role
    }