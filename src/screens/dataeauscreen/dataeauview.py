
# projets_view.py
from flet import *
import os

from allpath import AllPath
from myaction_elect import recuperer_releve
from screens.dataeauscreen.valeurform import ValeurForm
from .datatable import Mytable, tb
from screens.dataeauscreen.releveform import ReleveForm

from .infoinputfactureeauform import InfoInputFactureEauForm 
from .infolabelfactureeauform import InfoLabelFactureEauForm


path=AllPath()
path_data=path.path_data()

DB_PATH=os.path.join(path_data,"eau.db")


class DataEauView(View):
    def __init__(self,page:Page, route:str="/data"):
        super().__init__()
        self.page=page
        self.facture=self.page.client_storage.get('facture')
        self.types=self.page.client_storage.get('types')
        
        self.facture_form= InfoInputFactureEauForm(self.page, donnees=self.facture, formcontrol=self)
        self.facture_info_form=InfoLabelFactureEauForm(self.page, donnees=self.facture, formcontrol=self)
        self.facture_form.visible=False
        # self.releve_info_form=InfoReleveEauForm(self.page, donnees=self.facture, formcontrol=self)
        self.my_table=Column(

        )

        self.controls.append(
            SafeArea(
                Column(
                    controls=[
                        Row(
                            [
                                IconButton(icon=Icons.ARROW_BACK, on_click=self.page.on_view_pop)
                            ]
                        ),
                        Divider(color=Colors.BLUE_50),
                        Column(
                            controls=[
                                self.facture_info_form,
                                self.facture_form,
                                # self.releve_info_form,
                                self.my_table,
                                Row(
                                    [
                                    ElevatedButton("Ajouter",icon=Icons.ADD, on_click=self.show_add_room),
                                    ElevatedButton("Modifier",icon=Icons.EDIT, on_click=self.show_update_valeurs),
                                    ElevatedButton("les Factures", on_click=self.go_calcul_page),
                                    ],alignment=MainAxisAlignment.SPACE_EVENLY
                                )
                                
                            ]
                        ),
                        Column(
                            controls=[
                            ],expand=True, spacing=10
                        ),
                        Divider(color=Colors.BLUE_50),
                    ],scroll=ScrollMode.ALWAYS
                ),expand=True
            )
        )
        self.update_info(e=None)
    
    def togle_edit_form(self,e):
        if self.facture_info_form.visible ==False:
            self.facture_info_form.visible =True
            self.facture_form.visible =False
        else: 
            self.facture_info_form.visible = False
            self.facture_form.visible = True

        self.facture_form.update()
        self.facture_info_form.update()

    def togle_edit_form_rel(self,e):
        pass

    def show_update_valeurs(self,e):
        projet_content = ValeurForm(self.page, formcontrol=self)
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Modifier les valeurs"),
            content=projet_content,
            actions=[
                TextButton("Annuler", on_click=self.close_dlg),
                TextButton("Enregistrer", on_click=projet_content.SaveData),
            ],
            actions_alignment= MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.open(self.dlg_modal)
        self.page.update()
        
    def show_add_room(self,e):
        projet_content = ReleveForm(self.page, formcontrol=self)
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("Nouveau"),
            content=projet_content,
            actions=[
                TextButton("Annuler", on_click=self.close_dlg),
                TextButton("Enregistrer", on_click=projet_content.SaveData),
            ],
            actions_alignment= MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
            content_padding=0
        )
        self.page.open(self.dlg_modal)
        self.page.update()

    def update_info(self,e):
        donnees=recuperer_releve(self.facture['id'])
        if donnees==[]:
            return
        # print(donnees)
        tb.rows = []
        for don in donnees:
            tb.rows.append(
                    DataRow(
                        cells=[
                            DataCell(
                                Row(
                                    [
                                        Text(don["chambre"]),
                                        # TextButton('voir',icon=Icons.FORMAT_SIZE)
                                    ]
                                )
                            ),
                            DataCell(Text(self.facture["date"])),
                            DataCell(Text(don["valeur"])),
                            # DataCell(Text(don["num_compteur"])),
                            DataCell(Text(don["created_at"])),
                        ],
                        data=don,
                        selected=True,
                        # on_select_changed=lambda e, data=don: self.open_ouvrage_detail(data)
                    )
                )
        try:
            tb.update()
        except:
            pass
        self.my_table.controls.append(Mytable)
        # self.page.update()

    def go_calcul_page(self,e):
        self.page.go("/calcul")
    
    def close_dlg(self, e):
        self.page.close(self.dlg_modal)
        self.page.update()