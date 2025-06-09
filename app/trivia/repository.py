from typing import Optional
from fastapi import HTTPException
from app.utlis.logger import get_logger
from .models import MCQAnswerRequest
from fastapi import HTTPException


log = get_logger(__name__)


def get_or_create_guest_user_by_uid(uid: str, guest_user_name: str, db):
    with db.cursor() as cur:
        if uid == "guest":
            return create_guest_user(cur, guest_user_name)
        else:
            return get_registered_user(cur, uid)


def create_guest_user(cur, guest_user_name):
    try:
        cur.execute(
            "INSERT INTO users (name) VALUES (%s) RETURNING id", 
            (guest_user_name,)
        )
        user = cur.fetchone()
        log.debug(f"Guest user created with id : {user[0]}")
        if user:
            return {"id": user[0], "name": guest_user_name}
        raise HTTPException(status_code=400, detail="Guest user creation failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def get_registered_user(cur, uid):
    try:
        cur.execute("SELECT id FROM users WHERE uid = %s", (uid,))
        user = cur.fetchone()
        if user:
            return {"id": user[0], "name": "Registered User"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    raise HTTPException(status_code=404, detail="User not registered")


def init_session(user_id: int, db):
    try:
        with db.cursor() as cur:
            cur.execute("INSERT INTO game_sessions (user_id) VALUES (%s) RETURNING id", (user_id,))
            session = cur.fetchone()
            log.debug(f"Game session created with id: {session[0]}")
        return {"session_id": session[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def fetch_next_unanswered_question(session_id: int, category: Optional[str], sub_category: Optional[str], db):
    try:
        query = """
            SELECT q.id as id, q.question, q.options, q.question_type, q.category, q.sub_category, COUNT(a.id) as answered
            FROM questions q
            LEFT JOIN user_answers a ON q.id = a.question_id AND a.session_id = %s
            WHERE q.category NOT IN ('ad')
        """
        params: list[object] = [session_id]

        # Optional filters
        if category:
            query += " AND q.category = %s"
            params.append(category)
        if sub_category:
            query += " AND q.sub_category = %s"
            params.append(sub_category)

        query += """
            GROUP BY q.id
            HAVING COUNT(a.id) = 0
            ORDER BY q.id ASC
            LIMIT 1
        """

        with db.cursor() as cur:
            cur.execute(query, tuple(params))
            question = cur.fetchone()
            if not question:
                raise HTTPException(status_code=404, detail="No more questions")
            return {
                "id": question[0],
                "question": question[1],
                "options": question[2],
                "question_type": question[3],
                "category": question[4],
                "sub_category": question[5]
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        

def fetch_next_unanswered_ad_question(session_id: int, db):
    try:
        with db.cursor() as cur:
            cur.execute("""
                SELECT q.id as id, q.question, q.options, q.question_type, q.category, COUNT(a.id) as answered
                FROM questions q
                LEFT JOIN user_answers a ON q.id = a.question_id AND a.session_id = %s
                WHERE q.category IN ('ad')
                GROUP BY q.id
                HAVING COUNT(a.id) = 0
                ORDER BY q.id ASC
                LIMIT 1
            """, (session_id,))
            question = cur.fetchone()
            log.debug(f"Fetched question: {question}")
            if not question:
                raise HTTPException(status_code=404, detail="No more questions")
            return {
                "id": question[0],
                "question": question[1],
                "options": question[2],
                "question_type": question[3],
                "category": question[4],
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    
'''
    The user can answer a question only once, 
    but there is no check preventing the user from answering the same question multiple times here,
    we show the next question that the user has not answered yet using the fetch_next_unanswered_ad_question
'''
def store_answer_and_update_score(answer: MCQAnswerRequest, db):
    try:
        with db.cursor() as cur:
            cur.execute("SELECT correct_index FROM questions WHERE id = %s", (answer.question_id,))
            correct = cur.fetchone()
            log.info("Correct answer fetched: %s", correct)
            
            # selected_index = -1 if no option is selected within the time limit
            is_correct = (correct[0] == answer.selected_index)

            cur.execute("""
                INSERT INTO user_answers (session_id, question_id, selected_index, is_correct)
                VALUES (%s, %s, %s, %s)
            """, (answer.session_id, answer.question_id, answer.selected_index, is_correct))
            if is_correct:
                cur.execute("UPDATE game_sessions SET score = score + 1 WHERE id = %s", (answer.session_id,))

            return {"correct": correct[0], "is_correct": is_correct}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def finalize_session(session_id: int, db):
    try:
        with db.cursor() as cur:
            cur.execute("UPDATE game_sessions SET completed_at = CURRENT_TIMESTAMP WHERE id = %s", (session_id,))
            return {"status": "completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


'''
    No check is made if the session is completed or not, must be handled from front-end
'''
def get_top_leaderboard_entries(db):
    try:
        with db.cursor() as cur:
            cur.execute("""
                SELECT l.user_id, l.name, l.score, l.completed_at FROM leaderboard l WHERE l.completed_at IS NOT NULL
            """)
            result = cur.fetchall()
            log.info("Fetched leaderboard entries: %s", result)
            return [{"user_id": r[0], "name": r[1], "score": r[2], "completed_at": str(r[3])} for r in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    

def fetch_ad_content_by_id(ad_id: int, db):
    try:
        with db.cursor() as cur:
            cur.execute("SELECT id, title, content, duration, image_url FROM ads WHERE id = %s", (ad_id,))
            ad_content = cur.fetchone()
            log.debug(f"Fetched ad content: {ad_content}")
            if not ad_content:
                raise HTTPException(status_code=404, detail="Ad not found")
            return {
                "id": ad_content[0],
                "title": ad_content[1],
                "content": ad_content[2],
                "duration": ad_content[3],
                "image_url": ad_content[4],
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")