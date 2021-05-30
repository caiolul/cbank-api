from starlette.applications import Starlette
from starlette.routing import Route
from src.routes.routes import api_routes
from src.database.models import database
from src.middleware.token_auth import middleware_token


app = Starlette(debug=False,
                routes=api_routes,
                on_startup=[database.connect],
                on_shutdown=[database.disconnect],
                middleware=middleware_token())
