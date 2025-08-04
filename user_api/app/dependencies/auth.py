from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.utils.security import verify_access_token
from app.database.database import user_collection

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    email = payload.get("sub")

    if not email:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = await user_collection.find_one({"email": email})

    if not user or user.get("token") != token or not user.get("isactive", False):
        raise HTTPException(status_code=401, detail="Token inválido o usuario inactivo")

    return user
