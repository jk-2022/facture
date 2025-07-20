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

class FactureGeneralePDF(FPDF):
    def __init__(self, title:str=''):
        super().__init__()
        self.title=title 

    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, self.title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.ln(5)

    def add_ligne(self, libelle, valeur):
        self.set_font("Helvetica", "", 11)
        # self.cell(80, 8, f"{libelle} :", new_x=XPos.RIGHT, new_y=YPos.TOP, align="C")
        # self.cell(0, 8, str(valeur), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

        largeur_total = 120  # bloc centré
        largeur_libelle = 70
        largeur_valeur = 50
        marge_gauche = (210 - largeur_total) / 2  # centrer le bloc sur A4

        self.set_x(marge_gauche)
        self.set_font("Helvetica", "", 11)
        self.cell(largeur_libelle, 8, f"{libelle} :", border=0, align="L")
        self.cell(largeur_valeur, 8, str(valeur), border=0, align="R")
        self.ln()

    def add_table_header(self):
        self.set_font("Helvetica", "B", 11)
        self.set_x((210 - 200) / 2) 
        for header in ["N° Chambre", "Ancien relevé", "Nouveau relevé", "Nbre kWh", "Prix a Payer (FCFA)"]:
            self.cell(40, 8, header, border=1, align="C")
        self.ln()

    def add_table_row(self, chambre, ancien, nouveau, kw, prix):
        self.set_font("Helvetica", "", 10)
        self.set_x((210 - 200) / 2) 
        self.cell(40, 8, chambre, border=1)
        self.cell(40, 8, f"{ancien:.2f}", border=1)
        self.cell(40, 8, f"{nouveau:.2f}", border=1)
        self.cell(40, 8, f"{kw}", border=1)
        self.cell(40, 8, f"{prix:.2f}", border=1)
        self.ln()

def generer_facture_generale_pdf(releves):
    data_dict=releves[0]

    pdf = FactureGeneralePDF(title=f"Facture Générale du Moi {data_dict["date"]}")
    pdf.add_page(format=(210, 170))

    # Partie 1 : résumé
    pdf.set_font("Helvetica", "", 11)
    pdf.add_ligne("Facture Total du mois", f"{data_dict['total_prix']:.2f} FCFA")
    pdf.add_ligne("Tranches socials et entretien", f"{data_dict['allocation']:.2f} FCFA")
    pdf.add_ligne("Prix consommation sans les tranches", f"{data_dict['prix_consommation']:.2f} FCFA")
    pdf.add_ligne("Nombre d'occupants", data_dict['nbre_chambre'])
    pdf.add_ligne("Prix entretien par occuppant", f"{data_dict['prix_u_entretien']:.2f} FCFA")
    pdf.add_ligne("Total en Kw de tous les occup. (calculé)", f"{data_dict['nbre_total_kw']:.2f}")
    pdf.add_ligne("Prix Unitaire d'un KW", f"{data_dict['prix_u_conso']:.2f} FCFA")
    # pdf.add_ligne("Nombre Kw relevé", f"{total_conso:.2f}")
    pdf.ln(5)

    # Partie 2 : tableau
    pdf.add_table_header()
    for ligne in releves:
        pdf.add_table_row(
            f"{ligne["chambre"]} ({ligne['nom']})", ligne["ancien_valeur"], ligne["valeur"],
            ligne["nbre_kw"], ligne["total_a_payer"]
        )

    # Export
    nom_fichier = os.path.join(ARCHIVES_PATH, f"Facture_Generale_{data_dict['date']}.pdf")
    pdf.output(nom_fichier)
    return nom_fichier
