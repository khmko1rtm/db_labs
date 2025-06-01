from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# --- DB setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# --- FastAPI app
app = FastAPI(
    docs_url="/docs",
    redoc_url=None,
    swagger_ui_parameters={"persistAuthorization": True}
)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ========================
#       DB MODELS
# ========================

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)

class RoleDB(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

class PermissionDB(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

# --- USER
class UserCreate(BaseModel):
    username: str
    email: str

class User(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        from_attributes = True

# --- ROLE
class RoleCreate(BaseModel):
    name: str

class Role(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

# --- PERMISSION
class PermissionCreate(BaseModel):
    action: str

class Permission(BaseModel):
    id: int
    action: str
    class Config:
        from_attributes = True

# ========================
#       USER CRUD
# ========================

@app.post("/user/", response_model=User)
def create_user(user: UserCreate):
    db = SessionLocal()
    db_user = UserDB(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user

@app.get("/user/", response_model=List[User])
def get_users():
    db = SessionLocal()
    users = db.query(UserDB).all()
    db.close()
    return users

@app.get("/user/{user_id}", response_model=User)
def get_user(user_id: int):
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    db.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/user/{user_id}", response_model=User)
def update_user(user_id: int, user: UserCreate):
    db = SessionLocal()
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not db_user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = user.username
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user

@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    db.close()
    return {"ok": True}

# ========================
#       ROLE CRUD
# ========================

@app.post("/role/", response_model=Role)
def create_role(role: RoleCreate):
    db = SessionLocal()
    db_role = RoleDB(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    db.close()
    return db_role

@app.get("/role/", response_model=List[Role])
def get_roles():
    db = SessionLocal()
    roles = db.query(RoleDB).all()
    db.close()
    return roles

@app.get("/role/{role_id}", response_model=Role)
def get_role(role_id: int):
    db = SessionLocal()
    role = db.query(RoleDB).filter(RoleDB.id == role_id).first()
    db.close()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@app.put("/role/{role_id}", response_model=Role)
def update_role(role_id: int, role: RoleCreate):
    db = SessionLocal()
    db_role = db.query(RoleDB).filter(RoleDB.id == role_id).first()
    if not db_role:
        db.close()
        raise HTTPException(status_code=404, detail="Role not found")
    db_role.name = role.name
    db.commit()
    db.refresh(db_role)
    db.close()
    return db_role

@app.delete("/role/{role_id}")
def delete_role(role_id: int):
    db = SessionLocal()
    role = db.query(RoleDB).filter(RoleDB.id == role_id).first()
    if not role:
        db.close()
        raise HTTPException(status_code=404, detail="Role not found")
    db.delete(role)
    db.commit()
    db.close()
    return {"ok": True}

# ========================
#     PERMISSION CRUD
# ========================

@app.post("/permission/", response_model=Permission)
def create_permission(permission: PermissionCreate):
    db = SessionLocal()
    db_permission = PermissionDB(**permission.dict())
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    db.close()
    return db_permission

@app.get("/permission/", response_model=List[Permission])
def get_permissions():
    db = SessionLocal()
    permissions = db.query(PermissionDB).all()
    db.close()
    return permissions

@app.get("/permission/{permission_id}", response_model=Permission)
def get_permission(permission_id: int):
    db = SessionLocal()
    permission = db.query(PermissionDB).filter(PermissionDB.id == permission_id).first()
    db.close()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission

@app.put("/permission/{permission_id}", response_model=Permission)
def update_permission(permission_id: int, permission: PermissionCreate):
    db = SessionLocal()
    db_permission = db.query(PermissionDB).filter(PermissionDB.id == permission_id).first()
    if not db_permission:
        db.close()
        raise HTTPException(status_code=404, detail="Permission not found")
    db_permission.action = permission.action
    db.commit()
    db.refresh(db_permission)
    db.close()
    return db_permission

@app.delete("/permission/{permission_id}")
def delete_permission(permission_id: int):
    db = SessionLocal()
    permission = db.query(PermissionDB).filter(PermissionDB.id == permission_id).first()
    if not permission:
        db.close()
        raise HTTPException(status_code=404, detail="Permission not found")
    db.delete(permission)
    db.commit()
    db.close()
    return {"ok": True}

# ========================
#       Redirect to Docs
# ========================
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")
