from fastapi import FastAPI
from .routers import sugarlevel, user, auth
from .config import settings
app = FastAPI()

app.include_router(sugarlevel.router)
app.include_router(user.router)
app.include_router(auth.router)
@app.get('/')
async def root():
    return {"message":"welcome"}
