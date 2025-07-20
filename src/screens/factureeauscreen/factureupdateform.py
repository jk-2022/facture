
from flet import *

import sqlite3
import os

from allpath import AllPath
path=AllPath()
path_data=path.path_data()
DB_PATH=os.path.join(path_data,"eau.db")

# import json
from myaction_elect import recuperer_liste_facture

from uix.custominputfield import CustomInputField

dates=["Janvier","Fevrier","Mars","Avril","Mai","Juin","Juiellet","Août","Septembre","Octobre","Novembre","Décembre"]

class FactureUpdateForm(Container):
    def __init__(self, page: Page, facture, formcontrol):
        super().__init__()
        self.padding = 0
        self.page=page
        self.width=450
        self.facture=facture
        self.formcontrol=formcontrol
        self.created_at = Text(f"{facture['created_at']}")
        self.moi_facture = Dropdown(label="Relévé du mois de :", expand=True, border_color=Colors.WHITE54)
        for date in dates:
            self.moi_facture.options.append(dropdown.Option(date))
        self.moi_facture.value=facture["date"]


        self.content = Card(
            elevation=20,
            content=Container(
                padding=15,
                expand=True,
                content=Column(
                    scroll="always",
                    spacing=10,
                    controls=[
                        Row(
                            controls=[
                                self.created_at
                            ]
                        ),
                        Row(
                            controls=[
                                self.moi_facture,
                            ]
                        ),
                    ]
                )
            )
        )


    def recupererDonnees(self):
        date = self.moi_facture.value
        created_at = self.created_at.value
        return {"date": date, "created_at": created_at}
        
    def SaveData(self, e):
        donnees = self.recupererDonnees()
        pid=self.facture['id']
        # print(donnees)
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        try:
            c = conn.cursor()
            c.execute("UPDATE Facture SET date=? WHERE id=?", (donnees["date"], pid))
            conn.commit()
            list_facture=recuperer_liste_facture()
            self.page.client_storage.set("factures",list_facture)
        except Exception as e:
            print(e)
            return False
        self.formcontrol.formcontrol.load_factures()
        self.formcontrol.close_dlg(e=None)
