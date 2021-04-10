from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.routing import Route, Mount, WebSocketRoute
from src.socket.websocket import websocket_endpoint


templates = Jinja2Templates(directory='templates')


async def homepage(request):
    return templates.TemplateResponse('index.html', {'request': request})

api_routes = [
    Route('/', homepage),
    WebSocketRoute('/ws', websocket_endpoint)
]
