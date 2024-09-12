from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.engine import create_engine
import os

# creating a FastAPI server
server = FastAPI(title='User API')

# creating a connection to the database
mysql_url = 'mysql'
mysql_user = 'root'
mysql_password = os.getenv('MYSQL_PASSWORD', 'datascientest1234')  
database_name = 'Main'

# recreating the URL connection
connection_url = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_url}/{database_name}'

# creating the connection
mysql_engine = create_engine(connection_url)


# creating a User class
class User(BaseModel):
    user_id: int = 0
    username: str = 'daniel'
    email: str = 'daniel@datascientest.com'


@server.get('/status')
async def get_status():
    """Returns 1
    """
    return 1


@server.get('/users')
async def get_users():
    with mysql_engine.connect() as connection:
        results = connection.execute('SELECT * FROM Users;')

    results = [
        User(
            user_id=i[0],
            username=i[1],
            email=i[2]
            ) for i in results.fetchall()]
    return results


@server.get('/users/{user_id:int}', response_model=User)
async def get_user(user_id):
    with mysql_engine.connect() as connection:
        results = connection.execute(
            f'SELECT * FROM Users WHERE Users.id = {user_id};')

    results = [
        User(
            user_id=i[0],
            username=i[1],
            email=i[2]
            ) for i in results.fetchall()]

    if len(results) == 0:
        raise HTTPException(
            status_code=404,
            detail='Unknown User ID')
    else:
        return results[0]
