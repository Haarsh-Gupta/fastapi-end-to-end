from fastapi import FastAPI
from .schema.post_schema import Post
import psycopg2
from psycopg2.extras import RealDictCursor
from .models import post_model , user_model
from .db.database import engine, get_db, Base
from sqlalchemy.orm import Session
from .middlewares.timing import timing_middleware
from src.routes import post_routes, user_routes , auth_router , vote_routes


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.middleware("http")(timing_middleware)

app.include_router(post_routes.router, tags=["Posts"])
app.include_router(user_routes.router, tags= ["Users"])
app.include_router(auth_router.router , tags= ["Authorization"])
app.include_router(vote_routes.router , tags=["Vote Post"])


@app.get("/" , tags=["Health"])
def home():
    return {"data": "fucked_life"}
