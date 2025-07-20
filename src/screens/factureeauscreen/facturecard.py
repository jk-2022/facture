import os
from flet import *
import sqlite3

from allpath import AllPath
from screens.factureeauscreen.factureupdateform import FactureUpdateForm

path=AllPath()
path_data=path.path_data()

DB_PATH=os.path.join(path_data,"eau.db")
ARCHIVES_PATH=path.path_generated_docs()


class FactureCard(Card):
    def __init__(self, page: Page, facture, formcontrol):
        super().__init__()
        self.expand=True
        self.page=page
        self.elevation=10
        self.facture=facture
        self.formcontrol=formcontrol
        self.content=Container(
            on_click=lambda e: self.selectfacture(e),
            padding=padding.all(10),
            data=facture,
            ink=True,
            expand=True,
            content=Column(
                [
                    Container(
                        content=Column(
                            [
                                Text(f"{facture['created_at']}", size=11, italic=True),
                                Container(
                                    expand=True,
                                    content=Text(f"{facture['date']}", size=13, width=300)
                                    ),
                            ],
                        ),
                        ),
                    Row(
                            [
                                IconButton(icon=Icons.EDIT, on_click=self.show_edit_facture),
                                IconButton(icon=Icons.DELETE, on_click=self.show_delete_facture),
                            ],
                            alignment=MainAxisAlignment.END,
                        )
                    ]
                ))
        
        
    def selectfacture(self,e):
        self.page.client_storage.set('facture',self.facture)
        # self.page.client_storage.set('facture_id',self.facture['id'])
        self.page.go("/data")


    def show_delete_facture(self,e):
        date=self.facture["date"]
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Confirmation"),
            content=Container(
                padding=10,
                content=Row(
                        [
                            Text(f"Voulez-vous supprimer la facture du moi {date} ?", size=11)
                        ]
                            )
                    ),
            actions=[
                TextButton("Annuler", on_click=self.close_dlg),
                TextButton("Supprimer",icon=Icons.DELETE, icon_color=Colors.RED, on_click=self.del_facture),
            ],
            actions_alignment= MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.open(self.dlg_modal)
        self.page.update()
        
    def show_edit_facture(self,e):
        cont=FactureUpdateForm(page=self.page,facture=self.facture,formcontrol=self)
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Modifier la période"),
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
        
    def del_facture(self,e):
        pid=int(self.facture['id'])
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Facture WHERE id=?", (pid,))
        conn.commit()
        conn.close()
        self.formcontrol.load_factures()
        self.page.close(self.dlg_modal)
        self.page.update()