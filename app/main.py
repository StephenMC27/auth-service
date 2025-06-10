from fastapi import FastAPI

from app.routers import login, registration, users

app = FastAPI(title="User Authentication Service")

app.include_router(users.router)
app.include_router(registration.router)
app.include_router(login.router)
