from sqlalchemy import Table, Integer, MetaData, String, Column, ForeignKey, Float
import databases
from starlette.config import Config

# create config database
config = Config('.env')

DATABASE_URL = config("DATABASE_URL")

# Create models

metadata = MetaData()

User = Table(
    'User',
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, unique=True, nullable=False),
    Column("fname", String, nullable=False),
    Column("lname", String, nullable=False),
    Column("cpf", String, unique=True, nullable=False),
    Column("password", String, nullable=False),
)
Balance = Table(
    'Balance',
    metadata,
    Column("id", Integer, primary_key=True),
    Column("value", Float, nullable=False),
    Column("user_cpf", Integer, ForeignKey(
        'User.cpf'), nullable=False, unique=True),
)

database = databases.Database(DATABASE_URL)
