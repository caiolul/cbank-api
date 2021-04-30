import bcrypt
from enum import Enum
from starlette_jwt import JWTUser
from starlette.requests import Request
from starlette.authentication import requires
from starlette.responses import JSONResponse
from src.database.models import User, Balance, History, database
from src.utils.database_func import query_balance, update_balance


class TypeTransaction(Enum):
    WITHDRAWN = 1
    DEPOSIT = 2
    TRANSFER = 3


@requires('authenticated')
async def check_balance(request: Request) -> object:
    data: JWTUser = request.user
    # Query balance
    query = await query_balance(data.payload['cpf'])
    return JSONResponse({"balance": query["value"]})


@requires('authenticated')
async def withdrawn(request: Request) -> object:
    # Get data
    data: JWTUser = request.user
    data_json = await request.json()

    # Query balance
    query = await query_balance(data.payload["cpf"])

    # New balance
    result = query["value"] - data_json["value"]

    # Handling request
    if result >= 0.0:
        # Query to update balance
        resutl_query = await update_balance(result, data.payload["cpf"])
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
    query = await query_balance(data.payload["cpf"])
    # New balance
    result = query["value"] + data_json["value"]
    # Handling request
    if data_json["value"] >= 0.0:
        # Query to update balance
        resutl_query = await update_balance(result, data.payload["cpf"])

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
    query = await query_balance(data.payload["cpf"])
    # New balance
    result = query["value"] - data_json["value"]

    # Query cpf to recive
    query_cpf = await query_balance(data_json["cpf"])

    new_balance = query_cpf["value"] + data_json["value"]

    # Handling request
    if result >= 0.0 and query_cpf != None:
        # Query to update balance

        resutl_query = await update_balance(new_balance, data_json["cpf"])
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
