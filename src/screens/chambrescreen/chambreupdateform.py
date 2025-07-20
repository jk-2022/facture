from typing import Any, List, Optional
from flet import *

import sqlite3
import os

from allpath import AllPath
path=AllPath()
path_data=path.path_data()
DB_PATH=os.path.join(path_data,"eau.db")

# import json
from myaction_elect import recuperer_chambres

from uix.custominputfield import CustomInputField

class ChambreUpdateForm(Container):
    def __init__(self, page: Page, chambre, formcontrol):
        super().__init__()
        self.padding = 0
        self.page=page
        self.width=450
        self.chambre=chambre
        self.formcontrol=formcontrol
        # self.date = Text(f"{chambre['create_at']}")
        self.num_chambre = CustomInputField(title="Num chambre", height=40)
        self.num_chambre.value=chambre["num_chambre"]
        self.nom = CustomInputField(title="Nom", height=40)
        self.nom.value=chambre["nom"]
        self.contact = CustomInputField(title="Contact", height=40)
        self.contact.value=chambre["contact"]
        self.num_compteur = CustomInputField(title="Num Compteur", height=40)
        self.num_compteur.value=chambre["num_compteur"]


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
                                self.nom
                            ]
                        ),
                        self.contact,
                        self.num_chambre,
                        self.num_compteur,
                    ]
                )
            )
        )


    def recupererDonnees(self):
        num_chambre = self.num_chambre.value
        num_compteur = self.num_compteur.value
        nom = self.nom.value
        contact = self.contact.value
        return {"nom": nom, "contact": contact, "num_compteur": num_compteur, "num_chambre": num_chambre}
        
    def SaveData(self, e):
        donnees = self.recupererDonnees()
        pid=self.chambre['num_chambre']
        print(pid)
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        try:
            c = conn.cursor()
            c.execute("UPDATE Chambre SET num_chambre=?, nom=?, contact=?, num_compteur=? WHERE num_chambre=?", (donnees["num_chambre"], donnees["nom"],donnees["contact"],donnees["num_compteur"], pid))
            conn.commit()
            # list_chambre=recuperer_chambres()
            # self.page.data['chambres']=list_chambre
        except Exception as e:
            print(e)
            return False
        self.formcontrol.formcontrol.load_chambres()
        self.formcontrol.close_dlg(e=None)
        
    # def save_edit(ev):
    #     new_name = name_input.value.strip()
    #     if new_name:
    #         conn = sqlite3.connect(DB_PATH)
    #         cursor = conn.cursor()
    #         cursor.execute("UPDATE projects SET name=? WHERE id=?", (new_name, pid))
    #         conn.commit()
    #         conn.close()
    #         self.load_projects()


