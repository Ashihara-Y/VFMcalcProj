import flet as ft
import logging
from Screen1 import Screen1
from Screen2 import Screen2

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main(page: ft.Page):
    page.title = "Flet 2-Screen App"
    page.vertical_alignment = ft.MainAxisAlignment.START
    
    def route_change():
        page.views.clear()
        
        if page.route == "/screen2":
            page.views.append(
                ft.View(
                    route="/screen2",
                    controls=[Screen2()]
                )
            )
        else:
            # Default to Screen 1
            page.views.append(
                ft.View(
                    route="/",
                    controls=[Screen1()]
                )
            )
        page.update()

    async def view_pop(e: ft.ViewPopEvent):
        page.views.pop()
        top_view = page.views[-1]
        await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Initialize at root
    route_change()

#if __name__ == "__main__"
ft.run(main)
