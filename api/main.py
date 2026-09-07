from fastapi import FastAPI

from api.routes.auth import router as auth_router

app = FastAPI(title="Security API")
app.include_router(auth_router)
