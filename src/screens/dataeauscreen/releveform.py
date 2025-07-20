
from flet import *

from datetime import datetime
import sqlite3
import os

from allpath import AllPath
path=AllPath()
path_data=path.path_data()
DB_PATH=os.path.join(path_data,"eau.db")

# import json

from uix.custominputfield import CustomInputField
# from uix.customdropdown import CustomDropDown

class ReleveForm(Container):
    def __init__(self, page: Page, formcontrol):
        super().__init__()
        self.padding = 0
        self.page=page
        self.width=450
        self.formcontrol=formcontrol
        self.facture=self.page.client_storage.get('facture')

        dateTime = datetime.now().strftime("%d/%m/%Y")
        self.date = Text(f"{dateTime}", height=40)
        # des=['id','chambre','date','valeur','num_compteur','created_at']
        self.nom = CustomInputField(title="Nom Locataire", height=40)
        self.contact = CustomInputField(title="Contact", height=40)
        self.num_chambre = CustomInputField(title="N° Chambre", height=40)
        self.num_compteur = CustomInputField(title="N° Compteur", height=40)
        self.valeur = CustomInputField(title="Valeur", height=40)
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
                                self.date
                            ]
                        ),
                        self.nom,
                        self.contact,
                        self.num_chambre,
                        self.num_compteur,
                        self.valeur,
                        
                    ]
                )
            )
        )

    def recupererDonnees(self):
        nom = self.nom.value
        contact = self.contact.value
        num_chambre = self.num_chambre.value
        num_compteur = self.num_compteur.value
        valeur = self.valeur.value
        date = self.date.value
        return {"nom": nom,"contact": contact,"num_chambre": num_chambre,"num_compteur": num_compteur,"valeur": valeur}

    def SaveData(self, e):
        donnees = self.recupererDonnees()
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        try:
            c = conn.cursor()
            c.execute("""
                        INSERT INTO Chambre(num_chambre, nom, contact,num_compteur) VALUES(?,?,?,?)
                        """, (donnees["num_chambre"], donnees["nom"], donnees["contact"], donnees["num_compteur"]))
            
            c.execute("""
                        INSERT INTO Releve(chambre,facture_id,date,valeur) VALUES(?,?,?,?)
                        """, (donnees["num_chambre"], self.facture['id'], self.facture['date'], donnees["valeur"]))
            conn.commit()
        except Exception as e:
            print(e)
            return False
        self.formcontrol.update_info(e=None)
        self.formcontrol.close_dlg(e=None)
