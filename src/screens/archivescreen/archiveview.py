# projets_view.py
from flet import *
import os
from datetime import datetime
from allpath import AllPath
#from androidapi import AndroidApi

path=AllPath()
path_data=path.path_data()

DB_PATH=os.path.join(path_data,"rapport.db")
ARCHIVES_PATH=path.path_generated_docs()

#android_api=AndroidApi()


def get_exported_files():
    files = []
    if not os.path.exists(ARCHIVES_PATH):
        os.makedirs(ARCHIVES_PATH)
        print(files)
        return files

    for file_name in os.listdir(ARCHIVES_PATH):
        file_path = os.path.join(ARCHIVES_PATH, file_name)
        if os.path.isfile(file_path):
            ext = file_name.split(".")[-1].upper()
            created = datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%d/%m/%Y %H:%M")
            files.append({"name": file_name, "type": ext, "date": created})
    return files

def get_icon_for_extension(extension: str):
    icons_map = {
        "PDF": Icons.PICTURE_AS_PDF,
        "DOCX": Icons.DESCRIPTION,
        "CSV": Icons.TABLE_CHART,
        # Ajoute d'autres si besoin
    }
    return icons_map.get(extension, Icons.INSERT_DRIVE_FILE)

class ArchiveView(View):
    def __init__(self,page:Page,route:str="/archive"):
        super().__init__()
        self.padding = 0
        self.page=page
        
        self.archive_list = Column(
            expand=1
        )

        self.controls.append(SafeArea(
            Column(
                controls=[
                    Row(
                        controls=[
                            Row(
                                [
                                IconButton(icon=Icons.ARROW_BACK,on_click=self.page.on_view_pop),
                                Text('Archives')
                                ]
                            )
                        ],
                        alignment=MainAxisAlignment.START
                    ),
                    Divider(),
                    self.archive_list
                        ]
                    ),expand=1
                )
            )
        self.load_archives()
        
    def load_archives(self):
        self.archive_list.controls.clear()
        for file in get_exported_files():
            icon = get_icon_for_extension(file["type"])
            row = ListTile(
                    leading=Icon(icon),
                    title=Text(f"{file['name']}"),
                    subtitle=Text(f"{file['date']}"),
                    trailing=IconButton(icon=Icons.DELETE, tooltip="Supprimer", on_click=lambda e, f=file: self.delete_file(f["name"])),
                    on_click=lambda e, f=file: self.open_file(f))
            self.archive_list.controls.append(row)


    def open_file(self,file):
        try:
            #android_api.ouvrir_fichier(file["name"])
            os.startfile(os.path.join(ARCHIVES_PATH, file["name"]))
        except:
            os.startfile(os.path.join(ARCHIVES_PATH, file["name"]))

    def delete_file(self,file_name):
        os.remove(os.path.join(ARCHIVES_PATH, file_name))
        self.load_archives()
        self.page.update()
