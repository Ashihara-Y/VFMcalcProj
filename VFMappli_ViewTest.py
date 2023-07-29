import flet
from flet import (AppBar, ButtonStyle, Column, Container, ElevatedButton, Page, Text, View, colors, icons, padding, theme)
from Flet_inputDialogTest_class import Initial_Inputs

initial_inputs = Initial_Inputs()

def main(page: Page):
    page.title = "VFM計算アプリ"
    print("Initial Inputs", page.route)

    def route_change(e):
        print("Route changed to:", e.route)
        page.views.clear()
        page.views.append(
            View(
                "/",
                
                [   
                    AppBar(title=Text("VFM計算アプリ Initial Inputs")),
                    initial_inputs,
                    ElevatedButton("Go to Final Inputs", on_click=open_final_inputs),
                ],
            ), 
        )
        if page.route == "/final_inputs":
            page.views.append(
                View(
                    "/final_inputs",
                    [
                        AppBar(title=Text("VFM計算アプリ Final Inputs")),
                        Text("Final Inputs", style="headlineMedium"),
                        ElevatedButton("Go to Calculation", on_click=open_calculation),
                    ],
                ),
            )
        elif page.route == "/calculation":
            page.views.append(
                View(
                    "/calculation",
                    [
                        AppBar(title=Text("VFM計算アプリ Calculation")),
                        Text("Calculation", style="headlineMedium"),
                        ElevatedButton("Go to Initial Inputs", on_click=open_initial_inputs),
                    ],
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

    def open_calculation(e):
        page.go("/calculation")

    def open_initial_inputs(e):
        page.go("/")

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    
flet.app(target=main)
#flet.app(target=main, view=flet.TERMINAL)))