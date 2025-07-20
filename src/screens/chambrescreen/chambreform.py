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

class ChambreForm(Container):
    def __init__(self, page: Page, formcontrol):
        super().__init__()
        self.padding = 0
        self.page=page
        self.width=450
        self.formcontrol=formcontrol
        self.num_chambre = CustomInputField(title="Num chambre", height=40)
        self.nom = CustomInputField(title="Nom", height=40)
        self.contact = CustomInputField(title="Contact", height=40)
        self.num_compteur = CustomInputField(title="Num Compteur", height=40)


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
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        try:
            c = conn.cursor()
            c.execute("INSERT INTO Chambre(num_chambre, nom, contact, num_compteur) VALUES(?,?,?,?)", (donnees["num_chambre"], donnees["nom"],donnees["contact"],donnees["num_compteur"]))
            conn.commit()
        except Exception as e:
            print(e)
            return False
        self.formcontrol.load_chambres()
        self.formcontrol.close_dlg(e=None)

