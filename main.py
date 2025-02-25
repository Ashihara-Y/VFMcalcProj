import sys
sys.dont_write_bytecode = True
import flet as ft
from Initial_Inputs import Initial_Inputs
from Final_Inputs import Final_Inputs
from Resultview2 import Results
from view_saved import View_saved
import save_results
import export_to_excel
import download
import logging

logging.basicConfig(level=logging.DEBUG)

def main(page: ft.Page):
    page.title = "VFM計算アプリ"
    print("Initial Inputs", page.route)

    def route_change(e):
        print("Route changed to:", e.route)
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("初期入力")),
                    Initial_Inputs(),
                ],
                scroll=ft.ScrollMode.ALWAYS,
            ),
        )
        if page.route == "/final_inputs":
            # page.views.clear()
            page.views.append(
                ft.View(
                    "/final_inputs",
                    [
                        ft.AppBar(title=ft.Text("入力確認と追加入力")),
                        Final_Inputs(),
                        #ft.ElevatedButton("計算", on_click=open_saved_list),
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                ),
            )
        elif page.route == "/results_detail":
            # page.views.clear()
            page.views.append(
                ft.View(
                    "/results_detail",
                    [
                        ft.AppBar(title=ft.Text("算定結果詳細")),
                        Results(),
                        ft.ElevatedButton("結果リストへ戻る", on_click=open_saved_list),
                        ft.ElevatedButton("この結果をExcelに書き出す", on_click=result_to_excel),
                        ft.ElevatedButton("出力したファイルをダウンロード", on_click=download_excel),
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                ),
            )
        elif page.route == "/view_saved":
            # page.views.clear()
            page.views.append(
                ft.View(
                    "/view_saved",
                    [
                        ft.AppBar(title=ft.Text("算定結果一覧(要約表を長めにクリックすると詳細に遷移します)")),
                        View_saved(),
                        ft.ElevatedButton("詳細を見る", on_click=open_results_detail),
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                ),
            )
        elif page.route == "/download":
            # page.views.clear()
            page.views.append(
                ft.View(
                    "/download",
                    [
                        ft.AppBar(title=ft.Text("出力ファイルのダウンロード")),
                        download.download(),
                        #ft.ElevatedButton("詳細を見る", on_click=open_results_detail),
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                ),
            )
        page.update()

    def view_pop(e):
        print("View popped:", e.view)
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    def open_final_inputs(e):
        page.go("/final_inputs")

    #def open_results_summary(e):
    #    page.go("/results_summary")

    def open_results_detail(e):
        #Results()        
        page.go("/results_detail")

    def open_saved_list(e):
        page.go("/view_saved")

    def open_initial_inputs(e):
        page.go("/")
    
    def result_to_excel(e):
        export_to_excel.export_to_excel()

    def download_excel(e):  
        page.go("/download")
        download.download()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)
