from fastapi import FastAPI
from routes.router import router


app = FastAPI(title='Gestão de Código', version='0.0.1')
app.include_router(router)
