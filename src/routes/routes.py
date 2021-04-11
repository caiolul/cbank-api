from starlette.templating import Jinja2Templates
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.responses import JSONResponse
from src.socket.websocket import websocket_endpoint
from src.database.models import User, database


templates = Jinja2Templates(directory='templates')


async def homepage(request):
    return templates.TemplateResponse('index.html', {'request': request})


async def list_user(request):
    query = User.select()
    results = await database.fetch_all(query)
    content = [
        {
            "Name": result["name"],
            "Email": result["email"],
            "Cpf": result["cpf"]
        }
        for result in results
    ]
    return JSONResponse(content)


async def add_user(request):
    data = await request.json()
    query = User.insert().values(
        name=data["name"],
        email=data["email"],
        cpf=data["cpf"]
    )
    await database.execute(query)
    return JSONResponse({
        "Name": data["name"],
        "Email": data["email"],
        "Cpf": data["cpf"]
    })

api_routes = [
    Route('/', homepage),
    Route("/user", endpoint=list_user, methods=["GET"]),
    Route("/user", endpoint=add_user, methods=["POST"]),
    WebSocketRoute('/ws', websocket_endpoint)
]
