import flet as ft
import logging

logger = logging.getLogger(__name__)

@ft.control
class Screen2(ft.Column):
    def init(self):
        #super().__init__()
        #self.page = page
        
        # 5 Slider instances with range 0-9
        self.slider_aa = ft.Slider(min=0, max=9, divisions=9, label="AA: {value}")
        self.slider_bb = ft.Slider(min=0, max=9, divisions=9, label="BB: {value}")
        self.slider_cc = ft.Slider(min=0, max=9, divisions=9, label="CC: {value}")
        self.slider_dd = ft.Slider(min=0, max=9, divisions=9, label="DD: {value}")
        self.slider_ee = ft.Slider(min=0, max=9, divisions=9, label="EE: {value}")
        
        self.result_text = ft.Text("Result will be displayed here.", size=20)
    #def build(self):
        self.controls=[
            ft.Text("Screen 2", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Select values for AA, BB, CC, DD, EE (0-9)"),
            ft.Row([ft.Text("AA:"), self.slider_aa]),
            ft.Row([ft.Text("BB:"), self.slider_bb]),
            ft.Row([ft.Text("CC:"), self.slider_cc]),
            ft.Row([ft.Text("DD:"), self.slider_dd]),
            ft.Row([ft.Text("EE:"), self.slider_ee]),
            ft.Button(content="Calculate Result", on_click=self.calculate),
            self.result_text,
            ft.Button(content="Back to Screen 1", on_click=self.return_root)
        ]

    async def return_root(self, e):
        await self.page.push_route("/")

    def calculate(self, e):
        # Retrieve from page.session
        data_list = self.page.session.store.get("slider_values")
        if not data_list or len(data_list) == 0:
            self.result_text.value = "Error: No data in SessionStorage from Screen 1."
            self.update()
            return
            
        data = data_list[0]
        
        # Addition step
        sum_a = data.get("A", 0) + (self.slider_aa.value or 0.0)
        sum_b = data.get("B", 0) + (self.slider_bb.value or 0.0)
        sum_c = data.get("C", 0) + (self.slider_cc.value or 0.0)
        sum_d = data.get("D", 0) + (self.slider_dd.value or 0.0)
        sum_e = data.get("E", 0) + (self.slider_ee.value or 0.0)
        
        # Multiplication step
        product = sum_a * sum_b * sum_c * sum_d * sum_e
        
        # Display
        self.result_text.value = f"Calculated Result: {product}"
        self.update()

