### INITIALISING FIREBASE!!
from app.auth import firebase


import logging
from app.auth.dependencies import verify_firebase_token
from fastapi import FastAPI, Depends
from app.auth.test_routes import router as test_router
from fastapi.middleware.cors import CORSMiddleware
from app.trivia.routes import router as trivia_router


logging.basicConfig(
    level=logging.DEBUG,  # This enables debug logs globally
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="THE GREAT INDIAN TRIVIA",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    test_router,
    dependencies=[Depends(verify_firebase_token)]
)
app.include_router(
    trivia_router
)


@app.post("/")
def public():
    logger.info("Accessed public route")
    return {"msg": "Welcome to the public route"}