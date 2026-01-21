from fastapi import FastAPI
from .schema.post_schema import Post
import psycopg2
from psycopg2.extras import RealDictCursor
from .models import post_model , user_model
from .db.database import engine, get_db, Base
from sqlalchemy.orm import Session
from .middlewares.timing import timing_middleware
from src.routes import post_routes
from src.routes import user_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.middleware("http")(timing_middleware)

app.include_router(post_routes.router, tags=["Posts"])
app.include_router(user_routes.router, tags= ["Users"])


@app.get("/")
def home():
    return {"data": "fucked_life"}
