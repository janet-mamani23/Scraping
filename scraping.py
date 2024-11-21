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
            return response.read(), response
    except (HTTPError, URLError, TimeoutError) as error:
        print(f"Error al acceder a {miUrl}: {error}")
        return None, None

def bajar(miUrl, headers=None):
    body, _ = make_request(miUrl, headers)
    if body:
        return BeautifulSoup(body.decode("utf-8"), 'html.parser')
    else:
        return None

def indice_productos(soup):
    lista_productos = []    
    productos = soup.find_all('div', class_="inner_product main_color wrapped_style noLightbox av-product-class-")

    for producto in productos:
        nombre = producto.find('h2', class_="woocommerce-loop-product__title").get_text(strip=True)
        enlace = producto.find('a', class_="woocommerce-LoopProduct-link woocommerce-loop-product__link")['href']
        lista_productos.append({"NOMBRE": nombre, "ENLACE": enlace})
    return lista_productos 

def procesar_productos(lista_productos):
    productos_detallados = []
    for dic in lista_productos:
        try:
            laSopa = bajar(dic["ENLACE"])
            if laSopa:
                tabla = laSopa.find('table')
                if tabla:
                    info_producto = {}
                    for fila in tabla.find_all('tr'):
                        celdas = fila.find_all('td')
                        
                        if len(celdas) == 2:  # Solo procesar las filas con 2 celdas
                            clave = celdas[0].get_text(strip=True)
                            valor = celdas[1].get_text(strip=True)
                            info_producto[clave] = valor 
                    productos_detallados.append({"NOMBRE": dic["NOMBRE"], "DETALLES": info_producto})
        except Exception as e:
            print(f"Error al procesar el producto {dic['NOMBRE']}: {e}")
    return productos_detallados

def obtener_estaciones_de_venta(productos_procesados):
    estaciones_de_venta = set()  # Usamos un set para evitar duplicados
    for producto in productos_procesados:
        detalles = producto.get("DETALLES", {})
        estacion_venta = detalles.get("ESTACION DE VENTA", "").lower()
        if estacion_venta:  # Asegurarnos de que no esté vacío
            estaciones_de_venta.add(estacion_venta)
    return list(estaciones_de_venta)  # Convertimos el set de nuevo a lista

def filtrar_productos_estacion(productos_procesados, estacion_seleccionado):
    productos_filtrados = []  # Lista para almacenar los nombres
    for producto in productos_procesados:
        detalles = producto.get("DETALLES", {})
        estacion_venta = detalles.get("ESTACION DE VENTA", "").lower()
        if estacion_seleccionado.lower() in estacion_venta:  # Compara con el tipo seleccionado
            productos_filtrados.append(producto["NOMBRE"])
    return productos_filtrados

def obtener_tipos_de_cultivo(productos_procesados):
    tipos_cultivo = set()  # Usamos un set para evitar duplicados
    for producto in productos_procesados:
        detalles = producto.get("DETALLES", {})
        cultivo = detalles.get("TIEMPO DE CULTIVO", "").lower()
        if cultivo:
            tipos_cultivo.add(cultivo)
    return list(tipos_cultivo)

def filtrar_productos_cultivo(productos_procesados, tipo_cultivo):
    productos_filtrados = []  # Lista para almacenar los nombres
    for producto in productos_procesados:
        detalles = producto.get("DETALLES", {})
        cultivo = detalles.get("TIEMPO DE CULTIVO", "").lower()
        if tipo_cultivo in cultivo:
            productos_filtrados.append(producto["NOMBRE"])
    return productos_filtrados

