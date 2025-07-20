from flet import *
# des=['id','chambre','date','valeur','num_compteur','created_at']
tb_calc = DataTable(
    columns=[
        DataColumn(Text("Chambre N°",weight="bold", size=12)),
        DataColumn(Text("Old val.", weight="bold", size=12)),
        DataColumn(Text("New Val", weight="bold", size=12)),
        DataColumn(Text("total kw", weight="bold", size=12)),
        DataColumn(Text("Total+entretient",weight="bold", size=12)),
    ],
    rows=[]
)

MytableCalc = Column(
    scroll="auto",
    controls=[
        Row([tb_calc], scroll="always")
    ]
)
