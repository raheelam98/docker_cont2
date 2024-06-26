from docker_con1 import settings
from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Session

# create database schema
class Todo(SQLModel, table=True):
    todo_id : Optional[int] = Field(default=None, primary_key=True)
    todo_name : str
    is_complete : bool = False

# ===============  add databse =============== #

# create login model
class LoginModel(SQLModel):
    user_email: str
    user_password: str

# create pydantic model for user
class SignupModel(LoginModel):
    user_name: str
    # user_email: str
    # user_password: str

# Define User model
class User(SignupModel, table=True):
    user_id: Optional[int] = Field(None, primary_key=True)
    
# Define Token model
class Token(SQLModel, table=True):
    token_id: Optional[int] = Field(None, primary_key=True)
    user_id : int = Field(int, foreign_key="user.user_id")  # add fk :- save refresh token with user-id
    refresh_token: str  # refresh token for authentication    

    
# ===============  connection strin =============== #    


# connecting with database 
connection_string = str(settings.DATABASE_URL).replace("postgresql", "postgresql+psycopg2")

# create engine
engine = create_engine(connection_string, connect_args={"sslmode":"require"}, pool_recycle=300, echo=True)

# create database and tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# create session to get memory space in db
def get_session():
    with Session(engine) as session:
        yield session

# ===============  test databse =============== #

# connecting with database 
test_conn_string = str(settings.TEST_DATABASE_URL).replace("postgresql", "postgresql+psycopg2")

# create engine
test_engine = create_engine(test_conn_string, connect_args={"sslmode":"require"}, pool_recycle=300, echo=True)

# create database and tables
def test_create_db_tables():
    SQLModel.metadata.create_all(engine)

