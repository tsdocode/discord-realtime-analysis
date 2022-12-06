# Import database module.
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from dotenv import load_dotenv

import os

class RealtimeDB():
    def __init__(self, database_url):
        self._cred = credentials.Certificate(os.getenv("FIREBASE_KEY"))
        firebase_admin.initialize_app(
            self._cred, {
                'databaseURL': database_url
            }
        )
    def save(self, data, child):
        ref = db.reference(child)
        ref.set(data)

    def push(self, data, child):
        ref = db.reference(child).push()
        ref.set(data)

    def get(self, child):
        ref = db.reference(child)
        return ref.get()

