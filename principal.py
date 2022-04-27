from Graficos import Grafico
from Modelado import Modelo
from Utils import Util
from tkinter import Tk, Button, LEFT, YES
from random import shuffle
from math import sqrt, pow

# Globales
CONTEO_POBLACION = 0
HISTORIA_GENERACIONES = []

def poda(sobrepoblacion, poblacion_inicial, poblacion_final):
  """Funcion simulando la poda para una nueva generacion.
  1. Juntamos la poblacion inicial con la población cruzada y mutada en un arreglo.
  2. Ordenamos la poblacion final por aptitud de manera descendente.
  3. Estimamos la sobrepoblacion y removemos de la poblacion a los menos aptos (peor fitness).
  4. Actualizamos el conteo de población.

  Args:
    sobrepoblacion (int): Residuo entre la poblacion actual y la poblacion maxima.
    poblacion_inicial (list): Población inicial de generación
    poblacion_final (list): Población luego de cruzarse y mutar.

  Returns:
      list: Nueva población para siguiente generación
  """
  global CONTEO_POBLACION
  poblacion_total = []
  poblacion_total.extend(poblacion_inicial)
  poblacion_total.extend(poblacion_final)
  poblacion_total = Util.ordenar_poblacion_por_fitness(poblacion_total, False)
  print(f"Soprepoblacion: {sobrepoblacion}") 
  [ poblacion_total.pop() for i in range(sobrepoblacion) ]
  CONTEO_POBLACION = len(poblacion_total)
  Util.imprimir_lista('Poblacion podada', poblacion_total)
  return poblacion_total

def mutacion(modelado, poblacion):
  """Funcion simulando la mutación de bits en un individuo.
  1. Realizamos la mutación.
  2. Guardamos información nueva de los individuos.
  3. Actualizamos conteo de población

  Args:
    modelado (class): Clase con el modelado del programa
    poblacion (list): Población a mutar

  Returns:
    list:  Lista con la población después de mutar.
  """
  global CONTEO_POBLACION
  poblacion_mutada = []
  for iterador in range(len(poblacion)):
    rango_objetivo_de_origen = (sqrt(pow((modelado.get_objetivo_x() - 0), 2) + pow((modelado.get_objetivo_y() - 0), 2)) / 2)
    vo_mutado = Util.realizar_mutacion(poblacion[iterador]['Vo'], rango_objetivo_de_origen)
    elevacion_mutado = Util.realizar_mutacion(poblacion[iterador]['Elevacion'], rango_objetivo_de_origen)
    azimuth_mutado = Util.realizar_mutacion(poblacion[iterador]['Azimuth'], rango_objetivo_de_origen)
    data_padre = {
      'ID': poblacion[iterador]['ID'],
      'Vo': vo_mutado,
      'Elevacion': elevacion_mutado,
      'Azimuth': azimuth_mutado
    }
    diccionario_mutacion = Util.inicializar_lista_mutacion(data_padre, iterador+1)
    poblacion_mutada.append(diccionario_mutacion)
    CONTEO_POBLACION += 1
  poblacion_mutada = Util.completar_informacion_poblacion(poblacion_mutada, modelado)
  Util.imprimir_lista('Poblacion mutada', poblacion_mutada)
  return poblacion_mutada

def cruza(modelado, poblacion):
  """Funcion simulando la cruza entre individuos.
  1. Clonamos la lista de población.
  2. Ordenamos aleatoriamente la lista shuffle().
  3. Realizamos cruza entre parejas y por cada genetica del individuo.
  4. Guardamos información nueva de los individuos.

  Args:
    modelado (class): Clase con el modelado del programa
    poblacion (list): Población a cruzar

  Returns:
    list: Lista con la población después de cruzar entre parejas aleatoriamente
  """
  clon_poblacion = poblacion[:]
  shuffle(clon_poblacion)
  poblacion_cruzada = []
  for i in range(0, len(clon_poblacion), 2):
    vo_cruzada_uno, vo_cruzada_dos = Util.realizar_cruza(clon_poblacion[i]['Vo'], clon_poblacion[i+1]['Vo'])
    elevacion_cruzada_uno, elevacion_cruzada_dos = Util.realizar_cruza(clon_poblacion[i]['Elevacion'], clon_poblacion[i+1]['Elevacion'])
    azimuth_cruzada_uno, azimuth_cruzada_dos = Util.realizar_cruza(clon_poblacion[i]['Azimuth'], clon_poblacion[i+1]['Azimuth'])
    padre_uno = {
      'ID': clon_poblacion[i]['ID'],
      'Vo': vo_cruzada_uno,
      'Elevacion': elevacion_cruzada_uno,
      'Azimuth': azimuth_cruzada_uno
    }
    padre_dos = {
      'ID': clon_poblacion[i+1]['ID'],
      'Vo': vo_cruzada_dos,
      'Elevacion': elevacion_cruzada_dos,
      'Azimuth': azimuth_cruzada_dos
    }
    diccionario_mutacion_uno, diccionario_mutacion_dos = Util.inicializar_lista_cruza(padre_uno, padre_dos)
    poblacion_cruzada.append(diccionario_mutacion_uno)
    poblacion_cruzada.append(diccionario_mutacion_dos)
  poblacion_cruzada = Util.completar_informacion_poblacion(poblacion_cruzada, modelado)
  Util.imprimir_lista('Poblacion cruzada', poblacion_cruzada)
  return poblacion_cruzada

