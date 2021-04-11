from starlette.applications import Starlette
from starlette.routing import Route
from src.routes.routes import api_routes
from src.database.models import database


app = Starlette(debug=True, routes=api_routes, on_startup=[
                database.connect], on_shutdown=[database.disconnect])
