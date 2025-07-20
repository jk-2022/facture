import os
from flet import *
import sqlite3

from allpath import AllPath
from screens.chambrescreen.chambreupdateform import ChambreUpdateForm

path=AllPath()
path_data=path.path_data()

DB_PATH=os.path.join(path_data,"eau.db")
ARCHIVES_PATH=path.path_generated_docs()

# import json
from myaction_elect import recuperer_chambres
# from screens.chambrescreen.chambreupdateform import chambreUpdateForm
# from uix.customdropdown import CustomDropDown

class ChambreCard(Card):
    def __init__(self, page: Page, chambre, formcontrol):
        super().__init__()
        # self.expand=True
        self.elevation=1
        self.chambre=chambre
        self.formcontrol=formcontrol
        self.content=Container(
            on_click=lambda e: self.selectchambre(e),
            padding=padding.all(10),
            data=chambre,
            ink=True,
            # expand=True,
            content=Column(
                [
                    Container(
                        content=Column(
                            [
                                Text(f"Numero Chambre : {chambre['num_chambre']}", size=13, italic=True),
                                Text(f"{chambre['nom']}", size=12, width=300),
                                Text(f"{chambre['contact']}", size=12, width=300),
                                Text(f"{chambre['num_compteur']}", size=12, width=300),
                            ],
                        ),
                        ),
                    Row(
                            [
                                IconButton(icon=Icons.EDIT, on_click=self.show_edit_chambre),
                                IconButton(icon=Icons.DELETE, on_click=self.show_delete_chambre),
                            ],
                            alignment=MainAxisAlignment.END,
                        )
                    ]
                ))
        
        
    def selectchambre(self,e):
        self.page.data['chambre']=self.chambre
        print('ok')


    def show_delete_chambre(self,e):
        name=self.chambre["nom"]
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Supprimer chambre"),
            content=Text(f"Voulez-vous supprimer {name} ?"),
            actions=[
                TextButton("Annuler", on_click=self.close_dlg),
                TextButton("Supprimer", on_click=self.del_chambre),
            ],
            actions_alignment= MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.open(self.dlg_modal)
        self.page.update()
        
    def show_edit_chambre(self,e):
        cont=ChambreUpdateForm(page=self.page,chambre=self.chambre,formcontrol=self)
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Modifier chambre"),
            content=cont,
            actions=[
                TextButton("Annuler", on_click=self.close_dlg),
                TextButton("Modifier", on_click=cont.SaveData),
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
        
    def del_chambre(self,e):
        pid=int(self.chambre['num_chambre'])
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Chambre WHERE num_chambre=?", (pid,))
        conn.commit()
        conn.close()
        # news_data= recuperer_chambres()
        # self.page.data['chambres']=news_data
        self.page.close(self.dlg_modal)
        self.formcontrol.load_chambres()
        self.page.update()