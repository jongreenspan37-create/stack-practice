from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base
from datetime import date
from typing import Optional

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column (primary_key=True )
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)
    role_id: Mapped[Optional[int]] = mapped_column(ForeignKey("roles.id"), nullable=True)
    date_registered: Mapped[date] = mapped_column()

    role: Mapped["Role"] = relationship(back_populates="users")
    userprofile: Mapped["UserProfile"] = relationship(back_populates="user", uselist=False)

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    order: Mapped[int] = mapped_column(nullable=False, server_default="1")
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    users: Mapped[list["User"]] = relationship(back_populates="role")


class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    first_name: Mapped[str] = mapped_column(String(100),nullable=False)
    last_name: Mapped[str] = mapped_column(String(100),nullable=False)
    address1: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    address2: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    address3: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    postcode: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    user: Mapped["User"] = relationship(back_populates="userprofile")