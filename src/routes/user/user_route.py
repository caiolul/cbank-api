import bcrypt
import asyncio
import threading
from starlette.requests import Request
from starlette_jwt import JWTUser
from starlette.responses import JSONResponse
from starlette.authentication import requires
from src.database.models import User, Balance, database
from src.utils.database_func import query_user, update_user, update_password
from src.utils.send_mail import mail_send


def between_callback(args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(mail_send(args))
    loop.close()


async def add_user(request: Request) -> object:

    # Get data
    data = await request.json()
    # Hash password
    hashed = bytes(data["password"], "utf-8")

    # Check  user
    query = await query_user(data["cpf"], data["email"])

    # Verify
    if query == None:
        insert_user = User.insert().values(
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
        await database.execute(insert_user)
        await database.execute(add_balance)

        # thread to send mail
        _thread = threading.Thread(target=between_callback,
                                   args=[data["email"]])
        _thread.setDaemon(False)
    # starting the thread
        _thread.start()

        # Return user anyways
        return JSONResponse({
            "First name": data["fname"],
            "Last name": data["lname"],
            "Email": data["email"],
            "Cpf": data["cpf"],
        }, status_code=201)
    # If user exist
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
    # print(data)
    # Handling request
    if query:
        # Query to update user
        try:
            hasattr(data_json, 'email')
            update_query = await update_user(
                data_json["fname"],
                data_json["lname"],
                data_json["email"],
                data.payload["cpf"])
            return JSONResponse({"User update": data_json["fname"]}, status_code=201)
        except:
            resutl_query = await update_user(
                data_json["fname"],
                data_json["lname"],
                data.payload["email"],
                data.payload["cpf"])
            return JSONResponse({"User update": data_json["fname"]}, status_code=201)
    # Return errors
    return JSONResponse({"Error": "check data entry"}, status_code=400)

# Update password


@requires('authenticated')
async def alter_password(request: Request) -> object:
   # Get data
    data: JWTUser = request.user
    data_json = await request.json()

    # Query user
    query = await query_user(data.payload["cpf"], data.payload["email"])
    # print(data)
    # Handling request
    if query:
        hashed = bytes(data_json["password"], "utf-8")
        # Query to update user
        encrypt = bcrypt.hashpw(hashed, bcrypt.gensalt())
        resutl_query = await update_password(
            encrypt,
            data.payload["cpf"])
        return JSONResponse({"User update password": "ok"}, status_code=201)
    # Return errors
    return JSONResponse({"Error": "check data entry"}, status_code=400)
