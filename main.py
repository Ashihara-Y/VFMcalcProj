import sys
sys.dont_write_bytecode = True
import flet as ft
from Initial_Inputs import Initial_Inputs
from Final_Inputs import Final_Inputs
from Resultview import Results
from view_saved import View_saved
import save_results
#import logging

# from save_results import saveToDB


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
                    #ft.ElevatedButton("入力確認へ", on_click=open_final_inputs),
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
                        ft.AppBar(title=ft.Text("入力確認")),
                        Final_Inputs(),
                        #ft.ElevatedButton("計算", on_click=open_saved_list),
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                ),
            )
        #elif page.route == "/results_summary":
        #    # page.views.clear()
        #    page.views.append(
        #        ft.View(
        #            "/results_summary",
        #            [
        #                ft.AppBar(title=ft.Text("結果要約")),
        #                Results(),
        #                ft.ElevatedButton("結果一覧", on_click=open_saved_list),
        #            ],
        #            scroll=ft.ScrollMode.ALWAYS,
        #        ),
        #    )
        elif page.route == "/results_detail":
            # page.views.clear()
            page.views.append(
                ft.View(
                    "/results_detail",
                    [
                        ft.AppBar(title=ft.Text("結果詳細")),
                        Results(),
                        ft.ElevatedButton("結果リストへ戻る", on_click=open_saved_list),
                        ft.ElevatedButton("この結果をExcelに書き出す", on_click=result_to_excel),
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
                        ft.AppBar(title=ft.Text("結果一覧")),
                        View_saved(),
                        ft.ElevatedButton("詳細を見る", on_click=open_results_detail),
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

    def open_results_summary(e):
        page.go("/results_summary")

    def open_results_detail(e):
        #Results()        
        page.go("/results_detail")

    def open_saved_list(e):
        page.go("/view_saved")

    def open_initial_inputs(e):
        page.go("/")
    
    def result_to_excel(e):
        Results.export_to_excel()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)
