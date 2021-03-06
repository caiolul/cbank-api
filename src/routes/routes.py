from starlette.routing import Route
from src.routes.user.user_route import add_user, alter_user, alter_password
from src.routes.user.balance_routes import check_balance, deposit, withdraw, transfer_to_cpf, check_history
from src.routes.session.session_route import login


api_routes = [
    # User create routes
    Route("/user", endpoint=add_user, methods=["POST"]),
    Route("/user", endpoint=alter_user, methods=["PUT"]),
    Route("/user/password", endpoint=alter_password, methods=["PUT"]),
    Route("/user/session", endpoint=login, methods=["POST"]),
    # History
    Route("/user/verify/history", endpoint=check_history, methods=["GET"]),
    # Balance routes
    Route("/user/verify/balance", endpoint=check_balance, methods=["GET"]),
    Route("/user/deposit", endpoint=deposit, methods=["PUT"]),
    Route("/user/withdraw", endpoint=withdraw, methods=["POST"]),
    # Transfers routes
    Route("/user/transfer", endpoint=transfer_to_cpf, methods=["POST"]),
]
