from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from datetime import datetime
from os import path, getcwd
import csv

RUTA_BD = "db"
PLATOS = "bd.csv"

class Comida:
    def __init__(self, nombre:str, perfil_sabor:str, region:str,
                 tiempo_dia:str, aperitivo:str, tipo_comida:str,
                 calorias:str, proteinas:int, grasas:str, gluten:int,
                 vegano:int, lactosa:int):
        self.nombre = nombre.strip()
        self.perfil_sabor = [i.strip() for i in perfil_sabor.split("-")]
        if region != "":
            self.region = region.strip()
        else: self.region = []
        if tiempo_dia != "":
            self.tiempo_dia = [i.strip() for i in tiempo_dia.split("-")]
        else: self.tiempo_dia = []
        if aperitivo != "":
            self.aperitivo = [i.strip() for i in aperitivo.split("-")]
        else: self.aperitivo = []
        self.tipo_comida = tipo_comida.strip()
        temp = -1
        if calorias == "alto":
            temp = 1
        elif calorias == "bajo":
            temp = 0
        self.calorias = temp
        self.proteina_alta = int(proteinas)
        if grasas == "alto":
            temp = 1
        elif grasas == "bajo":
            temp = 0
        else:
            temp = -1
        self.grasas = temp
        self.contiene_gluten = int(gluten)
        self.vegano = int(vegano)
        self.contiene_lactosa = int(lactosa)

    def __str__(self):
        return (f"{self.nombre}:\n\t- Perfil Sabor: {self.perfil_sabor}\n\t- Región: {self.region}"
              + f"\n\t- Tiempo del Día: {self.tiempo_dia}\n\t- Tipo Aperitivo: {self.aperitivo}"
              + f"\n\t- Tipo Comida: {self.tipo_comida}\n\t- Calorias: {self.calorias}"
              + f"\n\t- Proteina: {self.proteina_alta}\n\t- Grasas: {self.grasas}"
              + f"\n\t- Gluten: {self.contiene_gluten}\n\t- Vegetariano: {self.vegano}"
              + f"\n\t- Lactosa: {self.contiene_lactosa}")

