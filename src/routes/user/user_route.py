import bcrypt
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.authentication import requires
from src.database.models import User, Balance, database
from src.utils.database_func import query_user, update_user


async def add_user(request: Request) -> object:

    # Get data
    data = await request.json()
    # Hash password
    hashed = bytes(data["password"], "utf-8")

    # Check  user
    query = await query_user(data["cpf"], data["email"])

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

    # Alter user


@requires('authenticated')
async def alter_user(request: Request) -> object:
    # Get data
    data: JWTUser = request.user
    data_json = await request.json()

    # Query user
    query = await query_user(data.payload["cpf"], data.payload["email"])

    # Handling request
    if query:
        # Query to update user
        resutl_query = await update_user(data_json["fname"], data_json["lname"], data.payload["cpf"])

        return JSONResponse({"User update": data_json["fname"]})
    # Return errors
    return JSONResponse({"Error": "check data entry"})
