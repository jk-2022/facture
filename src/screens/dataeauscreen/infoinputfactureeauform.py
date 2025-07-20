
import json
from flet import *

from datetime import datetime
import sqlite3
import os

from allpath import AllPath
from uix.custominputnumberfield import CustomInputNumberField
path=AllPath()
path_data=path.path_data()
DB_PATH=os.path.join(path_data,"eau.db")

class InfoInputFactureEauForm(Container):
    def __init__(self, page: Page, donnees:None,formcontrol):
        super().__init__()
        self.padding = 0
        self.page=page
        self.donnees=donnees
        donnees_allocation=self.donnees["allocation"]
        donnees_allocation=json.loads(donnees_allocation)
        # print(self.donnees)
        # print(donnees_allocation)
        self.formcontrol=formcontrol
        self.date = Text(f"Facture Mois de : {donnees['date']}", size=16, weight= FontWeight.BOLD)
        self.total_prix = CustomInputNumberField(title="Total prix",value=donnees['total_prix'])
        self.tranche_soc = CustomInputNumberField(title="Tranche Soscial",value=donnees_allocation['tranche_soc'])
        self.tranche_soc.on_change=lambda e: self.calculate_allocation()
        self.tranche1 = CustomInputNumberField(title="Tranche 1",value=donnees_allocation['tranche1'])
        self.tranche1.on_change=lambda e: self.calculate_allocation()
        self.tranche2 = CustomInputNumberField(title="Tranche 2",value=donnees_allocation['tranche2'])
        self.tranche2.on_change=lambda e: self.calculate_allocation()
        self.allocation = CustomInputNumberField(title="Allocation",read_only=True)
        self.total_kw = CustomInputNumberField(title="Total KW", value=donnees['total_kw'])
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
                            ],alignment=MainAxisAlignment.CENTER
                        ),
                        Row(
                            [
                                IconButton(icon=Icons.CLOSE, on_click=formcontrol.togle_edit_form, icon_color=Colors.RED)
                            ],alignment=MainAxisAlignment.END
                        ) ,
                        Row(
                            controls=[
                                self.total_prix,
                                self.total_kw,
                            ]
                        ),
                        Row(
                            [
                                self.tranche_soc,
                                self.tranche1,
                            ]
                        ),
                        Row(
                            [
                                self.tranche2,
                                self.allocation,
                            ]
                        ),
                        Row(
                            [
                                ElevatedButton("Save",icon=Icons.SAVE, on_click=self.SaveData)
                            ],alignment=MainAxisAlignment.CENTER
                        )             
                    ]
                )
            )
        )
        try:
            self.calculate_allocation()
        except:
            pass

    def calculate_allocation(self):
        tranche_soc = self.tranche_soc.value or 0
        tranche1 = self.tranche1.value or 0
        tranche2 = self.tranche2.value or 0

        allocation = float(tranche_soc) + float(tranche1) + float(tranche2)
        self.allocation.value=f"{allocation}"
        self.allocation.update()

    def recupererDonnees(self):
        date = self.date.value
        total_prix = self.total_prix.value
        total_kw = self.total_kw.value
        tranche_soc = self.tranche_soc.value
        tranche1 = self.tranche1.value
        tranche2 = self.tranche2.value
        return {
            # "date": date,
            "total_prix": total_prix,
            "total_kw": total_kw,
            "allocation": {
                "tranche_soc": tranche_soc,
                "tranche1": tranche1,
                "tranche2": tranche2
            },
            
            }

    def SaveData(self, e):
        donnees = self.recupererDonnees()
        allocation=donnees['allocation']
        allocation=json.dumps(allocation)
        donnees['allocation']=allocation
        donnees['id']=self.donnees["id"] # for update client storage data
        donnees['date']=self.donnees["date"] # for update client storage data
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        try:
            c = conn.cursor()
            c.execute("""
                    UPDATE Facture 
                     SET date = ?, total_prix = ?, allocation = ?, total_kw = ? WHERE id = ?
                    """, (
                    self.donnees["date"], donnees["total_prix"],
                    allocation, donnees["total_kw"], self.donnees["id"]
                    ))
            conn.commit()
            self.page.client_storage.set('facture',donnees)
        except Exception as e:
            print(e)
            return False
        self.formcontrol.facture_info_form.update_info()
        self.formcontrol.togle_edit_form(e=None)
        self.page.update()
