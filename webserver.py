from fastapi import FastAPI

from pfsw_gestao.routes import auth, todos, users

app = FastAPI(title="Gestão de Código", version="0.0.1")

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)
