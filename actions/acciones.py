from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from datetime import datetime

class ActionSetTime(Action):
    def name(self) -> Text:
        return "set_time"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        momento_del_dia = ""
        now = datetime.now()
        hour = now.hour
        #Check if it's morning, noon or evening.
        if hour >= 0 and hour < 12:
            momento_del_dia = "Desayuno"
        elif hour >= 12 and hour < 18:
            momento_del_dia = "Comida"
        else:
            momento_del_dia = "Cena"

        return [SlotSet("momento_del_dia", momento_del_dia)]

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

