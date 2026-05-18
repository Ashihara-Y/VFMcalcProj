import sys
sys.dont_write_bytecode = True
import flet as ft
from Landing_view import LandingContainer
from Initial_InputsT2 import Initial_Inputs
from Final_InputsT2 import Final_Inputs
from Resultview2 import Results
from view_savedT import View_saved
from Edit_result import Edit_result
import save_results
import export_to_excel
import download
import logging
import pandas as pd
import asyncio
from sqlalchemy import create_engine
from auth_manager import setup_auth
import os
from fastapi import FastAPI, Request, HTTPException
import flet.fastapi as flet_fastapi


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
@app.post("/api/webhook/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    logger.info("Received Stripe webhook: %s", payload)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        logger.error(f"Invalid payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        logger.error(f"Invalid signature: {e}")
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle the event (例: 支払い成功イベント)
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        logger.info(f"Checkout session completed: {session['id']}")
        # ここで支払い完了後の処理を実装（例: ユーザーのサブスクリプションを有効化）

    return {"status": "success"}

async def main(page: ft.Page):
    page.title = "VFM計算アプリ"
    page.vertical_alignment = ft.MainAxisAlignment.START

    def on_login_success():
        logger.info("Login successful")
        #page.session.store.set("auth0_sub", auth0_provider.get_user_id())  # 認証情報をセッションストレージに保存
        #page.update()
        asyncio.create_task(page.push_route("/")) # ログイン成功後にルートを"/"に変更してLandingContainerを表示

    auth_provider = setup_auth(page, on_login_success)

    def route_change(e=None):
        #troute = ft.TemplateRoute(page.route)
        #print("Route changed to:", page.route)
        page.views.clear()

        page.views.append(
                ft.View(
                    route="/",
                    controls=[
                        #ft.Text("Welcome to the VFM Calculator")
                        LandingContainer(
                            on_action=lambda r: asyncio.create_task(page.login(auth_provider)) if r == "login" else asyncio.create_task(page.push_route(r)),
                            current_locale='ja'
                        )
                    ],
                )
            )
        
        if page.route == "/initial_inputs":
            if not page.session.store.get("auth0_sub"):
                open_landing(e=None)  # 認証されていない場合はランディングページへ
            page.views.append(
                ft.View(
                    route="/initial_inputs", 
                    controls=[
                        ft.AppBar(title=ft.Text("初期入力"),
                                bgcolor=ft.Colors.SURFACE_CONTAINER,
                                actions=[
                                    ft.Button(content="既存の算定結果を見る", on_click=open_saved_list),
                                ],
                        ),
                        Initial_Inputs(),
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                )
            )
        

        elif page.route == "/final_inputs":
            if not page.session.store.get("auth0_sub"):
                open_landing(e=None)  # 認証されていない場合はランディングページへ
            initial_inputs = page.session.store.get("initial_inputs") 
            page.views.append(
                ft.View(
                    route="/final_inputs",
                    controls=[
                        ft.AppBar(title=ft.Text("入力確認と追加入力")),
                        Final_Inputs(initial_inputs=initial_inputs), # Final_Inputsクラスにinitial_inputsを渡す
                        #ft.ElevatedButton("計算", on_click=open_saved_list),
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                )
            )        

        elif page.route == "/results_detail":
            if not page.session.store.get("auth0_sub"):
                open_landing(e=None)  # 認証されていない場合はランディングページへ
            sel_dtimes = page.session.store.get("selected_datetime") # セッションストレージからselected_datetimeを取得
            sel_dtime = sel_dtimes[0] if sel_dtimes is not None else "No datetime selected" # 取得できない場合のデフォルト値
            page.views.append(
                ft.View(
                    route="/results_detail",
                    controls=[
                        ft.AppBar(title=ft.Text("算定結果詳細"),
                                bgcolor=ft.Colors.SURFACE_CONTAINER,
                                actions=[
                                    ft.Button(content="複製して調整", on_click=open_edit_result),
                                    ft.Button(content="結果リストに戻る", on_click=open_saved_list),
                                ],
                        ),
                        Results(selected_datetime=sel_dtime), # Resultsクラスにselected_datetimeを渡す
                        ft.Button(content="結果リストへ戻る", on_click=open_saved_list),
                        ft.Button(content="この結果をExcelに書き出す", on_click=result_to_excel),
                        ft.Button(content="出力したファイルをダウンロード", on_click=download_excel),
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                )
            )
        elif page.route == "/view_saved":
            if not page.session.store.get("auth0_sub"):
                open_landing(e=None)  # 認証されていない場合はランディングページへ
            page.views.append(
                ft.View(
                    route="/view_saved",
                    controls=[
                        #ft.AppBar(title=ft.Text("算定結果一覧")),
                        View_saved(),
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                )
            )
        elif page.route == "/edit_saved":
            if not page.session.store.get("auth0_sub"):
                open_landing(e=None)  # 認証されていない場合はランディングページへ
            sel_dtimes = page.session.store.get("selected_datetime") # セッションストレージからselected_datetimeを取得
            sel_dtime = sel_dtimes[0] if sel_dtimes is not None else "No datetime selected" # 取得できない場合のデフォルト値
            page.views.append(
                ft.View(
                    route="/edit_saved",
                    controls=[
                        ft.AppBar(title=ft.Text("算定結果調整")),
                        Edit_result(selected_datetime=sel_dtime),
                        #download.download(),
                        #ft.ElevatedButton("詳細を見る", on_click=open_results_detail),
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                )
            )
        page.update()

    async def view_pop(e):
        if e.view is not None:
            print("View popped:", e.view)
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    async def open_final_inputs(e):
        await page.push_route("/final_inputs")

    async def open_results_detail(e):
        await page.push_route("/results_detail")

    async def open_saved_list(e):
        emp_list=[]
        page.session.store.set("selected_datetime", emp_list) #initialization
        await page.push_route("/view_saved")

    async def open_edit_result(e):
        dtime = page.session.store.get("selected_datetime") #initialization
        #e.control.data = dtime
        #Results.save_to_db(self=Results(selected_datetime=Results.dtime))
        page.session.store.set("selected_datetime", dtime) #ここでは初期化は不要！
        await page.push_route("/edit_saved")

    async def open_landing(e):
        await page.push_route("/")
    
    async def result_to_excel(e):
        await export_to_excel.export_to_excel()

    async def download_excel(e):  
        await page.push_route("/download")
        await download.download()

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    #await page.push_route(page.route)
    route_change()


ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550) 