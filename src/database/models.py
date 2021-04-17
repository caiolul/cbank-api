# import base64
# import twofish
# import bcrypt
# from twofish import Twofish

from sqlalchemy import Table, Integer, MetaData, String, Column, ForeignKey, Float
# from sqlalchemy.orm import relationship
import databases
from starlette.config import Config

config = Config('.env')

DATABASE_URL = config("DATABASE_URL")

metadata = MetaData()

# relation = relationship()

User = Table(
    'User',
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, unique=True, nullable=False),
    Column("name", String, nullable=False),
    Column("cpf", String, unique=True, nullable=False),
    Column("password", String, nullable=False),
    # relationship("Balance", uselist=False, back_populates="User"),

)
Balance = Table(
    'Balance',
    metadata,
    Column("id", Integer, primary_key=True),
    Column("value", Float, nullable=False),
    Column("user_cpf", Integer, ForeignKey(
        'User.cpf'), nullable=False, unique=True),
    # relationship("User", back_populates="Balance"),

)

# password = bytes("klsjdlkajsdlkajlsdkj", "ascii")
# # Hash a password for the first time, with a randomly-generated salt
# hashed = bcrypt.hashpw(password, bcrypt.gensalt())
# # Check that an unhashed password matches one that has previously been
# # hashed
# ch = str(hashed, 'utf-8')
# print(ch)
# print(hashed)
# if bcrypt.checkpw(password, hashed):
#     print("It Matches!")
# else:
#     print("It Does not Match :(")

database = databases.Database(DATABASE_URL)
