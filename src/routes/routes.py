from starlette.routing import Route
from src.routes.user.user_route import add_user
from src.routes.user.balance_routes import check_balance, deposit, withdrawn
from src.routes.session.session_route import login
from src.routes.transfer.trasnfer_route import tranfer_to_cpf


api_routes = [
    # User create routes
    Route("/user", endpoint=add_user, methods=["POST"]),
    Route("/user/session", endpoint=login, methods=["POST"]),
    # Balance routes
    Route("/user/verify/balance", endpoint=check_balance, methods=["GET"]),
    Route("/user/deposit", endpoint=deposit, methods=["PUT"]),
    Route("/user/withdrawn", endpoint=withdrawn, methods=["POST"]),
    # Tranfers routes
    Route("/user/trasnfer", endpoint=tranfer_to_cpf, methods=["GET"]),
]
