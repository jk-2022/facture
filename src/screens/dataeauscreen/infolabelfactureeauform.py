
import json
from flet import *

from datetime import datetime
import sqlite3
import os

from allpath import AllPath
path=AllPath()
path_data=path.path_data()
DB_PATH=os.path.join(path_data,"eau.db")

from myaction_elect import recuperer_une_facture
from uix.custominputfield import CustomInputField

class InfoLabelFactureEauForm(Container):
    def __init__(self, page: Page, donnees:None, formcontrol):
        super().__init__()
        self.padding = 0
        self.page=page
        self.donnees=donnees
        self.formcontrol=formcontrol

        self.info_cont=Column(
            expand=True,
        )
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
                            [
                                Text(f"Facture Mois de : {self.donnees['date']}")
                            ],alignment=MainAxisAlignment.CENTER
                        ),
                        self.info_cont,
                        ElevatedButton("Modifier",icon=Icons.EDIT, on_click=formcontrol.togle_edit_form)
                    ]
                )
            )
        )
        self.update_info()
    
    def update_info(self):
        donnees=recuperer_une_facture(self.donnees['id'])
        allocation=donnees['allocation']
        allocation=json.loads(allocation)
        self.tranche_soc = allocation["tranche_soc"] or 0
        self.tranche1 = allocation["tranche1"] or 0
        self.tranche2 = allocation["tranche2"] or 0
        allocation= float(self.tranche_soc) + float(self.tranche1) + float(self.tranche2)
            
        text_listes=[Row(
                        [
                            Text(f"Total à payer  : "),
                            Text(f"{donnees['total_prix']}", color=Colors.RED_50)
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN
                    ),
                    Row(
                        [
                            Text(f"Total Kw  : "),
                            Text(f"{donnees['total_kw']}")
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN
                    ),
                    Row(
                        [
                            Text(f'Total allocations : '),
                            Text(f"{allocation}")
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN
                    ),
                     
                     ]

        self.info_cont.controls.clear()
        for text in text_listes:
            self.info_cont.controls.append(text)
        self.page.update()




