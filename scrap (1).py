from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


def make_request(url, headers=None):
    request = Request(url, headers=headers or {})
    try:
       with urlopen(request, timeout=10) as response:
             print(response.status)
             return response.read(), response
    except HTTPError as error:
         print(error.status, error.reason)
    except URLError as error:
         print(error.reason)
    except TimeoutError:
         print("Request timed out")

def bajar(laDir): 
   laPag = urlopen(laDir) 
   return BeautifulSoup(laPag.read(),features="html.parser")


agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41"
url = "https://pasionariafloricultura.com/semillas/"

body, response = make_request(
    url,
    {"User-Agent": agent}
)
 
realBody = body.decode("utf-8")
###print (body.decode("utf-8"))
soup = BeautifulSoup(realBody)


print(soup.prettify())
"""
if body:
    realBody = body.decode("utf-8")
    soup = BeautifulSoup(realBody, 'html.parser')  # Especificar el parser
    print(soup.prettify())  # Imprimir el HTML en formato bonito


    print("Indice:")
    for title in soup.find_all("h2", class_="woocommerce-loop-product__title"):
        print(title.get_text())

else:
    print("Failed to retrieve content.")"""

def obtener_indice(url):
    if body:  # Verifica que la solicitud fue exitosa
        realBody = body.decode("utf-8")
        soup = BeautifulSoup(realBody, 'html.parser')
        titulos = []
        for title in soup.find_all("h2", class_="woocommerce-loop-product__title"):
            titulos.append(title.get_text())

        return titulos
    else:
        print(f"Error al obtener el contenido. Código de estado: {response.status_code}")
        return []

url = "https://pasionariafloricultura.com/semillas/"
titulos = obtener_indice(url)

print("indice encontrados:")
for indice, titulo in enumerate(titulos, 1):
    print(f"{indice}. {titulo}")

def extract_pages(url):
    if body:
        realBody = body.decode("utf-8")
        soup = BeautifulSoup(realBody, 'html.parser')

        # Extraer el número total de páginas
        pagination_meta = soup.find("span", class_="pagination-meta")
        if pagination_meta:
            total_pages = pagination_meta.get_text(strip=True)
            print(total_pages)

        # Buscar todos los enlaces de paginación
        pages = []
        
        # Página actual
        current_page = soup.find("span", class_="current").get_text(strip=True)
        pages.append(current_page)
        
        # Otras páginas
        for a in soup.find_all("a", class_=["inactive", "next_page"]):
            page_number = a.get_text(strip=True)
            page_link = a['href']
            pages.append((page_number, page_link))

        return pages
    return []

# Usar la función
url = "https://pasionariafloricultura.com/semillas/"
pages = extract_pages(url)
print(pages)