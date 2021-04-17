import bcrypt
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.responses import JSONResponse
from src.socket.websocket import websocket_endpoint
from src.database.models import User, Balance, database


async def list_user(request) -> object:
    query = User.select()
    results = await database.fetch_all(query)
    content = [
        {
            "Name": result["name"],
            "Email": result["email"],
            "Cpf": result["cpf"],
            # "Password": str(result["password"], 'utf-8')
        }
        for result in results
    ]
    # print(results)
    # print(type(JSONResponse))
    return JSONResponse(content)


async def add_user(request) -> object:
    data = await request.json()
    hashed = bytes(data["password"], "ascii")

    crypt = bcrypt.hashpw(hashed, bcrypt.gensalt())

    # print(bcrypt.checkpw(hashed, crypt))
    # fish = encode(data["password"])
    # print(fish)
    query_user = User.insert().values(
        name=data["name"],
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
        "Name": data["name"],
        "Email": data["email"],
        "Cpf": data["cpf"],

        # "Account": data["value"]
        # "Password": data["password"]
    })

api_routes = [
    # Route('/', homepage),
    Route("/user", endpoint=list_user, methods=["GET"]),
    Route("/user", endpoint=add_user, methods=["POST"]),
    # WebSocketRoute('/ws', websocket_endpoint)
]
