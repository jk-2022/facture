import os
import sqlite3
from allpath import AllPath
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

path=AllPath()
path_data=path.path_data()

DB_PATH=os.path.join(path_data,"eau.db")
ARCHIVES_PATH=path.path_generated_docs()

class GenererOneInvoice(FPDF):
    def __init__(self,title:str=""):
        super().__init__()
        self.title=title

    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, f"{self.title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    def add_ligne(self, libelle, valeur):
        self.set_font("Helvetica", "", 12)
        self.cell(100, 7, f"{libelle} :", border=0)
        self.cell(0, 7, f"{valeur}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, border=0)

def exporter_facture_pdf(data_dict):
    date=data_dict['created_at'].split("-")
    annee=date[0]
    title=f"Facture du moi de : {data_dict["date"]} {annee}"
    pdf = GenererOneInvoice(title=title)
    pdf.add_page(format=(148, 130))
    # pdf.add_page()

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, f"Chambre : {data_dict['chambre']} ({data_dict['nom']})", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    # pdf.cell(0, 10, f"Mois : {mois}", ln=True)

    pdf.ln(5)

    # Contenu
    libelles={"Prix Facture Total du mois":data_dict['total_prix'],"Tranches socials et entretien":data_dict['allocation'], "Prix consommation sans les tranches":data_dict['prix_consommation'], "Nombre d'occupants":data_dict['nbre_chambre'], "Prix entretien par occuppant":data_dict['prix_u_entretien'], "Total en Kw de tous les occuppants":data_dict['nbre_total_kw'], "Prix Unitaire d'un KW":data_dict['prix_u_conso'], "Ancien Relevé":data_dict['ancien_valeur'], "Nouveau Relevé":data_dict['valeur'], "Nombre KW":data_dict['nbre_kw'], "Prix à Payer":data_dict['total_a_payer']}

    for lib, valeur in libelles.items():
        if isinstance(valeur, float):
            valeur = f"{valeur:.2f} FCFA" if "Prix" in lib or "Tranches" in lib else f"{valeur:.2f}"
        pdf.add_ligne(lib, valeur)

    # Nom du fichier
    fichier = f"{ARCHIVES_PATH}/Chambre_{data_dict["chambre"]}_Facture_{data_dict["date"]}.pdf"
    pdf.output(fichier)
    return fichier
