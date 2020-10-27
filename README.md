# Práctica 1: Web scraping coffee_varieties

## Descripción

Este trabajo se ha llevado a cabo dentro de la asignatura _Tipología y ciclo de vida de los datos_, perteneciente al Máster en Ciencia de Datos de la Universitat Oberta de Catalunya. En el mismo se aplican técnicas de _web scraping_ mediante el lenguaje de programación Python para extraer así datos de la web _worldcoffeeresearch_ y generar un _dataset_ sobre las variedades de café _arabica_.
El _dataset_ resultado proporciona información sobre la apariencia, información agronómica, genética y disponibilidad de cada variedad de café arábica. Las variables del conjunto de datos son útiles para identificar la idoneidad de determinada localización a las condiciones de crecimiento de cada variedad de café.

## Miembros del equipo

La actividad ha sido realizada por **Ivan García Jiménez** e **Itziar Ricondo Iriondo**.

## Ficheros del código fuente

* **src/main.py**: punto de entrada al programa. Inicia el proceso de scraping.
* **src/scraper.py**: contiene la implementación de la clase _AccidentsScraper_ cuyos métodos generan el conjunto de datos a partir de la base de datos online [PlaneCrashInfo](http://www.planecrashinfo.com/database.htm).
* **src/reason_classifier.py**: contiene la implementación de la clase que se encarga de asignar una causa a un resumen de accidente dado. Para ello, utiliza la librería *TextBlob*.

## Recursos

1. Lawson, R. (2015). _Web Scraping with Python_. Packt Publishing Ltd. Chapter 2. Scraping the Data.
2. Mitchel, R. (2015). _Web Scraping with Python: Collecting Data from the Modern Web_. O'Reilly Media, Inc. Chapter 1. Your First Web Scraper.
