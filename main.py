from charset_normalizer import from_bytes
from fastapi import FastAPI, Depends, status, HTTPException
# from fastapi.security import OAuth2PasswordRequestForm
import models, schemas, hashing
from datetime import datetime, timedelta
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional 
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm ,OAuth2PasswordBearer

models.Base.metadata.create_all(engine)   
SECRET_KEY = "09d25e094faabhgfdrgf7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()
#@app.get('/blog')
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


#############################################################

@app.post('/login',tags=["Login"])
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session= Depends(get_db)):
    user= db.query(models.User).filter(models.User.email== request.username).first()
    
    if not hashing.Hash.verify(user.password,request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password") 
    #generate a jwt token and return 
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token}



#######################################################################

#@app.get("/blog/token")
def get_token():
    data = {'info': 'information'}
    token = create_access_token(data=data)
    return{"token":token}

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # return the generated token
    return encoded_jwt



# the endpoint to verify the token
#@app.post("/blog/verify_token")
async def verify_token(token: str):
    try:
        # try to decode the token, it will
        # raise error if the token is not correct
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        #return payload
        email: str = payload.get("sub")
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},)

    return verify_token(data)
##########################################################################
####BLOG####



@app.get('/blog',tags=['Blogs'])
def all(db: Session=Depends(get_db),current_user: schemas.User = Depends(get_current_user)):
    blogs= db.query( models.Blog).all()
    return blogs


@app.post('/blog',tags=['Blogs'])
def create(request: schemas.Blog, db: Session=Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    new_blog= models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()  
    db.refresh(new_blog)
    return new_blog

@app.get('/blog/{id}',tags=['Blogs'])
def show (id,db: Session=Depends(get_db)):
   blog= db.query(models.Blog).filter(models.Blog.id==id).first()
   return blog


####################################################
############USER#########


# @app.post('/user', response_model=schemas.Show_user,tags=['Users'])
@app.post('/user',tags=['Users'])
def create_user(request:schemas.User, db: Session= Depends(get_db)):
    #encrypted password!!!
    #hashed_Password= pwd.cxt.hash(request.password)
    new_user= models.User(name=request.name, email= request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()  
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}',response_model=schemas.Show_user,tags=['Users'])
def get_user(id:int,db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    return user.show(id,db)