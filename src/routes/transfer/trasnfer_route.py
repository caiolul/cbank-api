from starlette.responses import JSONResponse
from starlette.authentication import requires
# from starlette.middleware.sessions import Session


# @requires('authenticated')
async def tranfer_to_cpf(request) -> object:
    return JSONResponse({'payload': request.session})


async def withdraw(request) -> object:
    pass


async def pay_account(request) -> object:
    pass


async def deposit(request) -> object:
    pass
