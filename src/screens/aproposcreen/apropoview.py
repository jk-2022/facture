from flet import *

class ApropoView(View):
    def __init__(self, page:Page,route="/apropos", **k):
        super().__init__(*k)
        self.page=page
        self.route=route
        bac_cnt=Container(height=40,
                          content=Row(
                              controls=[
                                  IconButton(icon=Icons.ARROW_BACK, data="/",
                                             on_click= self.page.on_view_pop),
                                  Text(" ")
                              ]
                          )
                          )
        with open("apropos.txt","r",encoding='utf-8') as f:
            text=f.read()

        apropo_cont=ListView(
            expand=True,
            controls=[
                Text(text)
            ]
        )
        self.controls=[
            SafeArea(
                Column(
                    expand=True,
                    controls=[
                        bac_cnt,
                        apropo_cont,
                    ]
                ),
                expand=True
            )]
        
    def go_back_to_products(self,e):
        self.page.go('/acceuil')
