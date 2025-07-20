import json
from flet import *

from genererpdfall import generer_facture_generale_pdf
from genererpdfone import exporter_facture_pdf
from myaction_elect import recuperer_nom_chambres, recuperer_nombre_chambre, recuperer_releve, get_deux_derniers_releves
from .datatablecalc import MytableCalc, tb_calc

class CalculView(View):
    def __init__(self, page:Page,route:str="calcul", **k):
        super().__init__(*k)
        self.page=page
        self.padding=0

        self.info_fact_cnt=Column( )
        self.my_table=Column(
            expand=True,
            scroll=ScrollMode.ALWAYS
        )

        self.facture=self.page.client_storage.get("facture")

        # self.donnee_dict={}
        
        self.controls=[
            SafeArea(
                Column(
                    expand=True,
                    controls=[
                        IconButton(icon=Icons.ARROW_BACK,
                                    on_click= self.page.on_view_pop),
                        Container(
                            padding=10,
                            content=self.info_fact_cnt
                        ),
                        Divider(),
                        self.my_table,
                        Row(
                            [
                                ElevatedButton("Générer Toutes les factures",on_click= self.show_confirm_all_invoice)
                            ],alignment=MainAxisAlignment.CENTER
                        ),
                        Container(height=5)
                    ]
                ),
                expand=True
            )]
        self.update_info()
        
    
    def update_info(self):
        donnees=self.facture
        allocation=donnees['allocation']
        allocation=json.loads(allocation)
        self.tranche_soc = allocation["tranche_soc"] or 0
        self.tranche1 = allocation["tranche1"] or 0
        self.tranche2 = allocation["tranche2"] or 0
        allocation= float(self.tranche_soc) + float(self.tranche1) + float(self.tranche2)
        prix_consommation=float(donnees["total_prix"])-allocation
        facture_id=self.facture["id"]
        releves=recuperer_releve(facture_id)
        
        nbre_total_kw=0
        # print("releves",releves)
        for releve in releves:
            anc, nveau= get_deux_derniers_releves(releve['chambre'])
            if anc== None and nveau==None:
                self.info_fact_cnt.controls.clear()
                self.info_fact_cnt.controls.append(Text(
                    "Toutes les informations requises ne sont pas renseigner pour calculer!\n Veiller les renseigner "
                ))
                return False
            if anc==None:
                print("c'est ici")
                anc=0

            releve["ancien_valeur"]=anc
            releve["nbre_kw"]=f"{float(nveau)-float(anc)}"
            nbre_total_kw+=float(releve["nbre_kw"])

        prix_u_conso=prix_consommation/nbre_total_kw
        nbre_chambre=recuperer_nombre_chambre()
        prix_u_entretien=allocation/float(nbre_chambre)
        
        text_listes=[Row(
                        [
                            Text(f"Total à payer  : "),
                            Text(f"{donnees['total_prix']}", color=Colors.RED_50)
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN
                    ),
                    Row(
                        [
                            Text(f"Total Kw CEET : "),
                            Text(f"{donnees['total_kw']}")
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN
                    ),
                    Row(
                        [
                            Text(f'Total allocations : '),
                            Text(f"{allocation}")
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN
                    ),
                    Row(
                        [
                            Text(f'Prix Consommation : '),
                            Text(f"{prix_consommation}")
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN
                    ),
                    Row(
                        [
                            Text(f'Total Kw maison : '),
                            Text(f"{nbre_total_kw}")
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN
                    ),
                    Row(
                        [
                            Text(f'Nombre de chambre: '),
                            Text(f"{nbre_chambre}")
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN
                    ),
                    Row(
                        [
                            Text(f'Prix U entretien : '),
                            Text(f"{prix_u_entretien}")
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN
                    ),
                    Row(
                        [
                            Text(f'Prix U consommation: '),
                            Text(f"{prix_u_conso}")
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN
                    ),
                     
                     ]
        
        # print(nbre_total_kw)
        # print(nbre_chambre)
        # print(round(prix_u_conso,2))
        # print(round(prix_u_entretien,2))

        self.info_fact_cnt.controls.clear()
        # print("fact",self.facture)
        for text in text_listes:
            self.info_fact_cnt.controls.append(text)

        # print(releves)
        tb_calc.rows=[]
        for releve in releves:
            total_a_payer=(float(releve["nbre_kw"])*float(prix_u_conso))+prix_u_entretien
            releve['total_a_payer']=round(total_a_payer,0)
            nom=recuperer_nom_chambres(releve['chambre'])
            releve['nom']=nom['nom']
            releve['prix_consommation']=prix_consommation
            releve['total_prix']=donnees['total_prix']
            releve['nbre_total_kw']=nbre_total_kw
            releve['nbre_chambre']=nbre_chambre
            releve['allocation']=allocation
            releve['prix_u_entretien']=round(prix_u_entretien,2)
            releve['prix_u_conso']=round(prix_u_conso,2)
            tb_calc.rows.append(
                    DataRow(
                        cells=[
                            DataCell(
                                Row(
                                    [
                                        Text(f"{releve["chambre"]} ({releve["nom"]})"),
                                        TextButton('PDF',icon=Icons.DOWNLOAD,on_click=lambda e, releve=releve:self.show_confirm_one_invoice(releve))
                                    ]
                                )
                            ),
                            DataCell(Text(releve["ancien_valeur"])),
                            DataCell(Text(releve["valeur"])),
                            DataCell(Text(releve["nbre_kw"])),
                            DataCell(Text(f"{round(total_a_payer,0)}",color=Colors.RED_600, weight=FontWeight.BOLD)),
                        ],
                        data=releve,
                        selected=True,
                        # on_select_changed=lambda e, data=don: self.open_ouvrage_detail(data)
                    )
                )
            try:
                tb_calc.update()
            except:
                pass
        self.datas_for_generate_all=releves
        self.my_table.controls.append(MytableCalc)
        self.page.update()
    
    def show_confirm_one_invoice(self,releve):
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("🔴 Confirmation ⚠️ "),
            content=Text(f"Enregistrer la facture de {releve['nom']} du moi {releve['date']}"),
            actions=[
                TextButton("Annuler", on_click=self.close_dlg),
                TextButton("Exporter", on_click = lambda e : self.generer_one_invoice(releve)),
            ],
            actions_alignment= MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.open(self.dlg_modal)
        self.page.update()
    
    def show_confirm_all_invoice(self,e):
        releves=self.datas_for_generate_all
        releve=releves[0]
        self.dlg_modal = AlertDialog(
            modal=True,
            title=Text("🔴 Confirmation ⚠️ "),
            content=Text(f"Enregistrer toutes les factures du moi {releve['date']}"),
            actions=[
                TextButton("Annuler", on_click=self.close_dlg),
                TextButton("Exporter", on_click = lambda e : self.generer_all_invoice(releves)),
            ],
            actions_alignment= MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.open(self.dlg_modal)
        self.page.update()

    def generer_all_invoice(self,e):
        generer_facture_generale_pdf(self.datas_for_generate_all)
        self.page.open(SnackBar(Text(f"✅ PDF généré avec succès ")))
        self.close_dlg(e=None)

    def generer_one_invoice(self, releve):
        exporter_facture_pdf(releve)
        self.page.open(SnackBar(Text(f"✅ PDF généré avec succès ")))
        self.close_dlg(e=None)

    def close_dlg(self,e):
        self.page.close(self.dlg_modal)
        self.page.update()

