import flet as ft
import asyncio
#from sqlalchemy import create_engine
#import pandas as pd
#from google.cloud import firestore
from db_conf import check_data_ownership

#engine = create_engine('sqlite///VFM.db', echo=False, connect_args={"check_same_thread": False})
#db = firestore.Client()
# Calc_idは、編集画面か詳細表示画面で、セッションに保存されている前提
#calc_id = page.session.store.get("calc_id")

# main.pyのルーティングと連携させて、「編集画面「詳細表示画面」以外のログインを確認
# True/Falseを返す。Falseの時は、main.pyで、処理（open_landing）を書く。
def enforce_security_guard(page: ft.Page, target_route: str) -> bool:
    troute = ft.TemplateRoute(target_toute)
    user_id = page.session.store.get('user_id')

    if troute.match('/'):
        return True
    elif not user_id:
        logger.warning(f"未認証アクセスをブロック: {target_route}")
        asyncio.create_task(page.push_route("/"))
        return False
    elif troute.match("/edit_saved") or troute.match("/result_detail"):
        calc_id = troute.query.get("calc_id")
        if calc_id:
            has_access = check_data_ownership(calc_id, user_id=user_id)
            if not has_access:
                logger.warning(f'認可エラー：ユーザー{user_id}は、算定結果{calc_id}へのアクセス権がありません')
                asyncio.create_task(page.push_route("/view_saved"))
                return False
    else:
        return True

