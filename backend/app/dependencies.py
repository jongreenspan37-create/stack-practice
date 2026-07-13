from Fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from app.users.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth import decode_access_token
from app.database import get_db
from app.users.crud import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = await get_user(db, int(user_id))
    if user is None or not user.is_active:
        raise credentials_exception

    return user
    
    



async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user