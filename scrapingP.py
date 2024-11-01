from bs4 import BeautifulSoup
from urllib.request import urlopen, Request, HTTPError, URLError

def make_request(miUrl, headers=None):
    headers = headers or {}
    headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    })
    request = Request(miUrl, headers=headers)
    
    try:
        with urlopen(request, timeout=10) as response:
            print(response.status)
            return response.read(), response
    except HTTPError as error:
        print(error.status, error.reason)
        return None, None
    except URLError as error:
        print(error.reason)
        return None, None
    except TimeoutError:
        print("Request timed out")
        return None, None

def bajar(miUrl, headers=None):
    body, response = make_request(miUrl, headers)
    if body:
        return BeautifulSoup(body.decode("utf-8"), 'html.parser')
    else:
        print("Error al descargar la página.")
        return None

    
def indice_productos(soup):  # Encuentra todos los productos en el soup
    lista_productos = []    
    productos = soup.find_all('div', class_="inner_product main_color wrapped_style noLightbox av-product-class-")

    for producto in productos:
        nombre = producto.find('h2', class_="woocommerce-loop-product__title").get_text(strip=True)  # Extrae el nombre del producto
        enlace = producto.find('a', class_="woocommerce-LoopProduct-link woocommerce-loop-product__link")['href'] # Extrae el enlace de la página del producto
        # Extrae la URL de la imagen del producto
        img_tag = producto.find('img', class_="wp-post-image")
        imagen = img_tag['data-src'] if img_tag and 'data-src' in img_tag.attrs else img_tag['src'] if img_tag else None
        
        lista_productos.append({  # Agrega la información del producto a la lista
            "NOMBRE": nombre,
            "ENLACE": enlace,
            #"IMAGEN": imagen
        })

    return lista_productos 

def procesar_productos(lista_productos):
    productos_detallados = []  # Lista para almacenar detalles de cada producto
    for dic in lista_productos:
        miDir = dic["ENLACE"]
        laSopa = bajar(miDir)  # Llama a la función para obtener el contenido de la página
        if laSopa:
            # Busca la tabla y extrae la información de producto en una sola función
            tabla = laSopa.find('table')
            if tabla:
                info_producto = {}
                for fila in tabla.find_all('tr'):
                    columnas = fila.find_all('td')
                    if len(columnas) == 2:  # Asegúrate de que hay dos columnas
                        clave = columnas[0].get_text(strip=True)
                        valor = columnas[1].get_text(strip=True)
                        info_producto[clave] = valor
                
                # Almacena los detalles en un diccionario si se encontró información
                producto_detallado = {
                    "NOMBRE": dic["NOMBRE"],
                    "DETALLES": info_producto
                }
                productos_detallados.append(producto_detallado)
            else:
                print("No se encontró información de la tabla para este producto.")
        else:
            print(f"No se pudo acceder a la página de {dic['NOMBRE']}")

    return productos_detallados  # Retorna la lista con los detalles de los productos

def filtrar_productos_inviernos(productos_procesados):
    nombres_inviernos = []  # Lista para los nombres de los productos de espacio de venta TODO EL AÑO
    for producto in productos_procesados:
        detalles = producto.get("DETALLES", {})
        # Verifica y muestra el valor del atributo "espacio de venta" para depurar
        estacion_venta = detalles.get("ESTACION DE VENTA", "").strip().lower()  # Elimina espacios adicionales y pasa a minúsculas
        print(f"Producto: {producto['NOMBRE']}, Espacio de venta: {estacion_venta}")
        
        # Verificar si el producto pertenece a "espacio de venta TODO EL AÑO"
        if estacion_venta == "TODO EL AÑO":
            nombres_inviernos.append(producto["NOMBRE"])  # Solo se agrega el nombre si coincide
    
    return nombres_inviernos
    

# Llama a la función bajar y realiza el scraping
miUrl1 = "https://pasionariafloricultura.com/semillas/"
soup = bajar(miUrl1)

lista_productos = indice_productos(soup)
print(f"lista {lista_productos}")
productos_procesados = procesar_productos(lista_productos)
print(f"PRODUCTOS{productos_procesados}")
nombres_inviernos = filtrar_productos_inviernos(productos_procesados)
print("Plantas de espacio en venta invierno:", nombres_inviernos)


"""for dic in lista_productos:
   miDir = dic["ENLACE"] 
   laSopa = bajar(miDir)
   print("ok")
   if laSopa:
        print(f"Información del producto: {dic['NOMBRE']}") # Extrae información de la tabla dentro de la página del producto
        producto_info = tabla_producto(laSopa)  # Imprime la información obtenida del producto, si está disponible
        if producto_info:
            print(producto_info)
        else:
            print("No se encontró información de la tabla para este producto.")
   else:
        print(f"No se pudo acceder a la página de {dic['NOMBRE']}")
        
def obtener_productos_clima_verano(lista_productos):
    productos_verano = []
    for dic in lista_productos:
        if dic.get('ESTACION DE VENTA') and 'verano' in dic['ESTACION DE VENTA'].lower():
            productos_verano.append(dic)

    return productos_verano"""


"""if soup:
    # Solo se ejecuta si se obtuvo el contenido correctamente
    print(soup.prettify())  # Solo imprime el HTML si se obtuvo correctamente

    productos = indice_productos(soup)  # Obtiene la lista de productos

    # Procesa cada producto
    for dic in productos:
        miDir = dic["ENLACE"]  # Extrae el enlace del producto
        laSopa = bajar(miDir)
        if laSopa:
            print(f"Información del producto: {dic['NOMBRE']}")
            producto = tabla_producto(laSopa)
            
            if producto:
                # Asigna el clima al diccionario del producto
                dic["CLIMA"] = producto.get('Clima', None)  # Cambia 'Clima' si el nombre de la clave es diferente
                print(producto)
            else:
                print("No se encontró información del producto.")
        else:
            print(f"No se pudo acceder a la página del producto: {dic['NOMBRE']}")

    # Filtra los productos de clima verano
    productos_verano = obtener_productos_clima_verano(productos)

    # Imprime los productos de clima verano
    if productos_verano:
        print("Productos de clima verano:")
        for p in productos_verano:
            print(f"Nombre: {p['NOMBRE']}, Clima: {p['ESTACION DE VENTA']}")
    else:
        print("No se encontraron productos de clima verano.")
else:
    print("No se pudo obtener el contenido de la página.")"""
    