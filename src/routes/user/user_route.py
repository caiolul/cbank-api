import bcrypt
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from src.database.models import User, Balance, database
from starlette.authentication import requires
from starlette_jwt import JWTUser


async def add_user(request: Request) -> object:

    # Get data
    data = await request.json()
    # Hash password
    hashed = bytes(data["password"], "utf-8")

    # Check  user
    raw = "SELECT * FROM USER WHERE CPF = :cpf AND EMAIL = :email"
    query = await database.fetch_one(
        query=raw,
        values={"cpf": data["cpf"], "email": data["email"]
                })

    # Verify
    if query == None:
        query_user = User.insert().values(
            fname=data["fname"],
            lname=data["lname"],
            email=data["email"],
            cpf=data["cpf"],
            password=bcrypt.hashpw(hashed, bcrypt.gensalt())
        )
        add_balance = Balance.insert().values(
            value=0,
            user_cpf=data["cpf"]
        )
        await database.execute(query_user)
        await database.execute(add_balance)
        return JSONResponse({
            "First name": data["fname"],
            "Last name": data["lname"],
            "Email": data["email"],
            "Cpf": data["cpf"],
        }, status_code=201)
    return JSONResponse(
        "User already exist", status_code=400
    )
