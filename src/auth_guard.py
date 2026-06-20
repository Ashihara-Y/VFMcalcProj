import flet as ft
from sqlalchemy import create_engine
import pandas as pd
from google.cloud import firestore

engine = create_engine('sqlite///VFM.db', echo=False, connect_args={"check_same_thread": False})
db = firestore.Client()
# Calc_idは、編集画面か詳細表示画面で、セッションに保存されている前提
calc_id = page.session.store.get("calc_id")

# main.pyのルーティングと連携させて、「編集画面「詳細表示画面」以外のログインを確認
# True/Falseを返す。Falseの時は、main.pyで、処理（open_landing）を書く。
def verify_access_permission(page: ft.Page) -> bool:
    current_user = page.session.store.get("user_id")
    auth0_sub = page.auth.user.id

    if not current_user or not auth0_sub:
        return False
    else:
        return True

# 「編集画面」または「詳細画面」へのアクセスを検証する
def check_page_permission(page: ft.Page, current_route: str) ->bool:
    troute = ft.TemplateRoute(current_route)
    user_id = page.session.store.get("user_id")
    # 当該算定結果（calc_id）のレコード上のuser_idが、今のログインユーザーのuser_idと等しいか、
    # または、該当レコードのis_sharedがTrueであるかを検証する
    # current_userはログインユーザID、auth0_subは認証情報
    # 
    current_user = page.session.store.get("user_id")
    auth0_sub = page.auth.user.id
    #auth_doc_ref = db.collection('auth_identities').document(auth0_sub)
    #auth_doc = auth_doc_ref.get()

    if not user_id:
        if troute.route in ["/", ""]:
            return True
        return False
    # 編集画面・詳細画面へのアクセス時、他人のデータであれば共有設定をチェック
    if troute.match("/edit_saved") or troute.match("/result_detail"):
        calc_id = troute.query.get("calc_id")
        if calc_id:
            # SELECT user_id, is_shared FROM results_table WHERE calc_id = :calc_id
            # user_id == auth0_sub or is_shared == True -> True
            pass
    return True