import flet as ft

page = ft.Page()


def main(sel_dict=None):
        
        if page.session.store.contains_key("selected_dict"):
            if page.session.store.get("selected_dict") == sel_dict:
                pass
            else:    
                page.session.store.remove("selected_dict")
                page.session.store.set("selected_dict", sel_dict)
        else:
            page.session.store.set("selected_dict", sel_dict)

