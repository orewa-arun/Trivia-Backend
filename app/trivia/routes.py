from fastapi import APIRouter, Depends, HTTPException

from app.db.dependencies import get_db
from .models import *
from .service import *


router = APIRouter(prefix="/trivia", tags=["Trivia"])


@router.post("/start")
def start_game(req: StartSessionRequest, db=Depends(get_db)):
    if req.guest_user_name:
        return create_game_session(req.uid, db, req.guest_user_name)
    return create_game_session(req.uid, db)


@router.post("/next")
def next_question(session_id: int, db=Depends(get_db)):
    return get_next_question(session_id, db)


@router.post("/answer")
def submit_answer(answer: MCQAnswerRequest, db=Depends(get_db)):
    return handle_answer(answer, db)


@router.post("/complete")
def complete_game(session_id: int, db=Depends(get_db)):
    return mark_game_complete(session_id, db)


@router.post("/leaderboard", response_model=List[LeaderboardEntry])
def get_leaderboard(db=Depends(get_db)):
    return fetch_leaderboard(db)