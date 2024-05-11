from fastapi import FastAPI, Depends, HTTPException, Body
from docker_con1.controllers.generate_pass3 import passwordInto_hash3, passswordIntoHash3
from docker_con1.model import create_db_and_tables, get_session, engine, Todo
from sqlmodel import Session, select
from typing import Annotated
from typing import AsyncGenerator
from contextlib import asynccontextmanager

@asynccontextmanager
async def life_span(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()
    yield

app = FastAPI(lifespan=life_span, title="Todo App")

@app.get('/')
def get_root():
    return {"Docker ": "Compose Image"}

# Define a route to generate a password hash
@app.get("/api/get_password3")
def generate_pass3():
    passwordInto_hash3()  # admin hash-password on terminal
    return passswordIntoHash3("user_password123")  # user hash-password on swagger (response body)

@app.get("/api/get_todo") 
def get_todo_route(session: Annotated[Session,Depends(get_session)]):
    get_todos =  select(Todo)
    todo_list = session.exec(get_todos).all()
    if not todo_list:
        raise HTTPException(status_code=404 , detail=f"Todo Not Found In Database")
    else:
        return todo_list

@app.post('/api/add_todo/', response_model=Todo) 
def add_todo_route(todo :Annotated[str, Body()], session: Annotated[Session,Depends(get_session) ]):
    todos = Todo(todo_name=todo)
    if not todos:
        raise HTTPException(status_code=404, detail=f"Can't Add Todo Name In Database")
    else:
        session.add(todos)
        session.commit()
        session.refresh(todos)
        return todos 
    
@app.put('/api/update_todo') 
def update_todo_route(id: int, todo : Annotated[str, Body()], session: Annotated[Session, Depends(get_session)]):
    select_todo =  select(Todo).where(Todo.todo_id == id)
    update_todo = session.exec(select_todo).first()
    if not update_todo:
        raise HTTPException(status_code=404, detail=f"Todo {id} Not Found in Database")
    else:
        update_todo.todo_name = todo
        session.commit()
        session.refresh(update_todo)
        return update_todo
    
@app.delete('/api/delete_todo/{id}')  
def delete_todo_route(id:int, session: Annotated[Session, Depends(get_session)]):
    select_todo = session.get(Todo, id)
    if not select_todo:
        raise HTTPException(status_code=404, detail=f"Todo {id} Not Found in Database")
    else:
        session.delete(select_todo)
        session.commit()
        return select_todo







   
