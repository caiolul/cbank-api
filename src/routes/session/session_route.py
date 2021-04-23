import bcrypt
import jwt
from starlette.responses import JSONResponse
from starlette.requests import Request
from src.database.models import User, database, config

key = config('HASH_GEN')


async def login(request: Request):
    data = await request.json()
    query = "SELECT * FROM USER WHERE EMAIL == :email"
    result = await database.fetch_one(query=query, values={"email": data["email"]})
    # print(result)
    if result != None:
        hashed = bytes(data["password"], "utf-8")
        # print(result["password"])
        check_password = bcrypt.checkpw(hashed, result["password"])
        print(check_password)
        if check_password:
            token = jwt.encode(
                {"f_name": result["fname"], "l_name": result["lname"], "email": result["email"], "cpf": result["cpf"]}, key, algorithm="HS256")

            # token_decode = jwt.decode(token, key, algorithms="HS256")
            return JSONResponse({"f_name": result["fname"], "l_name": result["lname"], "email": result["email"], "cpf": result["cpf"], "token": token}, 200)
        return JSONResponse("Email or passwor incorrect", 400)
    return JSONResponse("Not Found", 404)
