from fastapi import FastAPI
from app.routes import auth  # Ruta de registro
from app.routes import login  # Ruta de login con MongoDB

app = FastAPI()

# Incluir router de autenticación (registro)
app.include_router(auth.router, prefix="/auth", tags=["Autenticación"])

# Incluir router de login
app.include_router(login.router, prefix="/login", tags=["Login"])

@app.get("/")
async def root():
    return {"mensaje": "API funcionando correctamente"}
