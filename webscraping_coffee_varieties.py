import requests
from bs4 import BeautifulSoup
import builtwith
import whois
import pandas as pd


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


# Scrapea una variedad de café dada su URL
def scrap_coffe_variety(variety_URL):
    variety_page = requests.get(variety_URL)
    # Si la request es correcta se scrapea la web
    if variety_page.status_code == 200:
        variety_soup = BeautifulSoup(variety_page.content)
        
        # Obtenemos el nombre y la descripción del café
        name = variety_soup.title.string
        coffee_name = name.split(' | ')[1]
        description = variety_soup.find('p').string
        
        # Creamos una lista con el nombre y la descripción del café
        variety = [coffee_name, description]
        
        # Listamos las propiedades del café
        properties = variety_soup.find_all('h5')
        n_prop = len(properties)
        
        # Creamos un bucle que recorre las propiedades del café
        for p in range(n_prop):
            # Para la tercera propiedad hay que hacer algo diferente
            if p != 3 and p < 9:
                prop = properties[p]
                # El valor de la propiedad es el hermano del hermano
                hermano = prop.next_sibling.next_sibling
                # Transformar el valor a string y quitar los espacios laterales
                v_propiedad = str(hermano.contents[0]).strip()
                # Añadir propiedad la lista varieties
                variety.append(v_propiedad)
            
    return(variety)


# Scrapea todas las variedades de café dada la URL principal
def scrap_all_coffees(main_URL):
    
    # Crear lista vacía de cafes
    coffees = list()
    page = requests.get(main_URL)
    
    # Si la request es correcta se scrapea la web
    if page.status_code == 200:
        soup = BeautifulSoup(page.content)
        n_coffee = 0
        # Bucle para encontrar las URL de cada una de las variedades
        for link in soup.find_all('a',href=True):
            aLink=link.get('href')
            #print(aLink) aquí hay informaciones interesantes
            # Si la URL corresponde a la de una variedad la scrapeamos con
            # la función scrap_coffe_variety y la añadimos a la lista coffees
            if ('varieties/' in aLink):
                coffees.append(scrap_coffe_variety(aLink))
                n_coffee = n_coffee + 1
                print('{} coffee scraped'.format(n_coffee))

    return(coffees)


# Definimos la URL principal
main_URL = 'https://varieties.worldcoffeeresearch.org/varieties/'

# Definimos la URL raiz
root_URL = 'https://worldcoffeeresearch.org/'

# Mostrar por pantalla la tecnologia con la que se ha creado la web
#tecnologia(root_URL)

# Mostrar por pantalla la información del propietario de la web
#propietario(root_URL)

# Crear una lista con todos los cafes scrapeados
coffees = scrap_all_coffees(main_URL)

# Crear un dataframe con la lista anterior y añadir colunmas
df = pd.DataFrame(coffees, columns=["Name", "Description", "Stature",
                                    "Leaf_tip_color", "Bean_size",
                                    "Quality_potential","Yield_potential",
                                    "Coffee_leaf_rust", "CBD", "Nematodes"])

# Mostrar por pantalla la cabecera del dataframe
print(df.head())

# Expertar el dataframe a CSV
ruta = 'C:/Users/96gar/Desktop/coffee_varieties.csv'
df.to_csv(ruta, sep=';', index=False)
