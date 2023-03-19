import os
import hashlib
import datetime
from tqdm import tqdm
import send2trash

# Diccionario para almacenar los nombres de archivo duplicados y sus ubicaciones
duplicates = {}

# Recorre la carpeta actual y todas las subcarpetas y cuenta el número total de archivos
total_files = sum([len(files) for root, dirs, files in os.walk(os.getcwd())])

# Itera a través de los archivos y calcula el hash MD5 de cada uno
with tqdm(total=total_files, desc="Calculando hashes de archivos") as pbar:
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            # Obtiene el nombre y la ruta completa del archivo
            file_path = os.path.join(root, file)

            # Abre el archivo en modo binario
            with open(file_path, 'rb') as f:
                # Calcula el hash MD5 del archivo
                file_hash = hashlib.md5(f.read()).hexdigest()

                # Verifica si el hash ya está en el diccionario
                if file_hash in duplicates:
                    duplicates[file_hash].append(file_path)
                else:
                    duplicates[file_hash] = [file_path]

            # Actualiza la barra de progreso
            pbar.update(1)

# Elimina los archivos duplicados más nuevos
with tqdm(total=len(duplicates), desc="Eliminando archivos duplicados") as pbar:
    for file_hash, paths in duplicates.items():
        if len(paths) > 1:
            newest_file_path = None
            newest_modification_time = None
            for path in paths:
                # Obtiene la fecha de modificación del archivo
                modification_time = os.path.getmtime(path)

                # Verifica si este archivo es más nuevo que el anterior
                if newest_modification_time is None or modification_time > newest_modification_time:
                    newest_modification_time = modification_time
                    newest_file_path = path

            # Elimina los archivos duplicados más nuevos
            for path in paths:
                if path != newest_file_path:
                    send2trash.send2trash(path)

        # Actualiza la barra de progreso
        pbar.update(1)

print("Eliminación de archivos duplicados completa.")
print("Presione cualquier tecla para salir...")
input()