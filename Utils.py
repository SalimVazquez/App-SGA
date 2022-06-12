from math import cos, sin, radians, sqrt
from random import uniform

class Util:

  @staticmethod
  def data_parabola(poblacion):
    puntos_X, puntos_Y = [], []
    avance_tiempo = 0.01
    gravedad = 9.81
    for i in range(5):
      tiempo = 0
      x = 0
      y = 0
      vx = poblacion[i]['Vo'] * cos(radians(poblacion[i]['Elevacion']))
      vy = poblacion[i]['Vo'] * sin(radians(poblacion[i]['Elevacion']))
      puntos_X.clear()
      puntos_Y.clear()

      while y>=-0.01:
        tiempo = tiempo + avance_tiempo
        x = x + vx * tiempo
        y = y + vy * tiempo - gravedad * tiempo ** 2
        puntos_X.append(x)
        puntos_Y.append(y)
    return puntos_X, puntos_Y

  @staticmethod
  def split_informacion_grafica(data_grafica):
    """Funcion para preparar la información a graficar.

    Args:
      data_grafica (list): Lista con la información de HISTORIA_GENERACIONES.

    Returns:
      generaciones, maxs, mins, avgs (list): Listas con la información separada por generaciones, aptitudes maximas, aptitudes minimas y promedio de aptitudes.
    """
    generaciones = []
    maxs = []
    mins = []
    avgs = []
    for i in range(len(data_grafica)):
      generaciones.append(i+1)
      maxs.append(data_grafica[i]['Fitness-Max'])
      mins.append(data_grafica[i]['Fitness-Min'])
      avgs.append(data_grafica[i]['Fitness-Prom'])
    return generaciones, maxs, mins, avgs

  @staticmethod
  def inicializar_lista_mutacion(data_padre, id):
    """Funcion para recolectar la información de individuos en mutación.

    Args:
      data_padre (dict): Informacion del individuo padre.
      id (int): ID del individuo.

    Returns:
      diccionario_mutacion (dict): Diccionario con información del individuo mutado.
    """
    diccionario_mutacion = {
      'ID': f"{data_padre['ID']}-{id}",
      'Vo': data_padre['Vo'],
      'Elevacion': data_padre['Elevacion'],
      'Azimuth': data_padre['Azimuth'],
      'Rango': 0,
      'Fenotipo X': 0,
      'Fenotipo Y': 0,
      'Fitness': 0,
    }
    return diccionario_mutacion

  @staticmethod
  def realizar_mutacion(genetica_a_mutar, rango_objetivo):
    """Funcion encargada de realizar la mutación.
    1. Generamos un número aleatorio.
    2. Evaluamos la función

    Func:
      result = genetica_a_mutar + y * R
      - y: numero aleatorio entre (-1,1)
      - R: rango_objetivo/2

    Args:
      genetica_a_mutar (float): Genetica del individuo que mutara.
      rango_objetivo (float): Distancia del origen al objetivo.

    Returns:
      (str): Genetica evaluada en la funcion.
    """
    return round(genetica_a_mutar + (uniform(-1,1) * rango_objetivo),2)

  @staticmethod
  def inicializar_lista_cruza(data_padre_uno, data_padre_dos):
    """Funcion para recolectar la información de individuos en cruza.

    Args:
      data_padre_uno (dict): Información del padre 1
      data_padre_dos (dict): Información padre 2.

    Returns:
      (dict): Diccionarios de los individuos en cruza.
    """
    diccionario_cruza_uno = {
      'ID': data_padre_uno['ID'],
      'Vo': data_padre_uno['Vo'],
      'Elevacion': data_padre_uno['Elevacion'],
      'Azimuth': data_padre_uno['Azimuth'],
      'Rango': 0,
      'Fenotipo X': 0,
      'Fenotipo Y': 0,
      'Fitness': 0,
    }
    diccionario_cruza_dos = {
      'ID': data_padre_dos['ID'],
      'Vo': data_padre_dos['Vo'],
      'Elevacion': data_padre_dos['Elevacion'],
      'Azimuth': data_padre_dos['Azimuth'],
      'Rango': 0,
      'Fenotipo X': 0,
      'Fenotipo Y': 0,
      'Fitness': 0,
    }
    return diccionario_cruza_uno, diccionario_cruza_dos

  @staticmethod
  def realizar_cruza(genetica_uno, genetica_dos):
    """Funcion encargada de realizar la cruza.
    1. Recibimos la genetica del individuo y usamos la funcion de cruza.

    Func:
      result = a * genetica_padre_uno + (1-a) * genetica_padre_dos
        - a: numero aleatorio entre (0,1)

    Args:
      genetica_uno (float): Genetica del padre uno.
      genetica_dos (float): Genetica del padre dos.

    Returns:
      bits_cruzados_uno (str): bits resultanes de la cruza entre padre 1 y resto de padre 2.
      bits_cruzados_dos (str): bits resultanes de la cruza entre padre 2 y resto de padre 1.
    """
    numero_aleatorio = uniform(0,1)
    genetica_resultado_uno = numero_aleatorio * genetica_uno + (1-numero_aleatorio) * genetica_dos
    genetica_resultado_dos = numero_aleatorio * genetica_dos + (1-numero_aleatorio) * genetica_uno
    return round(genetica_resultado_uno,2), round(genetica_resultado_dos,2)

  def key_to_sort(lista):
    """Funcion usada para la key de ordenación.

    Args:
      lista (list): Población actual.

    Returns:
      lista['Fitness']: Key para ordenación de población.
    """
    return lista['Fitness']

  @staticmethod
  def ordenar_poblacion_por_fitness(poblacion, orden):
    """Funcion para ordenar la población por fitness y recuperar la población.

    Args:
      poblacion (list): Población actual.

    Returns:
      poblacion (list): Población ordenada por fitness.
    """
    poblacion.sort(key=Util.key_to_sort, reverse=orden)
    return poblacion

  def obtener_fitness_minimo(poblacion):
    """Funcion para ordenar la población por fitness ascendente y recuperar la minima de la población.

    Args:
      poblacion (list): Población actual.

    Returns:
      poblacion[0]['Fitness'] (float): Fitness minima de la población.
    """
    poblacion.sort(key=Util.key_to_sort)
    return poblacion[0]['Fitness']

  def obtener_fitness_maximo(poblacion):
    """Funcion para ordenar la población por fitness de manera descendente y recuperar la maxima de la población.

    Args:
      poblacion (list): Población actual.

    Returns:
      poblacion[0]['Fitness'] (float): Fitness máximo de la población.
    """
    poblacion.sort(key=Util.key_to_sort, reverse=True)
    return poblacion[0]['Fitness']

  @staticmethod
  def obtener_registro_fitness(poblacion):
    """Funcion principal para obtener la fitness minima y máxima de la población.

    Args:
      poblacion (list): Población actual.

    Returns:
      fitness_min (float): Fitness minima de la población.
      fitness_max (float): Fitness máxima de la población.
    """
    clon_poblacion = poblacion[:]
    fitness_min = Util.obtener_fitness_minimo(clon_poblacion)
    fitness_max = Util.obtener_fitness_maximo(clon_poblacion)
    return fitness_min, fitness_max

  @staticmethod
  def calcular_fitness(objetivo_x, objetivo_y, individuo_x, individuo_y):
    """Funcion para calcular la aptitud de cada individuo.

    Args:
      objetivo_x (float): Coordenada X del objetivo.
      objetivo_y (float): Coordenada Y del objetivo.
      individuo_x (float): Fenotipo X del individuo.
      individuo_y (float): Fenotipo Y del individuo.

    Returns:
      (double): Aptitud del individuo, ingresando los fenotipos en la función dada.
    """
    return sqrt(pow((objetivo_x-individuo_x),2) + pow((objetivo_y-individuo_y),2))

  @staticmethod
  def coordenadas_polares_a_cartesianas(coordenada, rango, tetha):
    """Funcion para convertir coordenadas polares a cartesianas

    Args:
      coordenada (str): Etiqueta para determinar que función usar
      rango (float): Rango de proyectil
      theta (float): Angulo de azimuth del individuo

    Returns:
      (float): fenotipo del individuo.
    """
    angulo = (cos(radians(tetha)) if coordenada == 'X' else sin(radians(tetha)))
    return rango * angulo

  @staticmethod
  def obtener_rango_proyectil(velocidad_inicial, tetha):
    """Funcion para calcular el rango que obtendra el proyectil

    Args:
      velocidad_inicial (float): Velocidad inicial con la que sale el proyectil
      tetha (float): Angular de elevación del cañon

    Returns:
      (float): Rango del proyectil
    """
    GRAVEDAD = 9.81
    return (pow(velocidad_inicial, 2) * sin(radians((2*tetha))) / GRAVEDAD)

  @staticmethod
  def coleccionar_historial(generacion, poblacion):
    """Funcion encargada de recolectar la información para la grafica final.
    1. Obtenemos el fitness minimo y máximo de la generación.
    2. Obtenemos la suma de los fitness y obtenemos el promedio.

    Args:
      generacion (int): Generación actual.
      poblacion (list): Lista con la población actual.

    Returns:
      (dict): Diccionario que almacena los datos para graficar.
    """
    fitness_min, fitness_max = Util.obtener_registro_fitness(poblacion)
    suma_fitness = sum([ poblacion[i]['Fitness'] for i in range(len(poblacion)) ])
    prom_fitness = suma_fitness / len(poblacion)
    return {
      'Gen': generacion,
      'Fitness-Max': fitness_min,
      'Fitness-Min': fitness_max,
      'Fitness-Prom': prom_fitness
    }

  @staticmethod
  def completar_informacion_poblacion(poblacion, modelado):
    """Funcion encargada de completar la información de cada individuo de la población 0.
    1. Calculamos el rango del proyectil.
    2. Calculamos el fenotipo X.
    3. Calculamos el fenotipo Y.
    4. Calculamos fitness.

    Args:
      poblacion (list): Lista con la población 0.
      modelado (class): Clase con la configuración del algoritmo.

    Returns:
      poblacion (list): Lista de la población 0 con la información completa.
    """
    for iterador in range(len(poblacion)):
      poblacion[iterador]['Rango'] = round(Util.obtener_rango_proyectil(poblacion[iterador]['Vo'], poblacion[iterador]['Elevacion']),2)
      poblacion[iterador]['Fenotipo X'] = round(Util.coordenadas_polares_a_cartesianas('X', poblacion[iterador]['Rango'], poblacion[iterador]['Azimuth']),2)
      poblacion[iterador]['Fenotipo Y'] = round(Util.coordenadas_polares_a_cartesianas('Y', poblacion[iterador]['Rango'], poblacion[iterador]['Azimuth']),2)
      poblacion[iterador]['Fitness'] = round(Util.calcular_fitness(modelado.get_objetivo_x(), modelado.get_objetivo_y(), poblacion[iterador]['Fenotipo X'], poblacion[iterador]['Fenotipo Y']),2)
    return poblacion

  @staticmethod
  def imprimir_lista( name, lista ):
    """Funcion para imprimir por consola alguna lista

    Args:
      name (string): Nombre de la lista a imprimir
      list (lista): Lista que se imprimira
    """
    print(f"==== Lista: {name}  ====")
    for i in range(len(lista)):
      print(lista[i])
    print('==== End Lista ====')

  @staticmethod
  def inicializar(poblacion_inicial):
    """Funcion para generar la población 0 del sistema.
    1. Generar bits de manera aleatoria.
    2. Generar un diccionario con la información relevante de los individuos y guardar en una lista.
    3. Actualizar conteo de población.

    Args:
      poblacion_inicial (int): Parametro en formulario.

    Returns:
      individuos (list): Lista de la población 0.
      conteo_poblacion (int): Conteo de la población.
    """
    conteo_poblacion = 0
    individuos = []
    for iterator in range(poblacion_inicial):
      diccionario_poblacion = {
        'ID': iterator +1,
        'Vo': round(uniform(0,100),2),
        'Elevacion': round(uniform(0,90),2),
        'Azimuth': round(uniform(0,360),2),
        'Rango': 0,
        'Fenotipo X': 0,
        'Fenotipo Y': 0,
        'Fitness': 0,
      }
      individuos.append(diccionario_poblacion)
      conteo_poblacion += 1
    return individuos, conteo_poblacion