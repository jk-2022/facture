 # main.py
from flet import *
from screens.screens import *
from myaction_elect import create_tables

def main(page: Page):
    page.title = "Gestion des projets"
    page.scroll = True
    page.window.width=450
    page.theme_mode = ThemeMode.DARK
    theme = Theme()
    theme.page_transitions.android = PageTransitionsTheme.android
    create_tables()
    # page.data= fetch_data()
    
    def route_change(route):
        if page.route == "/":
            page.views.append(AcceuilView(page))
        elif page.route == "/facture":
            page.views.append(FactureEauView(page))
        elif page.route == "/data":
            page.views.append(DataEauView(page))
        elif page.route == "/calcul":
            page.views.append(CalculView(page))
        elif page.route == "/chambres":
            page.views.append(ChambresView(page))

        page.update()

    def on_view_pop(e: ViewPopEvent):
        # 🔙 Cette fonction est appelée quand l'utilisateur appuie sur le bouton retour Android
        # print(page.views)
        if len(page.views) > 1:
            page.views.pop()
            page.go(page.views[-1].route)
        else:
            # Si on est sur la première page, quitter l'app
            page.window.close()

    
    page.views.append(AcceuilView(page))
    page.on_route_change = lambda e: route_change(page)
    page.on_view_pop = lambda e: on_view_pop(page)
    page.update()

app(main)
