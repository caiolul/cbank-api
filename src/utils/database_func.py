# Import types
from enum import Enum
from sqlalchemy.engine.result import RowProxy
from src.database.models import database


class QueryTypes(Enum):
    SELECT_BALANCE = "SELECT * FROM BALANCE WHERE USER_CPF = :cpf"
    UPDATE_BALANCE = "UPDATE BALANCE SET VALUE = :value WHERE USER_CPF = :cpf"


# Query balance user


async def query_balance(cpf: str) -> RowProxy:
    query = await database.fetch_one(
        query=QueryTypes.SELECT_BALANCE.value,
        values={"cpf": cpf})

    return query

# Update balance


async def update_balance(value: str, data: str) -> RowProxy:
    query = await database.execute(
        query=QueryTypes.UPDATE_BALANCE.value,
        values={
            "value": value,
            "cpf": value})
    return query
