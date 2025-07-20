
from flet import *


class AcceuilView(View):
    def __init__(self,page:Page,route:str="/",**k):
        super().__init__()
        self.expand=True
        self.page=page
        self.padding=0
        
        bar_cnt=Container(height=60,
                         bgcolor=Colors.BLUE_GREY,
                         
                         content=Row(
                             [
                                IconButton(icon=Icons.MENU, on_click =  self.open_drawer),
                                Text("GESTION DES FACTURES ", text_align=TextAlign.CENTER,
                                     size=20, weight=FontWeight.BOLD),
                                IconButton(icon=Icons.HELP, on_click= "")
                             ],alignment=MainAxisAlignment.SPACE_BETWEEN
                            )
                         )
        
        self.drawer = NavigationDrawer(
        # on_dismiss=handle_dismissal,
        on_change=self.handle_change,
        controls=[
                Container(
                    height=120,
                    content=CircleAvatar(content=Icon(name=Icons.PERSON)),
                    padding=10
                ),
                Divider(thickness=2),
                Column(
                    [
                        Container(
                            content=Column([
                                    ListTile(title=Text("Chambres"),leading=Icon(name=Icons.ARCHIVE),on_click=self.go_chambres),
                                    ListTile(title=Text("A propos"),leading=Icon(name=Icons.INFO), on_click=self.go_apropos),
                                        ]
                            ),
                                ),
                        Divider(thickness=2),
                        Row(
                            [
                                Text("jeankolou19@gmail.com\nTel:90007727")
                            ],alignment=MainAxisAlignment.CENTER,
                        ),
                        Container(
                            content=TextButton('Nous contacter !'),
                        ),
                    ],
                    expand=1,
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    horizontal_alignment=CrossAxisAlignment.END,
                )
            ],
        )
        
        self.controls.append(SafeArea(
            Stack(
                controls=[

                    Image(
                        src="eau2.png",
                        width=page.width,
                        height=page.height,
                        fit=ImageFit.COVER,
                    ),
                    
                    Container(
                        content=Column(
                                    [
                                        ElevatedButton(" 📋  FACTURE D'EAU  ", on_click=self.page_go_eau, elevation=10),
                                        ElevatedButton(" 📁  FACTURE D'ELECTRICITE  ", on_click=self.go_list_elect, elevation=10),
                                    ],
                                    expand=True,
                                    alignment=MainAxisAlignment.CENTER,
                                    spacing=40
                                ),
                            alignment=alignment.center,
                            expand=True,
                            top=0,bottom=0,left=0,right=0
                            ),
                    bar_cnt



                ]
            )
                )
            )
        
    def go_apropos(self,e):
        self.handle_change(e=None)
        self.page.go("/apropos")
    
    def open_drawer(self,e):
        self.page.open(self.drawer)
        
    def handle_change(self,e):
        # print(f"Selected Index changed: {e.control.selected_index}")
        self.page.close(self.drawer)
 
    def page_go_eau(self,e):
        self.page.client_storage.set('types',"eau")
        self.page.go('/facture')
    
    def go_chambres(self,e):
        self.handle_change(e=None)
        self.page.go('/chambres')
    
    def go_list_elect(self,e):
        self.page.client_storage.set('types',"electricite")
        self.page.go('/facture')