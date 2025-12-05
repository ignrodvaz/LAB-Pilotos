from collections import defaultdict
import csv
from datetime import date, datetime
from typing import NamedTuple

Carrera = NamedTuple("Carrera", 
            [("nombre", str),
             ("escuderia", str),
             ("fecha_carrera", date) ,
             ("temperatura_min", int),
             ("vel_max", float),
             ("duracion",float),
             ("posicion_final", int),
             ("ciudad", str),
             ("top_6_vueltas", list[float]),
             ("tiempo_boxes",float),
             ("nivel_liquido", bool)
            ])

#Carrera(nombre='Fernando Alonso', escuderia='Aston Martin', fecha_carrera=datetime.date(2022, 11, 21), temperatura_min=25, vel_max=330.1, duracion=30.5, 
# posicion_final=-1, ciudad='Abu Dhabi', top_6_vueltas=[31.254, 31.567, 31.789, 32.045, 0, 0], tiempo_boxes=15.23, nivel_liquido=False)

def lee_carreras(ruta_csv:str) -> list[Carrera]:
    with open(ruta_csv, encoding="utf-8")as f:
        lector = csv.reader(f, delimiter=";")
        next(lector)
        res = []
        for nombre, escuderia, fecha_carrera, temperatura_min, vel_max, duracion, pos_final, ciudad, top_6_vueltas, tiempo_boxes, nivel_liquido in lector:
            fecha_carrera = datetime.strptime(fecha_carrera, "%d-%m-%y").date()
            temperatura_min = float(temperatura_min)
            vel_max = float(vel_max)
            duracion = float(duracion)
            pos_final = int(pos_final)
            tiempo_boxes = float(tiempo_boxes) 
            
            top_6_vueltas = parsea_vueltas(top_6_vueltas)
            nivel_liquido = parsea_bool(nivel_liquido)
            
            carreras = Carrera(nombre, escuderia, fecha_carrera, temperatura_min, vel_max, duracion, pos_final, ciudad, top_6_vueltas, tiempo_boxes, nivel_liquido)
            res.append(carreras)
    return res

def parsea_vueltas(cadena_vueltas: str) -> list[float]:
    cadena_limpia = cadena_vueltas.replace("[", "").replace("]", "")
    
    if not cadena_limpia.split():
        return []
    
    trozos = cadena_limpia.split("/")
    lista = []
    for t in trozos:
        t = t.strip()
        if t == "-":
            lista.append(0.0)
        else:
            lista.append(float(t))
    return lista

def parsea_bool(nivel_liquido: str) -> bool:
    # Convertimos a minúsculas y quitamos espacios
    valor = nivel_liquido.strip().lower()
    # Devolvemos True solo si es '1', 'si' o 'true'.
    # 'no' devolverá False automáticamente.
    return valor in ("1", "si", "true")

def media_tiempo_boxes(carreras:list[Carrera], ciudad:str, fecha:date | None =None)->float:
    tiempos = []
    for carrera in carreras:
        if (ciudad == carrera.ciudad):
            if fecha is None or carrera.fecha_carrera == fecha:
                tiempos.append(carrera.tiempo_boxes)
                
        if len(tiempos) == 0:
            media = 0
        else:
            media = sum(tiempos)/len(tiempos)
        
    return media

def pilotos_menor_tiempo_medio_vueltas_top(carreras:list[Carrera], n)->list[tuple[str,date]]:
    lista = []
    for carrera in carreras:
        if 0 not in carrera.top_6_vueltas:
            media = sum(carrera.top_6_vueltas) / len(carrera.top_6_vueltas)
            lista.append((media, carrera.nombre, carrera.fecha_carrera))
    lista.sort()
    return [(carrera[1], carrera[-1]) for carrera in lista][:n]

def ratio_tiempo_boxes_total(carreras:list[Carrera])->list[tuple[str,date, float]]:
    tiempo_boxes_fecha = defaultdict(float)
    for carrera in carreras:
        tiempo_boxes_fecha[carrera.fecha_carrera] += carrera.tiempo_boxes
        
    res = [(carrera.nombre, carrera.fecha_carrera, round(carrera.tiempo_boxes/tiempo_boxes_fecha[carrera.fecha_carrera], 3)) for carrera in carreras]
    return sorted(res, key=lambda t:t[2], reverse=True)

def puntos_piloto_anyos(carreras:list[Carrera])->dict[str, list[int]]:
    puntos_por_piloto_y_anyo = defaultdict(int)
    for carrera in carreras:
        anyo = carrera.fecha_carrera.year
        puntos_por_piloto_y_anyo[(carrera.nombre, anyo)] += (total_puntos_por_piloto(carrera))
        
    agrupado_temporal = {}
    for(nombre, anyo), puntos in puntos_por_piloto_y_anyo.items():
        if nombre not in agrupado_temporal:
            agrupado_temporal[nombre] = []
        agrupado_temporal[nombre].append((anyo, puntos))
    
    res = {}
    for nombre, lista_tuplas in agrupado_temporal.items():
        lista_tuplas.sort()
        res[nombre] = [puntos for (anyo, puntos) in lista_tuplas]
    return res
        
def total_puntos_por_piloto(carrera: Carrera) -> int:
    puntos = 0
    if carrera.posicion_final == 1:
        puntos += 50
    elif carrera.posicion_final == 2:
        puntos += 25
    elif carrera.posicion_final == 3:
        puntos += 10
    else:
        puntos += 0
    return puntos

def mejor_escuderia_anyo(carreras:list[Carrera], anyo:int)->str:
    victorias_por_escuderia = defaultdict(int)
    for carrera in carreras:
        victorias_por_escuderia[carrera.fecha] += victorias(carrera)
        
    return victorias_por_escuderia
        
def victorias(carrera: Carrera):
    victoria = 0
    if carrera.posicion_final == 1:
        victoria += 1
    return victoria