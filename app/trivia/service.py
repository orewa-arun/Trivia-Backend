from app.trivia.models import MCQAnswerRequest
from app.trivia.repository import fetch_ad_content_by_id, fetch_next_unanswered_ad_question, fetch_next_unanswered_question, finalize_session, get_or_create_guest_user_by_uid, get_top_leaderboard_entries, init_session, store_answer_and_update_score
from app.utlis.logger import get_logger


log = get_logger(__name__)


# uid is passed as "guest" for users who are not signed in
def create_game_session(uid: str, db, guest_user_name: str = "Guest user"):
    user = get_or_create_guest_user_by_uid(uid, guest_user_name, db)
    log.debug(f"User created or fetched: {user['name']} with id: {user['id']}")
    return init_session(user["id"], db)


def get_next_question(session_id: int, db):
    return fetch_next_unanswered_question(session_id, db)


def get_next_ad_question(session_id: int, db):
    return fetch_next_unanswered_ad_question(session_id, db)


def get_ad_content(ad_id, db):
    return fetch_ad_content_by_id(ad_id, db)


def handle_answer(answer: MCQAnswerRequest, db):
    return store_answer_and_update_score(answer, db)


def mark_game_complete(session_id: int, db):
    return finalize_session(session_id, db)

def fetch_leaderboard(db):
    return get_top_leaderboard_entries(db)