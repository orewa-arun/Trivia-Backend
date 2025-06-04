from fastapi import Depends
from app.db.dependencies import get_db
from app.utlis.logger import get_logger


logger = get_logger(__name__)


def is_email_allowed(email: str, db=Depends(get_db)) -> bool:
    logger.debug(f"Checking DB for email access: {email}")
    with db.cursor() as cur:
        cur.execute("SELECT is_active FROM allowed_users WHERE email = %s", (email,))
        return cur.fetchone() is not None