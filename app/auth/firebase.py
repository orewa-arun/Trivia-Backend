import firebase_admin
from firebase_admin import credentials
import os
import json
from dotenv import load_dotenv

load_dotenv()

if not firebase_admin._apps:
    firebase_json = os.getenv("FIREBASE_CREDENTIALS")

    if not firebase_json:
        raise ValueError("FIREBASE_CREDENTIALS environment variable is missing.")

    # Parse the JSON string into a dictionary
    firebase_dict = json.loads(firebase_json)

    # Use the dictionary to create credentials
    cred = credentials.Certificate(firebase_dict)
    firebase_admin.initialize_app(cred)