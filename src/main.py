import sys
sys.dont_write_bytecode = True
import flet as ft
from Initial_InputsT import Initial_Inputs
from Final_InputsT2 import Final_Inputs
from Resultview2 import Results
from view_saved import View_saved
import save_results
import export_to_excel
import download
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def main(page: ft.Page):
    page.title = "VFM計算アプリ"
    page.vertical_alignment = ft.MainAxisAlignment.START

    def route_change():
        #print("Route changed to:", page.route)
        page.views.clear()
        page.views.append(
            ft.View(
                route="/",
                controls=[
                    ft.AppBar(title=ft.Text("初期入力")),
                    Initial_Inputs(),
                ],
                scroll=ft.ScrollMode.ALWAYS,
            )
        )
        if page.route == "/final_inputs":
            page.views.append(
                ft.View(
                    route="/final_inputs",
                    controls=[
                        ft.AppBar(title=ft.Text("入力確認と追加入力")),
                        Final_Inputs()
                        #ft.ElevatedButton("計算", on_click=open_saved_list),
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                )
            )
        if page.route == "/results_detail":
            page.views.append(
                ft.View(
                    route="/results_detail",
                    controls=[
                        ft.AppBar(title=ft.Text("算定結果詳細")),
                        Results(),
                        ft.Button(content="結果リストへ戻る", on_click=open_saved_list),
                        ft.Button(content="この結果をExcelに書き出す", on_click=result_to_excel),
                        ft.Button(content="出力したファイルをダウンロード", on_click=download_excel),
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                )
            )
        if page.route == "/view_saved":
            page.views.append(
                ft.View(
                    route="/view_saved",
                    controls=[
                        ft.AppBar(title=ft.Text("算定結果一覧(要約表を長めにクリックすると詳細に遷移します)")),
                        View_saved(),
                        ft.Button(content="詳細を見る", on_click=open_results_detail),
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                )
            )
        if page.route == "/download":
            page.views.append(
                ft.View(
                    route="/download",
                    controls=[
                        ft.AppBar(title=ft.Text("出力ファイルのダウンロード")),
                        download.download(),
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

    #def open_results_summary(e):
    #    page.go("/results_summary")

    async def open_results_detail(e):
        #Results()        
        await page.push_route("/results_detail")

    async def open_saved_list(e):
        await page.push_route("/view_saved")

    async def open_initial_inputs(e):
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


ft.run(main)
