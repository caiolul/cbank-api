from enum import Enum
from starlette_jwt import JWTUser
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.authentication import requires
from src.database.models import History, database
from src.utils.database_func import query_balance, update_balance, query_history, query_username


class TypeTransaction(Enum):
    WITHDRAW = 1
    DEPOSIT = 2
    TRANSFER = 3

# Query to history


@requires('authenticated')
async def check_history(request: Request) -> object:
    data: JWTUser = request.user
    # Query balance
    query = await query_history(data.payload['cpf'])

    if query:
        content = [
            {
                "id": result["id"],
                "type": result["type"],
                "value": result["value"],
                "cpf_send": result["cpf_send"],
                "send_user": str(await query_username(result["cpf_send"])),
                "time": str(result["create_at"]),
            }
            for result in query
        ]

        return JSONResponse(content=content)

    return JSONResponse({"History not found": "check data entry"}, status_code=400)

# Query to balance


@ requires('authenticated')
async def check_balance(request: Request) -> object:
    data: JWTUser = request.user
    # Query balance
    query = await query_balance(data.payload['cpf'])
    if query:
        return JSONResponse({"balance": query["value"]})

    return JSONResponse({"Balance not found": "check data entry"}, status_code=400)


@ requires('authenticated')
async def withdraw(request: Request) -> object:
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
            type=TypeTransaction.WITHDRAW.value,
            value=data_json["value"],
            cpf_recive=data.payload["cpf"],
        )

        await database.execute(history)
        # Return new value
        return JSONResponse({"New balance": result})
    # Return errors
    return JSONResponse({"Error": "higher value than available"}, status_code=400)


@ requires('authenticated')
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
    return JSONResponse({"Error": "Value incorrect"}, status_code=400)


@ requires('authenticated')
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
    remove_balance = query["value"] - data_json["value"]

    # Handling request
    if result >= 0.0 and query_cpf != None and remove_balance >= 0.0:
        # Query to update balance
        update_send_balance = await update_balance(remove_balance, data.payload["cpf"])
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
        return JSONResponse({"New balance recive": new_balance,
                             "New balance send": remove_balance})
    # Return errors
    return JSONResponse({"Error": "higher value than available"}, status_code=400)
