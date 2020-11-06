# Importamos las librerias
import requests
from bs4 import BeautifulSoup
import builtwith
import whois
import pandas as pd
import time
import os


# Tecnologia con la que se ha creado la web
def tecnologia(URL):
    technology = builtwith.builtwith(URL)
    print(technology)


# Información del propietario de la web
def propietario(URL):
    owner = whois.whois(URL)
    print('Domain name: {}'.format(owner['domain_name']))
    print('Creation date: {}'.format(owner['creation_date']))
    print('City: {}'.format(owner['city']))
    print('State: {}'.format(owner['state']))
    print('Zipcode: {}'.format(owner['zipcode']))
    print('Country: {}'.format(owner['country']))


# Escrapea la imagen dada su URL por parámetro y la guarda en una carpeta
# imagenes en el directorio donde se encuetra este programa
def scrap_image(source_url, headers):
    # Hacemos la request y añadimos un retraso exponencial
    # para evitar satura el servidor de peticiones
    t1 = time.time()
    r = requests.get(source_url, stream = True, headers=headers)
    response_delay = time.time() - t1
    time.sleep(5 * response_delay)
    # Si la request es correcta se scrapea la imagen
    if r.status_code == 200:
        ruta_actual = os.getcwd().replace("\\", "/")
        ruta_imagenes = ruta_actual + '/imagenes'
        # Si no existe el directorio imagenes lo creamos
        if not os.path.exists(ruta_imagenes):
            os.mkdir(ruta_imagenes)
        aSplit = source_url.split('/')
        ruta = ruta_imagenes + "/" + aSplit[len(aSplit)-1]
        output = open(ruta,"wb")
        for chunk in r:
            output.write(chunk)
        output.close()
        
    return(ruta)


# Scrapea una variedad de café dada su URL
def scrap_coffe_variety(variety_URL, headers):
    # Hacemos la request y añadimos un retraso exponencial
    # para evitar satura el servidor de peticiones
    t1 = time.time()
    variety_page = requests.get(variety_URL, headers= headers)
    response_delay = time.time() - t1
    time.sleep(5 * response_delay)
    # Si la request es correcta se scrapea la web
    if variety_page.status_code == 200:
        variety_soup = BeautifulSoup(variety_page.content, "lxml")
        
        # Obtenemos el nombre y la descripción del café
        name = variety_soup.title.string
        coffee_name = name.split(' | ')[1]
        description = variety_soup.find('p').text
        # Creamos una lista con el nombre y la descripción del café
        variety = [coffee_name, description]
        
        # Obtenemos las propiedades de apariencia y algunas propiedades
        # agronómicas del café
        values = variety_soup.find_all('div',{'class':'value'})
        for v in values:
            clase = v.parent.get('class')
            # Para la propiedad altitude hay que navegar entre la estructura
            # anidada para obtener los 3 valores de la tabla
            if clase[1] == 'altitude':
                optimal = v.find_all('div',{'class':'altitude-range-value'})
                for i in optimal:
                    valor = i.text.replace('–','-').strip()
                    variety.append(valor)
            # Para el resto de propiedades se obtiene directamente el string
            else:
                valor = str(v.contents[0]).strip()
                variety.append(valor)
        
         # Obtenemos el resto de propiedades agronómicas y las propiedades
         # de genetics y availability
        values = variety_soup.find_all('td',{'class':'cell value'})
        for v in values:
            clase = v.parent.get('class')
            # Las propiedades agronomics y history tienen párrafos
            # y se extrae el texto
            if clase[1] == 'agronomics' or clase[1] == 'history':
                valor = v.text.strip()
            # Para el resto de propiedades se obtiene directamente el string
            else:
                valor = v.string.strip()
            # Se reemplazan los valores inexistentes y el caracter '—' por ''
            if valor == '—' or not(valor):
                valor = ''
            variety.append(valor)
            
    # Se devuelve la lista variety, que es una lista con todas
    # las propiedades extraidas de esta variedad de café
    return(variety)


# Scrapea todas las variedades de café dada la URL principal
def scrap_all_coffees(main_URL):
    
    # Crear lista vacía de cafes
    coffees = list()
    
    # Se define un header cambiando el User-Agent para no evidenciar que la 
    # petición viene de un script
    headers = {}
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;\
        q=0.9,image/webp,*/*;q=0.8"
    headers["Accept-Encoding"]= "gzip, deflate, sdch, br"
    headers["Accept-Language"]= "en-US,en;q=0.8"
    headers["Cache-Control"]= "no-cache"
    headers["dnt"]= "1"
    headers["Pragma"]= "no-cache"
    headers["Upgrade-Insecure-Requests"]= "1"
    headers["User-Agent"]= "Mozilla/5.0 (Windows NT 10.0; Win64; x64; \
        rv:82.0)Gecko/20100101 Firefox/82.0"
    # Se realiza la petición
    page = requests.get(main_URL, headers=headers)
    
    # Si la request es correcta se scrapea la web
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "lxml")
        # Bucle para encontrar las URL de cada una de las variedades
        for link in soup.find_all('a',href=True):
            aLink=link.get('href')
            # Si la URL corresponde a la de una variedad la scrapeamos con
            # la función scrap_coffe_variety y la añadimos a la lista coffees
            if ('varieties/' in aLink):
                coffee = scrap_coffe_variety(aLink, headers)
                # Se obtiene la URL de la imagen del café 
                image_link = link.find('img').get('src')
                # Mediante la función scrap_image se guarda la imagen
                # y se obtiene su ruta para añadirla a la lista coffee
                ruta = scrap_image(image_link, headers)
                coffee.append(ruta)
                coffees.append(coffee)
    return(coffees)


# Definimos la URL principal
main_URL = 'https://varieties.worldcoffeeresearch.org/varieties/'
# Definimos la URL raiz
root_URL = 'https://worldcoffeeresearch.org/'

# Mostrar por pantalla la tecnología con la que se ha creado la web
#tecnologia(root_URL)

# Mostrar por pantalla la información del propietario de la web
#propietario(root_URL)

# Crear una lista con todos los cafes scrapeados
print('Begining scraping, wait 7 minutes')
t0 = time.time()
coffees = scrap_all_coffees(main_URL)

# Creamos una lista con las columnas del dataset
columnas = ["Name", "Description", "Stature", "Leaf_tip_color", "Bean_size",
            "Optimal_Altitude_1", "Optimal_Altitude_2", "Optimal_Altitude_3",
            "Quality_potential", "Yield_potential", "Coffee_leaf_rust", "CBD",
            "Nematodes", "Year_First_Production", "Nutrition_Requirement",
            "Ripening_of_Fruit", "CTGB", "Planting_Density", "Additional",
            " Lineage", "Genetic Description", "History", "Breeder",
            "Intellectual_Property_Rights", "Image"]

# Crear un dataframe con la lista anterior y añadir colunmas
df = pd.DataFrame(coffees, columns=columnas)

# Exportar el dataframe a CSV en la ruta donde se encuentra este programa
ruta_actual = os.getcwd().replace("\\", "/")
ruta_csv = ruta_actual + '/coffee_varieties.csv'
df.to_csv(ruta_csv, sep=';', index=False)

# Termina el programa
print('Scraping finished')
response_delay = int(time.time() - t0)
print('The program has lasted for {} seconds '.format(response_delay))
