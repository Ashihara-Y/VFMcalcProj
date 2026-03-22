import flet as ft
import logging

logger = logging.getLogger(__name__)

@ft.control
class Screen1(ft.Column):
    def init(self):
        #super().__init__()
        self.title  = "Screen 1"
        self.width  = 600
        self.height = 400
        #self.bgcolor = ft.colors.BLUE_100
        
        # 5 Slider instances with range 0-9
        self.slider_a = ft.Slider(min=0, max=9, divisions=9, label="A: {value}")
        self.slider_b = ft.Slider(min=0, max=9, divisions=9, label="B: {value}")
        self.slider_c = ft.Slider(min=0, max=9, divisions=9, label="C: {value}")
        self.slider_d = ft.Slider(min=0, max=9, divisions=9, label="D: {value}")
        self.slider_e = ft.Slider(min=0, max=9, divisions=9, label="E: {value}")

    #def build(self):
        self.controls=[
            ft.Text("Screen 1", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Select values for A, B, C, D, E (0-9)"),
            ft.Row([ft.Text("A:"), self.slider_a]),
            ft.Row([ft.Text("B:"), self.slider_b]),
            ft.Row([ft.Text("C:"), self.slider_c]),
            ft.Row([ft.Text("D:"), self.slider_d]),
            ft.Row([ft.Text("E:"), self.slider_e]),
            ft.Button(content="Save & Next", on_click=self.submit)
        ]

    async def submit(self, e):
        # Retrieve values, default to 0.0 if None
        val_a = self.slider_a.value or 0.0
        val_b = self.slider_b.value or 0.0
        val_c = self.slider_c.value or 0.0
        val_d = self.slider_d.value or 0.0
        val_e = self.slider_e.value or 0.0
        
        # 辞書のリストに格納 (List of Dictionary)
        data = [{
            "A": val_a,
            "B": val_b,
            "C": val_c,
            "D": val_d,
            "E": val_e,
        }]
        
        # Serialize/store into page.session
        self.page.session.store.set("slider_values", data)
        await self.page.push_route("/screen2")
