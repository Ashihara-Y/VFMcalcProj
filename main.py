import sys

sys.dont_write_bytecode = True
import flet as ft
from Initial_Inputs import Initial_Inputs
from Final_Inputs import Final_Inputs
from Resultview import Results
import save_results
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
                    ft.ElevatedButton("入力確認へ", on_click=open_final_inputs),
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
                        ft.ElevatedButton("計算へ", on_click=open_save_results),
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                ),
            )
        elif page.route == "/save_results":
            # page.views.clear()
            page.views.append(
                ft.View(
                    "/save_results",
                    [
                        ft.AppBar(title=ft.Text("結果表示")),
                        Results(),
                        ft.ElevatedButton("終了", on_click=open_initial_inputs),
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

    def open_save_results(e):
        page.go("/save_results")

    def open_initial_inputs(e):
        save_results.save_ddb()
        page.go("/")

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)
