from f1 import *
from datetime import date

# def test_media_tiempo_boxes(datos):
#     print("\n### PROBANDO media_tiempo_boxes ###")

#     # CASO 1: Ciudad 'Abu Dhabi', sin filtrar por fecha (coge todas)
#     # Resultado esperado: 14.218
#     res1 = media_tiempo_boxes(datos, "Abu Dhabi", None)
#     print(f"1. Abu Dhabi (Todas): {res1} (Esperado: 14.218)")

#     # CASO 2: Ciudad 'Abu Dhabi', fecha específica '2022-11-21'
#     # Resultado esperado: 14.218
#     res2 = media_tiempo_boxes(datos, "Abu Dhabi", date(2022, 11, 21))
#     print(f"2. Abu Dhabi (21-11-22): {res2} (Esperado: 14.218)")

#     # CASO 3: Ciudad 'Abu Dhabi', fecha donde NO hubo carrera
#     # Resultado esperado: 0
#     res3 = media_tiempo_boxes(datos, "Abu Dhabi", date(2023, 1, 1))
#     print(f"3. Abu Dhabi (Fecha incorrecta): {res3} (Esperado: 0)")

#     # CASO 4: Ciudad que no existe en el CSV
#     # Resultado esperado: 0
#     res4 = media_tiempo_boxes(datos, "Sevilla")
#     print(f"4. Sevilla (Ciudad inventada): {res4} (Esperado: 0)")
    
#     n = 5
#     res5 = pilotos_menor_tiempo_medio_vueltas_top(datos, n)
#     print(f"5. Los {n} pilotos con menor tiempo son {res5}")

if __name__ == "__main__":
    datos = lee_carreras("./LAB-Pilotos/data/f1.csv")
    # print(f"Leídos {len(datos)} datos.")
    # print("Mostrando los 2 primeros:")
    # for dato in datos[:2]:
    #     print(dato)
        
    # print("Mostrando los 2 últimos:")
    # for dato in datos[-2:]:
    #     print(dato)
    # test_media_tiempo_boxes(datos)
    # pilotos_menor_tiempo_medio_vueltas_top(datos, 5)
    # e = ratio_tiempo_boxes_total(datos)
    # for res in e: 
    #     print(f"Este es la funcion del ratio {res} \n")
    
    print(puntos_piloto_anyos(datos))
    print(mejor_escuderia_anyo(datos, 2022))