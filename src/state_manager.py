import flet as ft
from google.cloud import firestore_v1

db = firestore_v1.Client()

class StateManager:
    @staticmethod
    async def check_user_status(page: ft.Page, user_sub: str):
        doc_ref = db.collection("users").document(user_sub)
        doc = await doc_ref.get()

        if doc.exists:
            data = doc.to_dict()
            
            page.session.store.set("is_paid", data.get("is_paid", False))
            page.session.store.set("expire_at", data.get("expire_at"))
        else:
            page.session.store.set("is_paid", False)
            