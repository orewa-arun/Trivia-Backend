from dotenv import load_dotenv
from fastapi import APIRouter
from app.utlis.logger import get_logger


router = APIRouter(prefix="/test")
load_dotenv()
logger = get_logger(__name__)


@router.post("/send")
def send_money():
    return {"status": "money sent"}


@router.get("/balance")
def get_balance():
    return {"amount": 1000}