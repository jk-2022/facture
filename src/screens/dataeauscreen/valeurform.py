
from flet import *

# from datetime import datetime
import sqlite3
import os

from allpath import AllPath
path=AllPath()
path_data=path.path_data()
DB_PATH=os.path.join(path_data,"eau.db")

# import json

from myaction_elect import recuperer_releve
from uix.custominputfield import CustomInputField
# from uix.customdropdown import CustomDropDown

class ValeurForm(Container):
    def __init__(self, page: Page, formcontrol):
        super().__init__()
        self.padding = 0
        self.page=page
        self.width=450
        self.formcontrol=formcontrol
        self.facture=self.page.client_storage.get('facture')
        # self.facture_id=self.facture['date']
        self.facture_id=self.facture['id']

        self.valeur_field_dict={}
        
        self.contenu_relev_cnt=Column(
            scroll=ScrollMode.ALWAYS,
            expand=True
        )

        self.valeur = CustomInputField(title="Valeur", height=40)
        self.content = Card(
            elevation=10,
            expand=True,
            content=Container(
                expand=True,
                padding=10,
                content=self.contenu_relev_cnt
            )
        )
    
        releves=recuperer_releve(self.facture_id)
        self.contenu_relev_cnt.controls.clear()
        for releve in releves:
            field=CustomInputField(title=f"Chambre N° {releve['chambre']}", value=releve['valeur'])
            self.valeur_field_dict[releve['chambre']]=field
            self.contenu_relev_cnt.controls.append(field)


    def SaveData(self, e):
        donnees = self.valeur_field_dict
        if not donnees:
            return
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)

        try:
            c = conn.cursor()
            for key, val in donnees.items():
                c.execute("""
                            UPDATE Releve SET valeur=? WHERE  chambre=? AND facture_id =? """, (val.value, key, self.facture_id))
            conn.commit()
        except Exception as e:
            print(e)
            return False
        self.formcontrol.update_info(e=None)
        self.formcontrol.close_dlg(e=None)
