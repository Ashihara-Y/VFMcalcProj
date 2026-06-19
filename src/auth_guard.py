import flet as ft
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('sqlite///VFM.db', echo=False, connect_args={"check_same_thread": False})

def verify_access_permission(page: ft.Page, calc_id: str) -> bool:
    current_user = page.session.store.get("auth0_sub")
    if not current_user:
        return False
    # record = pd.read_query("SELECT user_id, is_shared FROM results WHERE id = :calc_id", calc_id=calc_id)
    if not record:
        return False
    if record['user_id']

def check_page_permission(page: ft.Page, current_route: str) ->bool:
    troute = ft.TemplateRoute(current_route)
    auth0_sub = page.session.store.get("auth0_sub")
    if not auth0_sub:
        if troute.route in ["/", ""]
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