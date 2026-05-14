#Importado de librerias
from pathlib import Path
import shutil
from datetime import  date, datetime


class ArchivoProcesado(): #clase que corresponde al archivo con el que ya se trabajó
    def __init__(self, nombre, tamaño, camino):
        self.nombre = nombre
        self.tamaño = tamaño
        self.camino = camino
        
class CarpetaProcesada(): #clase que corresponde a las carpetas con las que ya se trabajó
    def __init__(self, nombre, tamaño, archivo_unico: ArchivoProcesado):
        self.nombre = nombre
        self.tamaño = tamaño
        self.archivo_unico = archivo_unico
        
        
def BuscarMax(carpeta): #busca el archivo mas grande en una carpeta
    peso = 0 
    ArchivoMasGrande = ArchivoProcesado("ninguno", 0, "ninguno")
    MaxSubcarpeta= ArchivoProcesado("ninguno", 0, "ninguno")
    
    for inFile in carpeta.iterdir():
        if inFile.is_file():
            peso = inFile.stat().st_size
            if peso > ArchivoMasGrande.tamaño: #trabaja con la clase ArchivoProcesado()
                ArchivoMasGrande.nombre = inFile.name
                ArchivoMasGrande.tamaño = peso
                ArchivoMasGrande.camino = Path(inFile)
                
        elif not inFile.is_file():
            MaxSubcarpeta = BuscarMax(inFile) #recursividad
            
        if MaxSubcarpeta.tamaño > ArchivoMasGrande.tamaño:
            ArchivoMasGrande = MaxSubcarpeta
            
    return ArchivoMasGrande
        

def LecturaCarpeta(carpeta): #Captura el peso de la carpeta con la capacidad de leer una dentro de la otra. Utilizando la recursividad y no haciendo una sucesiva de If/Elif innecesarios
    peso_carpeta = 0
    for inFile in carpeta.iterdir():
        if inFile.is_file():
            peso_carpeta += inFile.stat().st_size
        elif not inFile.is_file():
            peso_carpeta += LecturaCarpeta(inFile) #recursividad
    return peso_carpeta
    

def OrganizacionTotal(directorio): #Funcion Organización de todos los archivos en la carpeta seleccionada, revisando si el archivo tiene un sufijo, es carpeta o no tiene sufijo
    directorio = Path(directorio)
    contador_Archivos = 0
    acumulador_Archivos = 0
    lista_carpeta = []
    for file in directorio.iterdir():
        sufijo = file.suffix.lower() #Captura el sufijo del archivo

        if not file.is_file():
            peso_unitario = LecturaCarpeta(file)
            continue #Esta linea es importante para la lógica ya que en caso de no tenerla las carpetas ya organizadas se juntaran dentro de otra carpeta y asi sucesivamente hasta que quede una unica carpeta. Aunque realmente puede resultar util, yo prefiero omitirlo

        if not sufijo:
            destino = (directorio / "otros_archivos")
            destino.mkdir(exist_ok=True) #Indica el movimiento que va a realizar el archivo
            peso_unitario = file.stat().st_size

        if sufijo:
            destino = directorio / f"archivos_{sufijo.strip(".")}"
            destino.mkdir(exist_ok=True) #Indica el movimiento que va a realizar el archivo
            peso_unitario = file.stat().st_size

        try: # Realiza el movimiento del archivo con la posibilidad de que si el archivo esta abierto o se este ejecutando en segundo plano, el sistema no crashee y pueda manejar la excepción
            shutil.move(str(file), str(destino))
            contador_Archivos += 1
            acumulador_Archivos += peso_unitario
            peso_unitario = 0
            
        except Exception as e:
            print(f"el archivo {file.name} no se pudo mover")
            continue
        
    cont_carpetas = 0
    ArchivoMax = ArchivoProcesado("ninguno", 0, "ninguno")
    lista_carpeta = []
    
    for file in directorio.iterdir(): 
        if not file.is_file():
            cont_carpetas += 1
            ArchivoMax = BuscarMax(file)
            CarpetaActual = CarpetaProcesada(file.name, LecturaCarpeta(file), ArchivoMax)
            lista_carpeta.append(CarpetaActual)
        
    return contador_Archivos, acumulador_Archivos, lista_carpeta

def Deshacer(directorio):
    directorio = Path(directorio)
    lista_carpeta = []
    archivos_error = []
    cont_archivos = 0
    acumulador_Archivos = 0
    for file in directorio.iterdir():
        if file.is_dir(): #Si es carpeta, es similar al if not file.is_file() pero es mas limpio, en el codigo dejo los dos de forma intencional
            if "archivos" in file.name :
                for inFile in file.iterdir():
                    try: # Realiza el movimiento del archivo con la posibilidad de que si el archivo esta abierto o se este ejecutando en segundo plano, el sistema no crashee y pueda manejar la excepción
                        acumulador_Archivos += inFile.stat().st_size
                        cont_archivos += 1
                        shutil.move(str(inFile), str(directorio))

                    except Exception as e:
                        archivos_error.append(inFile.name)
                        continue
                try:
                    file.rmdir()
                except: 
                    for i in range(len(archivos_error)):
                        print(f"el archivo {archivos_error[i]} no se pudo mover")
                    print(f"No se borrara la carpeta {file.name}")
    
    for file in directorio.iterdir():
        if not file.is_file():
            ArchivoMax = BuscarMax(file)
            CarpetaActual = CarpetaProcesada(file.name, LecturaCarpeta(file), ArchivoMax)
            lista_carpeta.append(CarpetaActual)

    archivos_error = []            
    return cont_archivos, acumulador_Archivos, lista_carpeta
    
def OrganizacionYReporte(directorio):
    contador_Archivos, acumulador_Archivos, lista_carpeta = OrganizacionTotal(directorio)
    Reporte(directorio, contador_Archivos, acumulador_Archivos, lista_carpeta)
    
def DeshacerYReporte(directorio):
    contador_Archivos, acumulador_Archivos, lista_carpeta = Deshacer(directorio)
    Reporte(directorio, contador_Archivos, acumulador_Archivos, lista_carpeta)
    
def Reporte(directorio, contador_Archivos, acumulador_Archivos, lista_carpeta): #Genera un reporte en formato txt
    directorio = Path(directorio)
    tamaño_total = LecturaCarpeta(directorio)
    with open(f"{directorio}\\Reporte {date.today()} {datetime.now().strftime('%Hhrs %Mmin')}.txt", 'w', encoding='UTF-8') as reporte:
       reporte.write(f"REPORTE ACTUALIZACION \t {date.today()} \t {datetime.now().strftime("%H:%M:%S")}")
       reporte.write("\n-------------------------------------------------------------------------------------------------\n")
       reporte.write(f"\nTamaño total de la carpeta {directorio.name}: {tamaño_total/((1024)**2):.2f} mb \nTotal de archivos organizados: {contador_Archivos} \nTamaño total organizado: {acumulador_Archivos/((1024)**2):.2f} mb\n")
       for i in range(len(lista_carpeta)): 
           reporte.write(f"\nCarpeta {lista_carpeta[i].nombre} \n\tPeso total: {lista_carpeta[i].tamaño/((1024)**2):.2f} mb \n\tArchivo Mas Grande: {lista_carpeta[i].archivo_unico.nombre}, Peso: {lista_carpeta[i].archivo_unico.tamaño/((1024)**2):.2f} mb, Enrutamiento:{lista_carpeta[i].archivo_unico.camino}\n")    
                