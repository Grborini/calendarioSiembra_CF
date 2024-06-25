import os
import colorama
import json
from datetime import datetime, timedelta

ruta_json = "Calendario_v3\\Especies.json"

try:
    with open(ruta_json, 'r', encoding='utf-8') as archivo:
        especies = json.load(archivo)

    def limpiarPantalla():
        os.system('cls' if os.name == 'nt' else 'clear')
        return

    def buscar_por_especie(busqueda_especie):
        limpiarPantalla()
        print(colorama.Fore.RED + "*" * 50)
        print(colorama.Fore.GREEN + "Usted eligió Búsqueda por Especie.")
        print(colorama.Fore.RED + "*" * 50)
        
        busqueda_especie = busqueda_especie.lower()
        
        try:
            with open(ruta_json, 'r', encoding='utf-8') as archivo:
                especies = json.load(archivo)
                
                busqueda = {cla.lower(): val for cla, val in especies.items()}.get(busqueda_especie)
                
                if busqueda:
                    detalles_formateados = ""
                    for clave, valor in busqueda.items():
                        detalles_formateados += f"{colorama.Fore.GREEN + clave}: {colorama.Fore.RESET + valor}\n"
                    print(f"{colorama.Fore.YELLOW + busqueda_especie}:\n{detalles_formateados}")
                else:
                    print(f"{colorama.Fore.YELLOW + busqueda_especie} no encontrada en la lista.")
                input(colorama.Fore.YELLOW +"presione enter para continuar")
        except FileNotFoundError:
            print("El archivo 'Especies.json' no existe.")

    def buscar_por_estacion(estacion):
        limpiarPantalla()
        print(colorama.Fore.RED + "*" * 50)
        print(colorama.Fore.GREEN + "Usted ha seleccionado: Búsqueda por estación.")
        print(colorama.Fore.RED + "*" * 50)

        estacion = estacion.lower().strip()

        try:
            with open(ruta_json, 'r', encoding='utf-8') as archivo:
                especies = json.load(archivo)
                busqueda_estacion = []
                for especie, detalles in especies.items():
                    momento_de_siembra = detalles.get("Momento de siembra", "")
                    estaciones = [e.strip().lower() for e in momento_de_siembra.split(',')]
                    if estacion in estaciones:
                        busqueda_estacion.append(especie.lower())
                if busqueda_estacion:
                    print(colorama.Fore.RESET + f"Especies que se pueden sembrar en {colorama.Fore.GREEN + estacion.capitalize()}:")
                    for especie in busqueda_estacion:
                        print(colorama.Fore.GREEN + f"- {especie.capitalize()}")
                    ver_detalles = input(colorama.Fore.RESET + "¿Quieres ver los detalles de alguna especie? (s/n): ").strip().lower()
                    if ver_detalles == "s":
                        limpiarPantalla()
                        especie_seleccionada = input("Escribe el nombre de la especie que quieres ver: ").strip().lower()
                        if especie_seleccionada in busqueda_estacion:
                            detalles = especies[especie_seleccionada.capitalize()]
                            detalles_formateados = ""
                            for clave, valor in detalles.items():
                                detalles_formateados += f"{colorama.Fore.GREEN + clave}: {colorama.Fore.RESET + valor}\n"
                            print(f"{colorama.Fore.YELLOW + especie_seleccionada.capitalize()}:\n{detalles_formateados}")
                        else:
                            print(colorama.Fore.RESET + f"La especie {colorama.Fore.GREEN + especie_seleccionada.capitalize()} no está en la lista de especies para {estacion}.")
                else:
                    print(colorama.Fore.RED + f"No se encontraron especies para el momento de siembra: {estacion}")
            input(colorama.Fore.YELLOW + "presione enter para continuar")
        except FileNotFoundError:
            print(colorama.Fore.RED + "El archivo 'Especies.json' no existe.")

    def Agregar_especie():
        limpiarPantalla()
        print(colorama.Fore.RED + "*" * 50)
        print(colorama.Fore.GREEN + "Usted ha seleccionado: Agregar una especie.")
        print(colorama.Fore.RED + "*" * 50)
        
        especie_nombre = input(colorama.Fore.RESET + "Ingresa el nombre de la especie: ").capitalize()
        
        especie_elementos = {
            "Momento de siembra": input("Momento de siembra: "),
            "Metodo de siembra": input("Método de siembra: "),
            "Profundidad de siembra": input("Profundidad de siembra: "),
            "Distancia entre plantas": input("Distancia entre plantas: "),
            "Distancia entre surcos": input("Distancia entre surcos: "),
            "Tiempo de germinacion": input("Tiempo de germinacion: "),
            "Trasplante (si aplica)": input("Trasplante (si aplica): "),
            "Tiempo de cosecha": input("Tiempo de cosecha: "),
            "Abonado": input("Abonado: "),
            "Riego": input("Riego: "),
            "plagas/observaciones": input("Plagas/observaciones: ")
        }
        
        try:
            with open(ruta_json, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
        except FileNotFoundError:
            datos = {}
        except json.JSONDecodeError:
            print(colorama.Fore.RED + "Error al leer el archivo 'Especies.json'. Asegúrate de que el formato del archivo sea correcto.")
            return
        
        datos[especie_nombre] = especie_elementos
        
        try:
            with open(ruta_json, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=4)
            print(colorama.Fore.GREEN + f"La especie '{especie_nombre}' se ha agregado con éxito!.")
            input(colorama.Fore.YELLOW + "presione enter para continuar")
        except IOError:
            print(colorama.Fore.RED + "Error al guardar el archivo 'Especies.json'.")

    def Modificar_especie(nombre_especie):
        limpiarPantalla()
        print(colorama.Fore.RED + "*" * 50)
        print(colorama.Fore.GREEN + "Usted ha seleccionado: Modificar una especie.")
        print(colorama.Fore.RED + "*" * 50)
        nombre_especie = nombre_especie.capitalize()
        try:
            with open(ruta_json, 'r', encoding='utf-8') as archivo:
                especies = json.load(archivo)
            
            if nombre_especie in especies:
                especie_elementos = especies[nombre_especie]
                print(colorama.Fore.RESET + "Ingresa los nuevos valores para la especie (deja vacío para mantener el valor actual):")
                
                for clave in list(especie_elementos.keys()):
                    nuevo_valor = input(f"Nuevo {clave}: ") or especie_elementos[clave]
                    especie_elementos[clave] = nuevo_valor
                
                especies[nombre_especie] = especie_elementos
                
                with open(ruta_json, 'w', encoding='utf-8') as archivo:
                    json.dump(especies, archivo, ensure_ascii=False, indent=4)
                
                print(colorama.Fore.RED + f"La especie '{colorama.Fore.GREEN + nombre_especie}' ha sido modificada correctamente.")
            else:
                print(colorama.Fore.RED + f"La especie '{colorama.Fore.GREEN + nombre_especie}' no existe en el archivo.")
            input(colorama.Fore.YELLOW + "presione enter para continuar")
        except FileNotFoundError:
            print(colorama.Fore.RED + "El archivo 'Especies.json' no existe.")
        except json.JSONDecodeError:
            print(colorama.Fore.RED + "Error al leer el archivo 'Especies.json'. Asegúrate de que el formato del archivo sea correcto.")

    def Eliminar_especie():
        limpiarPantalla()
        print(colorama.Fore.RED + "*" * 50)
        print(colorama.Fore.GREEN + "Usted eligió eliminar Especie.")
        print(colorama.Fore.RED + "*" * 50)
        try:
            with open(ruta_json, 'r', encoding='utf-8') as archivo:
                especies = json.load(archivo)
            
            print(colorama.Fore.GREEN +"Especies en el Calendario:")
            for nombre_especie in especies.keys():
                print(f"- {nombre_especie}")
            
            especie_a_eliminar = input(colorama.Fore.RESET +"Escribe el nombre de la especie que deseas eliminar: ").capitalize()
            if especie_a_eliminar in especies:
                confirmacion = input(f"Estás seguro que deseas eliminar la especie '{especie_a_eliminar}'? (s/n): ").lower()
                if confirmacion == 's':
                    del especies[especie_a_eliminar]
                    with open(ruta_json, 'w', encoding='utf-8') as archivo:
                        json.dump(especies, archivo, ensure_ascii=False, indent=4)
                    print(f"La especie '{especie_a_eliminar}' ha sido eliminada correctamente.")
                elif confirmacion == 'n':
                    print(colorama.Fore.RED + "Eliminación cancelada.")
                else:
                    print(colorama.Fore.RED + "Respuesta no válida. Eliminación cancelada.")
            else:
                print(colorama.Fore.RED + "La especie no se encuentra en el archivo.")
            input(colorama.Fore.YELLOW + "presione enter para continuar")
        except FileNotFoundError:
            print("El archivo 'Especies.json' no existe.")
        except json.JSONDecodeError:
            print("Error al leer el archivo 'Especies.json'. Asegúrate de que el formato del archivo sea correcto.")

    #Funcion para listar las Especies.
    '''En esta funcion:
    Recorremos al diccionario con un for 
    para extraer por separado las claves y valores y mostrarlas formateadas para 
    mejor visibilidad y atractivo'''
    def Listar_especies():
        limpiarPantalla()
        print(colorama.Fore.RED + "*" * 50)
        print(colorama.Fore.GREEN + "Usted eligió listar las especies.")
        print(colorama.Fore.RED + "*" * 50)
        try:
            with open(ruta_json, 'r', encoding='utf-8') as archivo:
                especies = json.load(archivo)
            
            print(colorama.Fore.GREEN + "Especies en el Calendario:")
            for nombre_especie in especies.keys():
                print(f"- {nombre_especie}")
            
            # Preguntar al usuario si desea ver detalles de alguna especie.
            ver_detalles = input(colorama.Fore.RESET + "¿Quieres ver los detalles de alguna especie? (s/n): ").strip().lower()
            if ver_detalles == "s":
                nombre_especie = input("Escribe el nombre de la especie para ver los detalles: ").capitalize()
                limpiarPantalla()
                if nombre_especie in especies:
                    print(colorama.Fore.RESET + f"Detalles de la especie '{colorama.Fore.YELLOW + nombre_especie}':")
                    for clave, valor in especies[nombre_especie].items():
                        print(f"{colorama.Fore.GREEN + clave}: {colorama.Fore.RESET + valor}")
                else:
                    print(colorama.Fore.RED + "La especie no se encuentra en el archivo.")
            elif ver_detalles == "n":
                print(colorama.Fore.RED +"Operación cancelada.")
            else:
                print(colorama.Fore.RED +"Respuesta no válida. Por favor, intenta de nuevo.")
            input(colorama.Fore.YELLOW + "presione enter para continuar")
        except FileNotFoundError:
            print(colorama.Fore.RED + "El archivo 'Especies.json' no existe.")
        except json.JSONDecodeError:
            print(colorama.Fore.RED + "Error al leer el archivo 'Especies.json'. Asegúrate de que el formato del archivo sea correcto.")

    def calcular_dia_de_cosecha(nombre_especie, fecha_siembra):
        limpiarPantalla()
        print(colorama.Fore.RED + "*" * 50)
        print(colorama.Fore.GREEN + "Usted ha seleccionado: Calcular días de cosecha.")
        print(colorama.Fore.RED + "*" * 50)

        try:
            with open(ruta_json, 'r', encoding='utf-8') as archivo:
                especies = json.load(archivo)
            
            nombre_especie = nombre_especie.capitalize()
            if nombre_especie in especies:
                detalles = especies[nombre_especie]
                tiempo_cosecha = detalles["Tiempo de cosecha"]
                tiempo_trasplante = detalles.get("Trasplante (si aplica)", None)

                # Verificar y manejar el tiempo de cosecha con rango
                if "a" in tiempo_cosecha.lower():  # Verifica si hay un rango de días
                    try:
                        dias = tiempo_cosecha.split(" a ")
                        dias_min = int(dias[0].strip())
                        dias_max = int(dias[1].strip().split()[0])
                        fecha_cosecha_min = fecha_siembra + timedelta(days=dias_min)
                        fecha_cosecha_max = fecha_siembra + timedelta(days=dias_max)
                        print(colorama.Fore.RESET + f"El rango estimado de cosecha es desde {colorama.Fore.GREEN + fecha_cosecha_min.strftime('%d/%m/%Y')} hasta {colorama.Fore.GREEN + fecha_cosecha_max.strftime('%d/%m/%Y')}.")
                    except ValueError:
                        return None
                else:
                    dias_cosecha = int(tiempo_cosecha.split()[0])
                    fecha_cosecha = fecha_siembra + timedelta(days=dias_cosecha)
                    print(colorama.Fore.RESET + f"El tiempo estimado de cosecha para la especie '{colorama.Fore.GREEN + nombre_especie}' es {colorama.Fore.GREEN + fecha_cosecha.strftime('%d/%m/%Y')}.")

                if tiempo_trasplante:
                    print(colorama.Fore.YELLOW + f"¡Atención! Esta especie requiere trasplante en {tiempo_trasplante}.")
            else:
                print(colorama.Fore.RED + f"La especie '{colorama.Fore.GREEN + nombre_especie}' no se encuentra en el archivo.")
            input("presione enter para continuar")
        except FileNotFoundError:
            print(colorama.Fore.RED + "El archivo 'Especies.json' no existe.")
        except json.JSONDecodeError:
            print(colorama.Fore.RED + "Error al leer el archivo 'Especies.json'. Asegúrate de que el formato del archivo sea correcto.")
        except ValueError:
            print(colorama.Fore.RED + "Error en el formato de tiempo de cosecha. Asegúrate de que el formato sea 'X días' o 'X a Y días'.")


    
    def menu():
        while True:
            limpiarPantalla()
            print(colorama.Fore.RESET + "\n")
            print(colorama.Fore.RED + "*" * 50)
            print(colorama.Fore.GREEN + "CALENDARIO DE SIEMBRA HEMISFERIO SUR")
            print(colorama.Fore.RED + "*" * 50)
            print(colorama.Fore.YELLOW + "Seleccione una opción:")
            print(colorama.Fore.GREEN + "1: ",colorama.Fore.YELLOW +"Buscar por especie")
            print(colorama.Fore.GREEN + "2: ",colorama.Fore.YELLOW +"Buscar por estación")
            print(colorama.Fore.GREEN + "3: ",colorama.Fore.YELLOW +"Agregar especie")
            print(colorama.Fore.GREEN + "4: ",colorama.Fore.YELLOW +"Modificar especie")
            print(colorama.Fore.GREEN + "5: ",colorama.Fore.YELLOW +"Eliminar especie")
            print(colorama.Fore.GREEN + "6: ",colorama.Fore.YELLOW +"Listar especies")
            print(colorama.Fore.GREEN + "7: ",colorama.Fore.YELLOW +"Calcular días de cosecha")
            print(colorama.Fore.GREEN + "8: ",colorama.Fore.YELLOW +"Salir")
            
            opcion = input(colorama.Fore.RESET + "Ingrese el número de la opción deseada: ")
            
            if opcion == "1":
                busqueda_especie = input("Ingrese el nombre de la especie que desea buscar: ")
                buscar_por_especie(busqueda_especie)
            elif opcion == "2":
                estacion = input("Ingrese la estación (primavera, verano, otoño, invierno): ")
                buscar_por_estacion(estacion)
            elif opcion == "3":
                Agregar_especie()
            elif opcion == "4":
                nombre_especie = input("Ingrese el nombre de la especie que desea modificar: ")
                Modificar_especie(nombre_especie)
            elif opcion == "5":
                Eliminar_especie()
            elif opcion == "6":
                Listar_especies()
            elif opcion == "7":
                nombre_especie = input("Ingrese el nombre de la especie: ")
                fecha_siembra_str = input("Ingrese la fecha de siembra (formato: dd/mm/aaaa): ")
                try:
                    fecha_siembra = datetime.strptime(fecha_siembra_str, "%d/%m/%Y")
                    calcular_dia_de_cosecha(nombre_especie, fecha_siembra)
                except ValueError:
                    print(colorama.Fore.RED + "Formato de fecha incorrecto. Por favor, use el formato dd/mm/aaaa.")
            elif opcion == "8":
                limpiarPantalla()
                print(colorama.Fore.RED + "*" * 50)
                print(colorama.Fore.GREEN + "¡Gracias por usar el calendario de siembra! Hasta luego.")
                print(colorama.Fore.RED + "*" * 50)
                break
            else:
                print(colorama.Fore.RED + "Opción no válida, por favor ingrese un número del 1 al 8.")

    if __name__ == "__main__":
        menu()

except json.JSONDecodeError:
    print(colorama.Fore.RED + "Error al leer el archivo 'Especies.json'. Asegúrate de que el formato del archivo sea correcto.")
except FileNotFoundError:
    print(colorama.Fore.RED + "El archivo 'Especies.json' no existe.")
