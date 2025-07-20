# projets_view.py
from flet import *
import os
from allpath import AllPath
from myaction_elect import recuperer_liste_facture
from .facturecard import FactureCard
from .factureform import FactureForm

path=AllPath()
path_data=path.path_data()

DB_PATH=os.path.join(path_data,"eau.db")
ARCHIVES_PATH=path.path_generated_docs()


#

class FactureEauView(View):
    def __init__(self,page:Page,route:str="/facture-eau"):
        super().__init__()
        self.padding = 0
        self.page=page
        self.types=self.page.client_storage.get('types')
        self.fact_list_cnt = Column(
            expand=1
        )
        self.floating_action_button = FloatingActionButton(icon=Icons.ADD, on_click=self.show_facture,bgcolor=Colors.BLACK54)

        self.controls.append(SafeArea(
            Column(
                controls=[
                    Container(
                        content=Row(
                                [
                                IconButton(icon=Icons.ARROW_BACK, on_click=self.page.on_view_pop),
                                Text("Liste Relévé facture d'eau ", text_align=TextAlign.CENTER)
                                ]
                                # ,alignment=MainAxisAlignment.CENTER
                            ),
                    ),
                    Divider(),
                    self.fact_list_cnt
                        ]
                    )
                )
            )
        self.load_factures()
        
    def show_facture(self,e):
        facture_content = FactureForm(self.page, self)
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Nouveau Relevé"),
            content=facture_content,
            actions=[
                TextButton("Annuler", on_click=self.close_dlg),
                TextButton("Enregistrer", on_click=facture_content.SaveData),
            ],
            actions_alignment= MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.open(self.dlg_modal)
        self.page.update()
        
    def load_factures(self):
        self.fact_list_cnt.controls.clear()
        factures=recuperer_liste_facture(self.types)
        if factures:
            for facture in factures:
                des=['id','date','types','total_prix','allocation','total_kw','created_at']
                facture=dict(zip(des, facture))
                self.fact_list_cnt.controls.append(
                FactureCard(page=self.page, facture=facture,formcontrol=self)
            )

 
        
    def close_dlg(self, e):
        self.page.close(self.dlg_modal)
        self.page.update()

