
import gestor

from pathlib import Path
import shutil
from datetime import  date, datetime
            
print("Proyecto Organización")


#definición de variables
directorio = Path("D:\\Usuario\\descargas")
sufijo = ""
contador_Archivos = 0
acumulador_Archivos = 0
lista_carpeta = []
exit = 0

#definimos la carpeta que se va a organizar
directorio = input("ingrese la ruta de la carpeta con la que trabajar(0 para Default/exit para salir):").strip('"').strip("'")
print("\n")

while exit == 0:
    if directorio != "exit":
        if directorio == "0":
                directorio = Path("D:\\Usuario\\descargas")
                
        if Path(directorio).exists() and Path(directorio).is_dir():
                directorio = Path(directorio)
                print(f"Ruta validada: {directorio}")
                exit = 1

        while exit == 0 and directorio != "exit" and not Path(directorio).exists(): #corroboramos la existencia de la ruta
            directorio = input("ingrese otra ruta: ")
            if directorio == "0":
                directorio = Path("D:\\Usuario\\descargas")
            elif Path(directorio).exists() and Path(directorio).is_dir():
                directorio = Path(directorio)
                print(f"Ruta validada: {directorio}")
                exit = 1
    
    if directorio == "exit":
        exit = 1

exit = 0

while exit == 0: #Empieza el bucle que le permite el usuario ejecutar el programa
    eleccion = input(f"Seleccione tarea a realizar (Organizar/Deshacer/OrganizarIA/Cerrar): ").lower()

    if eleccion == "organizar":
        gestor.OrganizacionYReporte(directorio) 
    elif eleccion == "deshacer":
        gestor.Deshacer(directorio)
    elif eleccion == "organizaria": #Actualizacion mas adelante del proyecto donde la idea es que la IA guie la organizacion por "contexto" del archivo
        print("En desarrollo")
    elif eleccion == "cerrar": 
        print("Cerrando...")
        exit = 1
    else: 
        print("ERROR al elegir la accion")