import sqlalchemy
import databases
from starlette.config import Config

config = Config('.env')

DATABASE_URL = 'sqlite:///test.sqlalchemy'

metadata = sqlalchemy.MetaData()

User = sqlalchemy.Table(
    'User',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True, nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("cpf", sqlalchemy.String, unique=True, nullable=False),
)


# class State(sqlalchemy):
#     cnpj = sqlalchemy.Column(sqlalchemy.String(120), unique=True,
#                              nullable=False, primary_key=True)
#     username = sqlalchemy.Column(sqlalchemy.String(80), nullable=False)
#     email = sqlalchemy.Column(sqlalchemy.String(120),  nullable=False)


database = databases.Database(DATABASE_URL)