class BaseDatos():
    bd = []

    def __init__(self):
        self.cargarCSV() # Se crea la lista que fungira como base de datos.

    def cargarCSV(self):
        pwd = getcwd()
        with open(path.join(pwd, "db", "bd.csv"), 'r', encoding="utf-8") as archivo:
           lectorCSV = csv.reader(archivo)
           print(next(lectorCSV))
           for comida in lectorCSV:
               CSVToDict.bd.append(Comida(comida[0], comida[1], comida[2], comida[3],
                                            comida[4], comida[5], comida[6], comida[7],
                                            comida[8], comida[9], comida[10], comida[11]))
           #for i in CSVToDict.bd: # For testing.
           #     print(i)

    """ Descripción: Filtrar productos de acuerdo a sus características.
        Regresa: Una lista con las comidas que cumplen con los filtros.
    """
    def filtrarProductos(self, nombre="", perfil_sabor="", region="",
                 tiempo_dia="", aperitivo="", tipo_comida="",
                 calorias="", proteinas_altas=False, grasas="", sin_gluten=False,
                 vegano=False, sin_lactosa=False):
        resultados = CSVToDict.bd

        print(f"INFO: Función: (filtrarProductos)\n\tArgumentos: {nombre}, {perfil_sabor}, {region}, {tiempo_dia}, {aperitivo}, " +
              f"{tipo_comida}, {calorias}, {proteinas_altas}, {grasas}, {sin_gluten}, " +
              f"{vegano}, {sin_lactosa}")

        if nombre != "":
            print(f"INFO: Buscando con NOMBRE: {nombre}")
            for res in resultados[:]:
                if res.nombre != nombre:
                    resultados.remove(res)
        if perfil_sabor != "":
            print(f"INFO: Buscando por PERFIL DE SABOR: {perfil_sabor}")
            for res in resultados[:]:
                borrar = True
                for perfil in res.perfil_sabor:
                    if perfil == perfil_sabor:
                        borrar = False
                        break
                if borrar: resultados.remove(res)
        if region != "":
            print(f"INFO: Buscando por REGION: {region}")
            for res in resultados[:]:
                if res.region != region:
                    resultados.remove(res)
        if tiempo_dia != "":
            print(f"INFO: Buscando MOMENTO DEL DIA: {tiempo_dia}")
            for res in resultados[:]:
                borrar = True
                for tiempo in res.tiempo_dia:
                    if tiempo == tiempo_dia:
                        borrar = False
                        break
                if borrar: resultados.remove(res)
        if aperitivo != "":
            print(f"INFO: Removiendo APERITIVO distintos de: {aperitivo}")
            for res in resultados[:]:
                borrar = True
                for aper in res.aperitivo:
                    if aper == aperitivo:
                        borrar = False
                        break
                if borrar: resultados.remove(res)
        if tipo_comida != "":
            print(f"INFO: Removiendo TIPO COMIDA distintos de: {tipo_comida}")
            for res in resultados[:]:
                if res.tipo_comida != tipo_comida: resultados.remove(res)
        if calorias != "":
            print(f"INFO: Buscando CALORIAS: {calorias}")
            mapeo = -1
            if calorias == "muchas":
                mapeo = 1
            elif calorias == "pocas":
                mapeo = 0
            if mapeo != -1:
                for res in resultados[:]:
                    if res.calorias != mapeo: resultados.remove(res)
        if grasas != "":
            print(f"INFO: Buscando GRASAS: {grasas}")
            mapeo = -1
            if grasas == "muchas":
                mapeo = 1
            elif grasas == "pocas":
                mapeo = 0
            if mapeo != -1:
                for res in resultados[:]:
                    if res.grasas != mapeo: resultados.remove(res)
        if proteinas_altas:
            print(f"INFO: Buscando PROTEINAS ALTAS: {proteinas_altas}")
            for res in resultados[:]:
                    if not res.proteina_alta:
                        resultados.remove(res)
        if sin_gluten:
            print(f"INFO: Buscando SIN GLUTEN: {sin_gluten}")
            for res in resultados[:]:
                    if res.contiene_gluten:
                        resultados.remove(res)
        if vegano:
            print(f"INFO: Buscando VEGETARIANO: {vegano}")
            for res in resultados[:]:
                if not res.vegano:
                    resultados.remove(res)
        if sin_lactosa:
            print(f"INFO: Buscando SIN LACTOSA: {sin_lactosa}")
            for res in resultados[:]:
                    if res.contiene_lactosa: # True == 1
                        resultados.remove(res)
        
        #for i in resultados: print(i)
        print(f"INFO: # de Coincidencias Encontradas: {len(resultados)}")
        return resultados
        

class ActionMostrarSugerencias(Action):
    def name(self):
        return "mostrar_sugerencias"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Momento del Día: ", tracker.get_slot("momento_del_dia"))
        print("Perfil de sabor: ", tracker.get_slot("perfil_sabor"))
        print("Condiciones Especiales:", tracker.get_slot("condiciones_especiales"))
        print("\t- sin_gluten:", tracker.get_slot("sin_gluten"))
        print("\t- sin_lactosa:", tracker.get_slot("sin_lactosa"))
        print("\t- vegetariano:", tracker.get_slot("vegetariano"))
        print("Aporte Nutricional:", tracker.get_slot("personalizar_aporte_nutricional"))
        print("Tipo de Comida: ", tracker.get_slot("tipo_comida"))
        print("Cantidad de Calorias:", tracker.get_slot("cant_calorias"))
        print("Cantidad de Grasas: ", tracker.get_slot("cant_grasas"))
        print("Cantidad de Proteinas: ", tracker.get_slot("proteinas_altas"))
        print("Region: ", tracker.get_slot("region"))
        #print(tracker.get_slot("cant_gresas"))

class ActionAjustarImagen(Action):
    def name(self):
        return "ajustar_imagen"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Log: Mostrando imagen...")

class ActionConsultarDuda(Action):
    def name(self):
        return "consultar_duda"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        nombre_comida = tracker.get_slot("nombre_comida")
        campo_duda = tracker.get_slot("campo_duda")
        valor_duda =  tracker.get_slot("valor_duda")
        print("Log: Consultando si {0} tiene/es {1} {2} en base de datos...".format(nombre_comida, valor_duda, campo_duda))
