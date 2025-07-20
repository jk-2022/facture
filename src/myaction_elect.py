import os
import sqlite3
from allpath import AllPath

path=AllPath().path_data()
path_db=os.path.join(path,"eau.db")

def create_tables():
    conn = sqlite3.connect(path_db, check_same_thread=False)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS Chambre (
            num_chambre TEXT PRIMARY KEY,
            nom TEXT,
            contact TEXT,
            num_compteur TEXT
        )
        """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS Releve (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chambre TEXT,
        facture_id TEXT,
        date TEXT,
        valeur REAL,
        created_at  TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(chambre) REFERENCES Chambre(num_chambre)
        FOREIGN KEY(facture_id) REFERENCES Facture(id)
    )
        """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS Facture (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        types TEXT,
        total_prix REAL,
        allocation REAL,
        total_kw REAL,
        created_at  TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()
    
def recuperer_liste_facture(types):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM Facture WHERE types=?", (types,))
        projets = c.fetchall()
        return projets
    except Exception as e:
        print(e)

def recuperer_chambres():
    conn = sqlite3.connect(path_db, check_same_thread=False)
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM Chambre")
        chambres = c.fetchall()
        if chambres:
            donnees=[]
            for  rel in chambres:
                des=['num_chambre','nom','contact','num_compteur']
                don=dict(zip(des, rel))
                donnees.append(don)
            return donnees
        else:
            return chambres
    except Exception as e:
        print(e)

def recuperer_nom_chambres(num_chambre):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    try:
        c = conn.cursor()
        c.execute("SELECT nom FROM Chambre WHERE num_chambre=?", (num_chambre,)) 
        chambre = c.fetchone()
        if chambre:
            des=['nom']
            don=dict(zip(des, chambre))
            return don
        else:
            return ""
    except Exception as e:
        print(e)

def recuperer_nombre_chambre():
    conn = sqlite3.connect(path_db, check_same_thread=False)
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM Chambre")
        chambres = c.fetchall()
        # print(chambres)
        if chambres:
            return len(chambres)
        else:
            return 0
    except Exception as e:
        print(e)
        
def recuperer_une_facture(facture_id):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    try:
        c = conn.cursor()
        c.execute("""
            SELECT * FROM Facture 
            WHERE id = ?
        """, (facture_id,))
        factures = c.fetchone()
        if factures:
            des=['id','date','types','total_prix','allocation','total_kw','created_at']
            donnee=dict(zip(des, factures)) 
        return donnee
    except Exception as e:
        print(e)

def recuperer_releve(facture_id):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    try:
        c = conn.cursor()
        c.execute("""
            SELECT * FROM Releve 
            WHERE facture_id = ?
        """, (facture_id,))
        releves = c.fetchall()
        if releves:
            donnees=[]
            for  rel in releves:
                des=['id','chambre','facture_id','date','valeur','created_at']
                don=dict(zip(des, rel))
                donnees.append(don)
            return donnees
        else:
            return releves
    
    except Exception as e:
        print(e)


def get_deux_derniers_releves(chambre, facture_id):
    conn = sqlite3.connect(path_db, check_same_thread=False)
    c = conn.cursor()
    c.execute(
        "SELECT date, valeur FROM Releve WHERE chambre = ? AND facture_id = ?ORDER BY date DESC LIMIT 2",
        (chambre,facture_id,)
        )
    resultats = c.fetchall()
    # print(resultats)
    if len(resultats) == 2:
        date_courante, valeur_courante = resultats[0]
        date_precedente, valeur_precedente = resultats[1]
        # consommation = float(valeur_courante) - float(valeur_precedente)
        print(f"✅ Consommation entre {date_precedente} et {date_courante} : kWh")
        return valeur_courante,valeur_precedente

    elif len(resultats) == 1:
        date_courante, valeur_courante = resultats[0]
        print(f"⚠️ Un seul relevé disponible pour {chambre} ({date_courante}), impossible de calculer la consommation.")
        return None, valeur_courante

    else:
        print(f"❌ Aucun relevé trouvé pour la chambre {chambre}.")
        return None, None

