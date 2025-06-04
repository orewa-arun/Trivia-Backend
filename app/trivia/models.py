from pydantic import BaseModel
from typing import List, Optional


class StartSessionRequest(BaseModel):
    uid: str
    guest_user_name : Optional[str] # Will be used for users who are not signed in


class MCQQuestionOut(BaseModel):
    id: int
    mcq_question: str
    mcq_options: List[str]
    mcq_correct_index: int


class MCQAnswerRequest(BaseModel):
    session_id: int
    question_id: int
    selected_index: int


class LeaderboardEntry(BaseModel):
    name: str
    score: int
    completed_at: Optional[str]