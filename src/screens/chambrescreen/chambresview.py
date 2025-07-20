# projets_view.py
from flet import *
import os
from datetime import datetime
from allpath import AllPath
from myaction_elect import recuperer_chambres
from screens.chambrescreen.chambrecard import ChambreCard
from screens.chambrescreen.chambreform import ChambreForm

path=AllPath()
path_data=path.path_data()

DB_PATH=os.path.join(path_data,"rapport.db")
ARCHIVES_PATH=path.path_generated_docs()

class ChambresView(View):
    def __init__(self,page:Page,route:str="/chambres"):
        super().__init__()
        self.padding = 0
        self.page=page
        
        self.floating_action_button = FloatingActionButton(icon=Icons.ADD, on_click=self.add_chambre,bgcolor=Colors.BLACK12)
        self.chambres_list = Column(
            expand=1,
            scroll=ScrollMode.ALWAYS
        )

        self.controls.append(SafeArea(
            Column(
                controls=[
                    Row(
                        controls=[
                            Row(
                                [
                                IconButton(icon=Icons.ARROW_BACK,on_click=self.page.on_view_pop),
                                Text('Chambres')
                                ]
                            )
                        ],
                        alignment=MainAxisAlignment.START
                    ),
                    Divider(),
                    self.chambres_list
                        ]
                    ),expand=1
                )
            )
        self.load_chambres()
        
    def load_chambres(self):
        self.chambres_list.controls.clear()
        chambres=recuperer_chambres()
        for chambre in chambres:
            self.chambres_list.controls.append(
                ChambreCard(page=self.page,chambre=chambre,formcontrol=self)
            )
            # print(chambre)
        # self.chambres_list.controls.clear()
    
    def add_chambre(self,e):
        cont=ChambreForm(page=self.page,formcontrol=self)
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Ajouter chambre"),
            content=cont,
            actions=[
                TextButton("Annuler", on_click=self.close_dlg),
                TextButton("Enregistré", on_click=cont.SaveData),
            ],
            actions_alignment= MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.open(self.dlg_modal)
        self.page.update()

    def close_dlg(self,e):
        self.page.close(self.dlg_modal)
        self.page.update()

