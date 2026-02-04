from fastapi import FastAPI
from .db.database import engine, get_db, Base
from .middlewares.timing import timing_middleware
from src.routes import post_routes, user_routes , auth_router , vote_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.middleware("http")(timing_middleware)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post_routes.router, tags=["Posts"])
app.include_router(user_routes.router, tags= ["Users"])
app.include_router(auth_router.router , tags= ["Authorization"])
app.include_router(vote_routes.router , tags=["Vote Post"])


@app.get("/" , tags=["Health"])
def home():
    return {"data": "fucked_life"}
