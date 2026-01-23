
from fastapi import APIRouter , Depends , status , HTTPException , Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..db.database import get_db , engine
from ..schema.user_schema import UserLogin , UserPayload
from ..schema.token_schema import Token
from ..models.user_model import User
from ..utils.hash import verify_password
from typing import List 
from ..utils.auth import create_access_token


router = APIRouter(prefix="/users")


#one way use manual jwt 

# @router.post("/login" )
# def login_user(user_data: UserLogin, db: Session = Depends(get_db)):

#     user = None

#     if user_data.username:
#         user = db.query(User).filter(User.username == user_data.username).first()

#     elif user_data.email:
#         user = db.query(User).filter(User.email == user_data.email).first()

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User doesn't exist"
#         )

#     if not verify_password(user_data.password, user.password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid credentials"
#         )

#     #convert the orm to pydantic payload
#     #pass payload dict to jwt
#     # create and return token

#     payload = UserPayload.model_validate(user)
#     token = create_access_token(payload.model_dump())

#     return {
#         "access_token" : token ,
#         "token_type" : "bearer"
#     }



#second oauth jwt by fastapi

@router.post("/login" , response_model=Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends() , db : Session = Depends(get_db)):
    # OAuth2PasswordRequestForm data 
    # {username : "u" , password : "p"}

    user = db.query(User).filter(User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    
    if not verify_password(user_credentials.password , user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Invalid Credentials")
    
    #create jwt token
    payload = UserPayload.model_validate(user)
    token = create_access_token(payload.model_dump())

    # user = db.query(User).filter(User.id == payload.id).first()
    # return user

    return Token(access_token=token)