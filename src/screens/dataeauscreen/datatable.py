from flet import *
# des=['id','chambre','date','valeur','num_compteur','created_at']
tb = DataTable(
    columns=[
        DataColumn(Text("Chambre N°",weight="bold", size=12)),
        DataColumn(Text("Mois", weight="bold", size=12)),
        DataColumn(Text("Valeur", weight="bold", size=12)),
        # DataColumn(Text("N° compteur", weight="bold", size=12)),
        DataColumn(Text("Date prel.",weight="bold", size=12)),
    ],
    rows=[]
)

Mytable = Column(
    scroll="auto",
    controls=[
        Row([tb], scroll="always")
    ]
)
