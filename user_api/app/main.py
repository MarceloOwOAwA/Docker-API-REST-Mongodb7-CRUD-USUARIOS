from fastapi import FastAPI
from app.routes import auth  # Ruta de registro
from app.routes import login  # Ruta de login con MongoDB
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY no está definido en el archivo .env")

app = FastAPI()

# Incluir router de autenticación (registro)
app.include_router(auth.router, prefix="/auth", tags=["Autenticación"])

# Incluir router de login
app.include_router(login.router, prefix="/login", tags=["Login"])

@app.get("/")
async def root():
    return {"mensaje": "API funcionando correctamente"}
