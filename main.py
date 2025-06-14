from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.users_router import users_router

app = FastAPI()

# Agregás el middleware directamente
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Desarrollo
        "https://login-form-front-git-main-belgique5432s-projects.vercel.app"  # Producción
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrás el router
app.include_router(users_router)
