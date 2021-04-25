from starlette.routing import Route
from src.routes.user.user_route import add_user, check_balance
from src.routes.session.session_route import login
from src.routes.transfer.trasnfer_route import tranfer_to_cpf


api_routes = [
    Route("/user", endpoint=add_user, methods=["POST"]),
    Route("/user/verify/balance", endpoint=check_balance, methods=["GET"]),
    Route("/user/trasnfer", endpoint=tranfer_to_cpf, methods=["GET"]),
    Route("/user/session", endpoint=login, methods=["POST"]),
]
