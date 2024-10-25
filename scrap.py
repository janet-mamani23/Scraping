from urllib.request import urlopen 
from bs4 import BeautifulSoup


def bajar(laDir): 
   laPag = urlopen(laDir) 
   return BeautifulSoup(laPag.read()) 
   
def leeLinea(linea):
   lista = []
   for dato in linea.find_all('td'):
      lista.append(dato.get_text())
   return lista
   
def leeTabla(tabla):
    filas = []
    for fila in tabla.find_all('tr'):
       filas.append(leeLinea(fila))
    return filas
    
    
miDir = "https://es.wikipedia.org/wiki/C%C3%B3rdoba_(Argentina)"
laSopa = bajar(miDir)
lasTablas = laSopa.find_all("table")
tablaClima = lasTablas[6]
tabla = leeTabla(tablaClima)

