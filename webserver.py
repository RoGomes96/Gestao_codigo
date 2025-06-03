from fastapi import FastAPI
from pfsw_gestao.routes.router import router


app = FastAPI(title='Gestão de Código', version='0.0.1')
app.include_router(router)
