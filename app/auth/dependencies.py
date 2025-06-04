from fastapi import Request, HTTPException, Depends
from firebase_admin import auth as firebase_auth
from app.db.dependencies import get_db
from app.repository.auth_repository import is_email_allowed
from app.utlis.logger import get_logger, log_with_method


logger = get_logger(__name__)


def verify_firebase_token(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")

    try:
        scheme, token = auth_header.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid auth scheme")

        decoded_token = firebase_auth.verify_id_token(token)
        return decoded_token

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid or expired token: {str(e)}")


async def verify_firebase_token_and_email_is_allowed(request: Request, db=Depends(get_db)):

    log_with_method(logger, "debug", "started")

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = auth_header.split("Bearer ")[1]

    try:
        decoded_token = firebase_auth.verify_id_token(token)
        email = decoded_token.get("email")
        logger.debug(f"Decoded Firebase email: {email}")

        if not email:
            raise HTTPException(status_code=403, detail="No email in token")

        if not is_email_allowed(email, db):
            logger.debug(f"Email not allowed: {email}")
            raise HTTPException(status_code=403, detail="Access denied")

        log_with_method(logger, "debug", "ends")
        return decoded_token

    except Exception as e:
        logger.debug(f"Firebase verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")