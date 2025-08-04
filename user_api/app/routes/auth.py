from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserCreate, UserOut
from app.database.database import user_collection
from app.utils.security import get_password_hash, create_access_token
from pymongo.errors import DuplicateKeyError
from uuid import uuid4
from datetime import datetime, timezone

router = APIRouter()

@router.post("/registro", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    # Verifica si el usuario ya existe por email
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado."
        )

    # Hashea la contraseña antes de guardarla
    hashed_password = get_password_hash(user.password)

    # Crea el token JWT para devolverlo al crear el usuario
    token = create_access_token({"sub": user.email})

    # Fecha actual en UTC
    now = datetime.now(timezone.utc)

    # Prepara el documento para guardar en la base de datos
    user_dict = {
        "id": str(uuid4()),
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "phones": [phone.dict() for phone in user.phones],
        "created": now,
        "modified": now,
        "last_login": now,
        "token": token,
        "isactive": True
    }

    try:
        await user_collection.insert_one(user_dict)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe."
        )

    # Retorna la info usando el modelo UserOut (sin password)
    user_dict.pop("password")
    return UserOut(**user_dict)
