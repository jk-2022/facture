
import json
from flet import *

from datetime import datetime
import sqlite3
import os

from allpath import AllPath
path=AllPath()
path_data=path.path_data()
DB_PATH=os.path.join(path_data,"eau.db")

# import json
from myaction_elect import recuperer_chambres

dates=["Janvier","Fevrier","Mars","Avril","Mai","Juin","Juiellet","Août","Septembre","Octobre","Novembre","Décembre"]

class FactureForm(Container):
    def __init__(self, page: Page, formcontrol):
        super().__init__()
        self.padding = 0
        self.page=page
        self.types=self.page.client_storage.get('types')
        # self.width=450
        self.formcontrol=formcontrol
        dateTime = datetime.now().strftime("%d/%m/%Y")
        self.created_at = Text(f"{dateTime}", height=40)
        self.moi_facture = Dropdown(label="Relévé du mois de :", expand=True, border_color=Colors.WHITE54)
        for date in dates:
            self.moi_facture.options.append(dropdown.Option(date))

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
        allocation={
            'tranche_soc':"",
            'tranche1':"",
            'tranche2':""
        }
        allocation=json.dumps(allocation)
        return {"date":date, "allocation":allocation}

    def SaveData(self, e):
        donnees = self.recupererDonnees()
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        try:
            c = conn.cursor()
            c.execute("""
                        INSERT INTO Facture(date,types,total_prix,allocation,total_kw) VALUES(?,?,?,?,?)
                        """, (donnees["date"], self.types, "0.0", donnees["allocation"],"0.0"))
            dernier_id = c.lastrowid
            donnees_chambre=recuperer_chambres()
            # print(donnees_chambre)
            if donnees_chambre:
                for chambre in donnees_chambre:
                    c.execute("""
                        INSERT INTO Releve(chambre,facture_id,date,valeur) VALUES(?,?,?,?)
                        """, (chambre["num_chambre"], dernier_id, donnees["date"], "0.0"))
            else:
                print("pas de chambres")
                pass
            conn.commit()
        except Exception as e:
            print(e)
            return False
        self.formcontrol.load_factures()
        self.formcontrol.close_dlg(e=None)
