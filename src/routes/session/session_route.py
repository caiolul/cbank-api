import bcrypt
import jwt
import datetime
from starlette.responses import JSONResponse
from starlette.requests import Request
from src.database.models import config
from src.utils.database_func import login_user

key = config('HASH_GEN')

# print(exp_token)


async def login(request: Request):
    exp_token = datetime.datetime.now()
  # Get data
    data = await request.json()
    result = await login_user(data["email"])

    # Handle request
    if result != None:
        hashed = bytes(data["password"], "utf-8")
        # Compare password
        check_password = bcrypt.checkpw(hashed, result["password"])
        # Generate token
        if check_password:
            token = jwt.encode(
                {"f_name": result["fname"], "l_name": result["lname"],
                    "email": result["email"], "cpf": result["cpf"], "exp": exp_token},
                key,
                algorithm="HS256")
            # Return token
            print(exp_token)
            return JSONResponse({
                "f_name": result["fname"],
                "l_name": result["lname"],
                "email": result["email"],
                "cpf": result["cpf"],
                "token": token}, 200)
        return JSONResponse("Email or password incorrect", 400)
    return JSONResponse("Not Found", 404)
