import event_array as ea
import flet as ft

sig_array = ea.e_data_array

def slider_changed(e):
    #sig_array = ea.e_data_array
    new_value = {"{e.control.name}": e.control.value}
    sig_array.append(new_value)
    ft.page.pubsub.send_all("slider_changed", new_value)
    new_value = None
    ft.page.update()
    
