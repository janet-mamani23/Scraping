from bs4 import BeautifulSoup
from urllib.request import urlopen, Request, HTTPError, URLError

#TODO- solicitud HTTP a una URL

def make_request(miUrl, headers=None):
    request = Request(miUrl, headers=headers or {})
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


def bajar(miUrl, headers=None):
    body, response = make_request(miUrl, headers)
    if body:
        return BeautifulSoup(body.decode("utf-8"), 'html.parser')
    else:
        print("Error al descargar la página.")
        return None
    
agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41"
miUrl1 = "https://pasionariafloricultura.com/semillas/"
 
##realBody = body.decode("utf-8")
###print (body.decode("utf-8"))
##soup = BeautifulSoup(realBody)  // En la soup siguiente esta implementado todo

soup = bajar(miUrl1, {"User-Agent": agent})
#print(soup.prettify())

def obtener_indice(soup):
    titulos = []
    for title in soup.find_all("h2", class_="woocommerce-loop-product__title"):
        titulos.append(title.get_text())
    return titulos

titulos = obtener_indice(soup)

print("indice encontrados:")
for indice, titulo in enumerate(titulos, 1):
    print(f"{indice}. {titulo}")

