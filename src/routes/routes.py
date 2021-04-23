from starlette.routing import Route
from src.routes.user.user_route import add_user
from src.routes.session.session_route import login
from src.routes.transfer.trasnfer_route import tranfer_to_cpf


# async def list_user(request: Request) -> object:
#     query = User.select()
#     results = await database.fetch_all(query)
#     content = [
#         {
#             "First name": result["fname"],
#             "Last name": result["lname"],
#             "Email": result["email"],
#             "Cpf": result["cpf"],
#         }
#         for result in results
#     ]
#     return JSONResponse(content)


api_routes = [
    # Route("/user", endpoint=list_user, methods=["GET"]),
    Route("/user", endpoint=add_user, methods=["POST"]),
    Route("/user/trasnfer", endpoint=tranfer_to_cpf, methods=["GET"]),
    Route("/user/session", endpoint=login, methods=["POST"]),
]
