import os
import csv

def guardar_directorios_y_archivos_csv(ruta=None, nombre_csv="directorios_y_archivos.csv"):
    """
    Lista los directorios dentro de una ruta dada y los archivos dentro de cada directorio,
    luego los guarda en un archivo CSV con una estructura de columnas dinámicas.
    
    :param ruta: Ruta donde se listarán los directorios y archivos (opcional, por defecto el directorio actual).
    :param nombre_csv: Nombre del archivo CSV donde se guardará la lista.
    """
    if ruta is None:
        ruta = os.getcwd()  # Obtener el directorio actual

    try:
        # Obtener la lista de directorios
        directorios = [d for d in os.listdir(ruta) if os.path.isdir(os.path.join(ruta, d))]

        # Crear una lista para almacenar los datos
        datos = []

        for directorio in directorios:
            dir_path = os.path.join(ruta, directorio)
            archivos = os.listdir(dir_path)  # Listar archivos en el directorio
            
            if archivos:
                datos.append([directorio] + archivos)  # Guardar el directorio y los archivos en la fila
            else:
                datos.append([directorio, "Sin archivos"])  # Si está vacío, poner "Sin archivos"

        # Determinar el número máximo de archivos en un directorio para ajustar las columnas
        max_archivos = max(len(fila) for fila in datos)

        # Escribir en el archivo CSV
        with open(nombre_csv, mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            
            # Crear encabezados dinámicos
            encabezados = ["Directorio"] + [f"Archivo{i+1}" for i in range(max_archivos - 1)]
            escritor.writerow(encabezados)  # Escribir la primera fila con los encabezados
            
            # Escribir los datos
            for fila in datos:
                escritor.writerow(fila + [""] * (max_archivos - len(fila)))  # Completar con espacios vacíos si faltan columnas

        print(f"Archivo CSV '{nombre_csv}' creado con éxito en {os.getcwd()}.")

    except FileNotFoundError:
        print("Error: La ruta especificada no existe.")
    except PermissionError:
        print("Error: No tienes permisos para acceder a esta ruta.")

# Uso de la función
guardar_directorios_y_archivos_csv()
