from scraping import filtrar_productos_estacion, filtrar_productos_cultivo, obtener_tipos_de_cultivo, obtener_estaciones_de_venta

def mostrar_menu():
    print("\n--- Menú Principal ---")
    print("1. Mostrar tipos de cultivo disponibles")
    print("2. Mostrar productos por tipo de cultivo")
    print("3. Mostrar tipos de estación en venta")
    print("4. Mostrar productos por tipo de estación de venta")
    print("5. Salir")

def ejecutar_opcion(opcion, productos_procesados):
    if opcion == "1":
        tipos_cultivo = obtener_tipos_de_cultivo(productos_procesados)
        print("Tipos de tiempo de cultivo disponibles:")
        for idx, tipo in enumerate(tipos_cultivo, 1):
            print(f"{idx}. {tipo}")
    elif opcion == "2":
        # Solicitar al usuario seleccionar un tipo de cultivo
        try:
            seleccion = int(input("\nSelecciona el número del tipo de cultivo: "))
            tipos_cultivo = obtener_tipos_de_cultivo(productos_procesados)
            tipo_seleccionado = tipos_cultivo[seleccion - 1]
            print(f"\nHas seleccionado: {tipo_seleccionado}")
            
            # Filtrar los productos según el tipo de cultivo seleccionado
            cultivos = filtrar_productos_cultivo(productos_procesados, tipo_seleccionado)
            print(f"\nProductos con tiempo de cultivo de '{tipo_seleccionado}':")
            for producto in cultivos:
                print(f"- {producto}")
        except (ValueError, IndexError):
            print("Selección no válida.")
    elif opcion == "3":
        # Mostrar tipos de estación en venta
        tipos_estacion = obtener_estaciones_de_venta(productos_procesados)
        print("Tipos de estación en venta disponibles:")
        for idx, tipo in enumerate(tipos_estacion, 1):
            print(f"{idx}. {tipo}")
    elif opcion == "4":
        try:
            seleccion = int(input("\nSelecciona el número del tipo de estación de venta: "))
            tipos_estacion = obtener_estaciones_de_venta(productos_procesados)
            tipo_seleccionado = tipos_estacion[seleccion - 1]
            print(f"\nHas seleccionado: {tipo_seleccionado}")
            productos_estacion = filtrar_productos_estacion(productos_procesados, tipo_seleccionado)
            print(f"\nProductos en estación de venta '{tipo_seleccionado}':")
            for producto in productos_estacion:
                print(f"- {producto}")
        except (ValueError, IndexError):
            print("Selección no válida.")
    elif opcion == "5":
        print("Saliendo del programa. ¡Hasta luego!")
        return False
    else:
        print("Opción no válida. Intente nuevamente.")
    return True