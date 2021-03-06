from fastapi import FastAPI,Depends, status, Response, HTTPException
from . import models 
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
from .schemas import Blog

app = FastAPI()

models.Base.metadata.create_all(bind =engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog',status_code = status.HTTP_201_CREATED)
def create(requestbody:Blog, db:Session = Depends(get_db)):
    new_blog = models.Blog(title = requestbody.title,body = requestbody.body)

    db.add(new_blog)

    db.commit()

    db.refresh(new_blog)
    return new_blog


@app.get('/blog')
def get_all_blogs(db:Session  = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',status_code = status.HTTP_200_OK)
def get_blog_id(id,response:Response,db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail =f"Blog with id {id} not available")
        
        
    return blog
