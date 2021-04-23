import bcrypt
import jwt
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from starlette.requests import Request
from src.database.models import User, database

# check_password = bcrypt.checkpw(hashed, crypt)


async def login(request: Request):
    data = await request.json()
    query = "SELECT * FROM USER WHERE EMAIL == :email"
    result = await database.fetch_one(query=query, values={"email": data["email"]})
    print(result)
    if result != None:
        return JSONResponse("ok")
    # return JSONResponse("User":user, "Token":token)
    return JSONResponse("Not Found")
