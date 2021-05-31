# Import types
from enum import Enum
from sqlalchemy.engine.result import RowProxy
from src.database.models import database

# For postgres


class QueryTypes(Enum):
    SELECT_BALANCE = """SELECT * FROM public."Balance" WHERE user_cpf = :cpf"""
    SELECT_USER = """SELECT * FROM public."User" WHERE cpf = :cpf AND email = :email"""
    SELECT_HISTORY = """SELECT * FROM public."History" WHERE cpf_recive = :cpf OR cpf_send = :cpf"""
    RETURN_USERNAME = """SELECT * FROM public."User" WHERE cpf = :cpf"""
    UPDATE_BALANCE = """UPDATE public."Balance" SET VALUE = :value WHERE user_cpf = :cpf"""
    UPDATE_USER = """UPDATE public."User" SET fname = :fname, lname = :lname, email = :email WHERE cpf = :cpf"""
    UPDATE_PASSWORD = """UPDATE public."User" SET password = :password WHERE cpf = :cpf"""
    QUERY_LOGIN = """SELECT * FROM public."User" WHERE email = :email"""

# Query username


async def query_username(cpf: str) -> RowProxy:
    query = await database.fetch_one(
        query=QueryTypes.RETURN_USERNAME.value,
        values={"cpf": cpf})
    # Exist or not
    if query:
        return query["fname"] + ' ' + query["lname"]
    return query

# Query balance user


async def query_balance(cpf: str) -> RowProxy:
    query = await database.fetch_one(
        query=QueryTypes.SELECT_BALANCE.value,
        values={"cpf": cpf})

    return query


async def query_history(cpf: str) -> RowProxy:
    query = await database.fetch_all(
        query=QueryTypes.SELECT_HISTORY.value,
        values={"cpf": cpf})

    return query

# Query user


async def query_user(cpf: str, email: str) -> RowProxy:
    query = await database.fetch_one(
        query=QueryTypes.SELECT_USER.value,
        values={
            "cpf": cpf,
            "email": email})

    return query

# Update balance


async def update_balance(value: str, data: str) -> RowProxy:
    query = await database.execute(
        query=QueryTypes.UPDATE_BALANCE.value,
        values={
            "value": value,
            "cpf": data})
    return query

# Update user


async def update_user(fname: str, lname: str, email: str, cpf: str) -> RowProxy:
    query = await database.execute(
        query=QueryTypes.UPDATE_USER.value,
        values={
            "fname": fname,
            "lname": lname,
            "email": email,
            "cpf": cpf})
    return query

# Update password user


async def update_password(password: bytes, cpf: str) -> RowProxy:
    query = await database.execute(
        query=QueryTypes.UPDATE_PASSWORD.value,
        values={
            "password": password,
            "cpf": cpf})
    return query

# Query user to login


async def login_user(email: str) -> RowProxy:
    query = await database.fetch_one(
        query=QueryTypes.QUERY_LOGIN.value,
        values={"email": email})
    return query
