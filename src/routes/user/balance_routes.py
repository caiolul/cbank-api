import bcrypt
from enum import Enum
from starlette.requests import Request
from starlette.responses import JSONResponse
from src.database.models import User, Balance, History, database
from starlette.authentication import requires
from starlette_jwt import JWTUser
# from src.utils.database_func import update_data


class TypeTransaction(Enum):
    WITHDRAWN = 1
    DEPOSIT = 2
    TRANSFER = 3


@requires('authenticated')
async def check_balance(request: Request) -> object:
    data: JWTUser = request.user
    # print(request.user.payload)
    raw = "SELECT * FROM BALANCE WHERE USER_CPF = :cpf"
    query = await database.fetch_one(
        query=raw,
        values={"cpf": data.payload["cpf"]})
    # print(query)
    # print(await update_data(data.payload["cpf"]))
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
        # Create history
        history = History.insert().values(
            type=TypeTransaction.WITHDRAWN.value,
            value=data_json["value"],
            cpf_recive=data.payload["cpf"],
        )

        await database.execute(history)
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
        history = History.insert().values(
            type=TypeTransaction.DEPOSIT.value,
            value=data_json["value"],
            cpf_recive=data.payload["cpf"],
        )
        await database.execute(history)
        # Return new balance
        return JSONResponse({"New balance": result})
    # Return errors
    return JSONResponse({"Error": "Value incorrect"})


@requires('authenticated')
async def transfer_to_cpf(request: Request) -> object:
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

    # Query cpf to recive
    raw = "SELECT * FROM BALANCE WHERE USER_CPF = :cpf"
    query_cpf = await database.fetch_one(
        query=raw,
        values={"cpf": data_json["cpf"]})
    new_balance = query_cpf["value"] + data_json["value"]

    # Handling request
    if result >= 0.0 and query_cpf != None:
        # Query to update balance
        raw_updade = "UPDATE BALANCE SET VALUE = :value WHERE USER_CPF = :cpf"
        resutl_query = await database.execute(
            query=raw_updade,
            values={"value": new_balance, "cpf": data_json["cpf"]})
        # Create history
        history = History.insert().values(
            type=TypeTransaction.TRANSFER.value,
            value=data_json["value"],
            cpf_recive=data_json["cpf"],
            cpf_send=data.payload["cpf"]
        )

        await database.execute(history)
        # Return new value
        return JSONResponse({"New balance": new_balance})
    # Return errors
    return JSONResponse({"Error": "higher value than available"})
