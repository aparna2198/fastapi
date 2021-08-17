from fastapi import FastAPI
from typing import Optional
import os 
import sys
current_dir = os.path.dirname('main')
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0,parent_dir)
from .basemodel import Blog
app = FastAPI()

@app.get("/")
def home():
    return "Home"

@app.get('/blog')
def index(limit=10,published:bool = True, sort : Optional[str] = None):
    
    if published:
        return {"data":f"{limit} {published} blogs from URL "}
    else:
        return {"data":"all blogs"}


@app.get("/blog/unpublished")
def unpublished():
    return {"data":"all unpublished blogs"}

@app.get("/blog/{id}/comments")
def comments(id,limit=10):
    return {"comments":{limit}}

@app.get("/blog/{id}")
def show(id:int):
    return {"data":id}
 

@app.post('/blog')
def create_blog(requestbody:Blog):
    return {"data":f"Blog with title {requestbody.title} is created"}

 