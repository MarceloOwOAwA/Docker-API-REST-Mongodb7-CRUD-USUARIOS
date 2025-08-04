from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.user import UserCreate, UserOut
from app.database.database import get_mongo_db, user_collection
from app.utils.security import get_password_hash, create_access_token
from uuid import uuid4
from datetime import datetime, timezone
import re

router = APIRouter()

EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=(?:.*\d){2,}).+$'

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db=Depends(get_mongo_db)):
    # Validación de email
    if not re.match(EMAIL_REGEX, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Correo no tiene el formato correcto"
        )

    # Validación de contraseña
    if not re.match(PASSWORD_REGEX, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña no cumple con el formato requerido"
        )

    # Verificar si ya existe el correo
    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya registrado"
        )

    # Hash de contraseña
    hashed_password = get_password_hash(user.password)

    # Fechas y token
    now = datetime.now(timezone.utc)
    token = create_access_token(data={"sub": user.email})

    # Crear nuevo usuario
    user_dict = {
        "id": str(uuid4()),
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "phones": [phone.dict() for phone in user.phones],  # lista de teléfonos
        "created": now,
        "modified": now,
        "last_login": now,
        "token": token,
        "isactive": True
    }

    # Insertar en la colección usuarios
    await db["users"].insert_one(user_dict)

    # Remover password para la respuesta
    user_dict.pop("password")

    return user_dict
