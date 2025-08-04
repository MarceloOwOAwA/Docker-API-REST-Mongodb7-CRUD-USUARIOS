from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.user import LoginRequest, UserResponse
from app.utils.security import verify_password, create_access_token
from app.database.database import get_mongo_db, user_collection
from datetime import datetime, timezone

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def login_user(login_data: LoginRequest, db=Depends(get_mongo_db)):
    # Buscar usuario por email usando user_collection
    user = await user_collection.find_one({"email": login_data.email})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    # Verificar contraseña
    if not verify_password(login_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    # Generar token
    token = create_access_token(data={"sub": user["email"]})
    now = datetime.now(timezone.utc)

    # Actualizar campos en MongoDB
    await user_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {
            "last_login": now,
            "modified": now,
            "token": token
        }}
    )

    # Devolver usuario actualizado
    user["last_login"] = now
    user["modified"] = now
    user["token"] = token
    user["id"] = str(user["_id"])  # Convertimos ObjectId a string
    return UserResponse(**user)
