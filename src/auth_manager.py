import os
import flet as ft
from flet.auth.providers.auth0_oauth_provider import Auth0OAuthProvider
from dotenv import load_dotenv
load_dotenv()

# === Auth0 設定情報 ===
# ※本番環境では必ず .env ファイル等の環境変数から読み込んでください
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
REDIRECT_URL = os.getenv("REDIRECT_URL") # Flet開発時のデフォルト

def get_auth0_provider():
    """Auth0プロバイダのインスタンスを生成して返す"""
    return Auth0OAuthProvider(
        domain=AUTH0_DOMAIN,
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        redirect_url=REDIRECT_URL
    )

def setup_auth(page: ft.Page, on_login_success):
    """
    FletのPageオブジェクトに対し、ログイン時のイベントを紐付ける。
    on_login_success: ログイン成功時に実行したい関数（画面遷移など）
    """
    provider = get_auth0_provider()

    def on_login(e):
        if e.error:
            # ログインキャンセルやエラー時の処理
            print(f"Auth0 Login Error: {e.error}")
            page.snack_bar = ft.SnackBar(ft.Text(f"ログインに失敗しました: {e.error}"), open=True)
            page.update()
        else:
            # ログイン成功時：Auth0のID(sub)をFletのセッションに保存
            page.session.store.set("auth0_sub", page.auth.user.id)
            #if page.auth.user.email:
            #    page.session.store.set("user_email", page.auth.user.email)
            
            print(f"Login Success! User ID: {page.auth.user.id}")
            
            # 成功時のコールバック関数（ダッシュボード等への遷移）を実行
            on_login_success()

    # Pageにイベントを登録
    page.on_login = on_login
    
    # 呼び出し元で page.login(provider) を実行できるよう、プロバイダを返す
    return provider