from scraping import bajar, indice_productos, procesar_productos
from menu import mostrar_menu, ejecutar_opcion

# URL inicial
miUrl1 = "https://pasionariafloricultura.com/semillas/"
soup = bajar(miUrl1)

if soup:
    lista_productos = indice_productos(soup)
    productos_procesados = procesar_productos(lista_productos)
    continuar = True

    while continuar:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        continuar = ejecutar_opcion(opcion, productos_procesados)
else:
    print("Error al cargar la página. Verifique su conexión.")