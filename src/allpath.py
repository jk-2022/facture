
import os

def is_android():
    # Android : chemin typique d’un environnement Android
    return os.path.exists("/storage/emulated/0")


class AllPath:
    def path_data(self):
        if is_android():
            dir_path = os.getenv("FLET_APP_STORAGE_DATA")
        else:
            dir_path = os.getenv("FLET_APP_STORAGE_DATA")
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return dir_path  

    def path_generated_docs(self):
        if is_android():
            dir_path = dir_path = "/storage/emulated/0/Documents/factures"
        else:
            dir_path = os.getcwd()
        file_path = os.path.join(dir_path, "generated_docs")
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        return file_path        