def competencia(generacion, poblacion, modelado):
  """Funcion simulando la competencia entre individuos
  1. Completamos la información de los individuos.
  2. Recolectamos la información para la grafica.

  Args:
    generacion (int): Generacion en la que va el programa
    poblacion (list): Población por enviar a competencia
    modelado (class): Clase con el modelado del programa

  Returns:
    list: Lista con información completa de los individuos a competir
  """
  global DELTA_X
  global DELTA_Y
  global HISTORIA_GENERACIONES
  if poblacion[0]['Fitness'] == 0:
    poblacion = Util.completar_informacion_poblacion(poblacion, modelado)
  Util.imprimir_lista(f"Poblacion Gen: {generacion}", poblacion)
  diccionario_generacion = Util.coleccionar_historial(generacion, poblacion)
  HISTORIA_GENERACIONES.append(diccionario_generacion)
  Util.imprimir_lista(f"Mejores Resultados", HISTORIA_GENERACIONES)
  return poblacion

def clonacion(poblacion):
  global CONTEO_POBLACION
  """Funcion simulando la clonacion del ultimo individuo si la población fuese impar

  Args:
    poblacion (list): Lista de población

  Returns:
    list: Población modificada con un clon
  """
  poblacion.append(poblacion[-1])
  CONTEO_POBLACION += 1
  return poblacion

def iniciar_algoritmo(modelado):
  """Funcion para preparar y inicializar el algoritmo

  Args:
    modelado (class): Clase que almacena el modelado del algoritmo

  Procesos:
    - Definir cuantos bits se usaran
    - Generar poblacion inicial
    - Iteracion por generaciones
    - Llamar a los procesos evolutivos (clonacion, competencia, cruza, mutacion, poda)
    - Llamar a funcion de graficar
  """
  global DELTA_X
  global DELTA_Y
  global CONTEO_POBLACION
  global HISTORIA_GENERACIONES
  bandera = 1.0
  contador_generaciones = 0
  print('==== Starting ====')
  poblacion, CONTEO_POBLACION = Util.inicializar(modelado.get_poblacion_inicial())
  while bandera > 0.6 and contador_generaciones < 50:
    if len(poblacion) % 2 != 0:
      poblacion = clonacion(poblacion)
    individuos_competencia = competencia(contador_generaciones, poblacion, modelado)
    bandera = Util.obtener_fitness_minimo(individuos_competencia)
    print(f"Bandera de impacto: {bandera}")
    individuos_cruzados = cruza(modelado, individuos_competencia)
    individuos_mutados = mutacion(modelado, individuos_cruzados)
    if CONTEO_POBLACION > modelado.get_poblacion_maxima():
      sobrepoblacion = CONTEO_POBLACION - modelado.get_poblacion_maxima()
      poblacion = poda(sobrepoblacion, individuos_competencia, individuos_mutados)
    contador_generaciones += 1
  generaciones, maxs, mins, avgs = Util.split_informacion_grafica(HISTORIA_GENERACIONES)
  Grafico.graficar_evolucion(generaciones, maxs, mins, avgs)

def cargar_configuracion(inputs):
  """Funcion encargada de guardar el modelado del algoritmo

  Args:
    inputs (list): Campos solicitados en el formulario inicial.
  """
  configuracion = {
    'pob_ini': int(inputs["Población inicial"].get()),
    'pob_max': int(inputs["Población máxima"].get()),
    'objetivo_x': float(inputs["Posicion objetivo X"].get()),
    'objetivo_y': float(inputs["Posicion objetivo Y"].get()),
  }
  modelado = Modelo(configuracion)
  iniciar_algoritmo(modelado)

if __name__ == '__main__':
  """Funcion main para crear la ventana inicial.
  """
  ventana = Tk()
  ventana.title("Tiro al blanco - IA")
  ventana.resizable(0,0)
  entries = Grafico.crear_formulario(ventana)
  btn1 = Button(ventana, text = 'Iniciar',
    command=(lambda e=entries: cargar_configuracion(e)), bg="green",fg='white')
  btn1.pack(side = LEFT, pady = 5, expand = YES)
  btn2 = Button(ventana, text = 'Quitar', command = ventana.quit, bg="red",fg='white')
  btn2.pack(side = LEFT, pady = 5, expand = YES)
  ventana.mainloop()