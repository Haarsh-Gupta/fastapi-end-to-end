from fastapi import APIRouter , Depends , status , HTTPException , Response
from sqlalchemy.orm import Session
from ..db.database import get_db , engine
from ..schema.user_schema import UserLogin , UserOut , UserRegister, UserUpdate
from ..models.user_model import User
from ..models import user_model
from ..utils.hash import get_hashed_password , verify_password
from typing import List 

router = APIRouter(prefix="/users")

@router.post("/register" , response_model= UserOut , status_code= status.HTTP_201_CREATED)
def register_user(user: UserRegister , db : Session = Depends(get_db)):
    
    user_dict = user.model_dump()
    user_dict['password'] = get_hashed_password(user_dict["password"])
    add_user = User(**user_dict) 
    db.add(add_user)
    db.commit()
    db.refresh(add_user)

    return add_user


@router.get("/" , response_model=List[UserOut])
def get_all_users(db : Session = Depends(get_db)):

    all_users = db.query(User).all()

    return all_users


@router.get("/{id}" , status_code=status.HTTP_302_FOUND , response_model=UserOut)
def get_by_id (id: int, db : Session = Depends(get_db)):

    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"User with id {id} doesn't exist")
    
    return user


@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id : int , db : Session = Depends(get_db)):

    query = db.query(User).filter(User.id == id)
    user = query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"User with id {id} doesn't exist")
    
    query.delete(synchronize_session=False)
    db.commit()


@router.put("/{id}", response_model=UserOut)
def update_user(id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} doesn't exist"
        )

    data = user_data.model_dump(exclude_unset=True)

    if "name" in data:
        user.name = data["name"]

    if "phone" in data:
        user.phone = data["phone"]

    if "password" in data:
        user.password = get_hashed_password(data["password"])

    db.commit()
    db.refresh(user)

    return user

@router.post("/login", response_model=UserOut)
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):

    user = None

    if user_data.username:
        user = db.query(User).filter(User.username == user_data.username).first()

    elif user_data.email:
        user = db.query(User).filter(User.email == user_data.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User doesn't exist"
        )

    if not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    return user
