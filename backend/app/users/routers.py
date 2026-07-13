from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.schemas import UserResponseBasic, UserResponseRole, UserLogin
from app.users.schemas import UserResponse, RoleResponse, RoleCreate, UserCreate, Token
from app.database import get_db
from app.users.crud import get_selected_users, get_all_users, get_user, create_role
from app.users.crud import create_user, login_user
from app.dependencies import get_current_user, require_admin
from app.users.models import User


router = APIRouter(prefix="/api/users")

@router.get("/list/selected", response_model=list[UserResponseRole])
async def list_selected_users(db: AsyncSession = Depends(get_db)):
    return await get_selected_users(db)

@router.get("/list/all", response_model=list[UserResponseBasic])  
async def list_users(db: AsyncSession = Depends(get_db), 
                        current_user: User=Depends(get_current_user)):
    return await get_all_users(db)

@router.get("/{user_id}", response_model=UserResponse)
async def user_info(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    return user

@router.post("/roles", response_model=RoleResponse)
async def add_role(role: RoleCreate, 
                   db: AsyncSession = Depends(get_db), 
                   current_user: User=Depends(require_admin)):
    
        
    return await create_role(db, role)

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db:AsyncSession = Depends(get_db)):
    return await create_user(db, user)

@router.post("/login", response_model=Token)
async def verify_login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    login = await login_user(db, credentials)
    if login is None: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or Password incorrect")
    return {"access_token": login, "token_type": "bearer"}




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  