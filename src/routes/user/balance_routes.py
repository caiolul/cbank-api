import bcrypt
from starlette.requests import Request
from starlette.responses import JSONResponse
from src.database.models import User, Balance, database
from starlette.authentication import requires
from starlette_jwt import JWTUser


@requires('authenticated')
async def check_balance(request: Request) -> object:
    data: JWTUser = request.user
    # print(request.user.payload)
    raw = "SELECT * FROM BALANCE WHERE USER_CPF = :cpf"
    query = await database.fetch_one(
        query=raw,
        values={"cpf": data.payload["cpf"]})
    # print(query)

    return JSONResponse({"balance": query["value"]})


@requires('authenticated')
async def withdrawn(request: Request) -> object:
    # Get data
    data: JWTUser = request.user
    data_json = await request.json()

    # Query balance
    raw = "SELECT * FROM BALANCE WHERE USER_CPF = :cpf"
    query = await database.fetch_one(
        query=raw,
        values={"cpf": data.payload["cpf"]})
    # New balance
    result = query["value"] - data_json["value"]

    # Handling request
    if result >= 0.0:
        # Query to update balance
        raw_updade = "UPDATE BALANCE SET VALUE = :value WHERE USER_CPF = :cpf"
        resutl_query = await database.execute(
            query=raw_updade,
            values={"value": result, "cpf": data.payload["cpf"]})
        # Return new value
        return JSONResponse({"New balance": result})
    # Return errors
    return JSONResponse({"Error": "higher value than available"})


@requires('authenticated')
async def deposit(request: Request) -> object:
    # Get data
    data: JWTUser = request.user
    data_json = await request.json()

    # Query balance
    raw = "SELECT * FROM BALANCE WHERE user_cpf = :cpf"
    query = await database.fetch_one(
        query=raw,
        values={"cpf": data.payload["cpf"]})
    result = query["value"] + data_json["value"]
    if result >= 0.0:
        # Query to update balance
        raw_updade = "UPDATE BALANCE SET value = :value WHERE USER_CPF = :cpf"
        resutl_query = await database.execute(
            query=raw_updade,
            values={"value": result, "cpf": data.payload["cpf"]})
        # Return new balance
        return JSONResponse({"New balance": result})
    # Return errors
    return JSONResponse({"Error": "Value incorrect"})
