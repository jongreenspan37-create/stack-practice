from datetime import date
from app.users.models import User, UserProfile, Role
from app.users.schemas import (RoleCreate, UserCreate, 
                               UserResponse, UserLogin)
from app.security import hash_password, verify_password
from app.auth import create_access_token, decode_access_token
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

async def get_selected_users(db: AsyncSession):
    sql = (
        select(
            User.id,
            User.email,
            UserProfile.first_name,
            UserProfile.last_name,
            Role.name.label("role_name"),
        )
        .join(User.userprofile, isouter=True)
        .join(User.role, isouter=True)
    )
    result = await db.execute(sql)
    return result.mappings().all()

async def get_all_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()



async def get_user(db:AsyncSession, user_id: int):
    sql = (select (User)
        .options(selectinload(User.userprofile))
        .options(joinedload(User.role))
        .where(User.id== user_id)
    )
    result = await db.execute(sql)
    return result.scalars().one_or_none()

async def create_role(db:AsyncSession, role: RoleCreate):
    new_role = Role(name=role.name, order=role.order)
    db.add(new_role)
    await db.commit()
    await db.refresh(new_role)
    return new_role

async def create_user(db:AsyncSession, user: UserCreate):
    hashed_pass = hash_password(user.password)
    new_user = User(email=user.email, 
                    hashed_password=hashed_pass, 
                    date_registered=date.today())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    new_profile = UserProfile(user_id=new_user.id,
                              first_name=user.first_name,
                              last_name=user.last_name,
                              address1=user.address1, 
                              address2=user.address2,
                              address3=user.address3,
                              postcode=user.postcode
                              )
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_user, attribute_names=["email", "is_active", "is_admin", "date_registered", "role", "userprofile"])
    

    return new_user

async def get_user_by_email(db: AsyncSession, email: str):
    sql = select(User).where(User.email == email)
    result = await db.execute(sql)
    return result.scalars().one_or_none()

async def login_user (db:AsyncSession, credentials: UserLogin):
    user = await get_user_by_email(db, credentials.email)
    if user is None:
        return None
    if not verify_password(credentials.password, user.hashed_password):
        return None
    token = create_access_token(data={"sub": str(user.id)})
    return token
    
