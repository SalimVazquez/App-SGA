from tkinter import Frame, Entry, Label, TOP, RIGHT, LEFT, YES
from matplotlib import pyplot as plt
from numpy import arange
from math import cos, sin, radians

PARAMETROS = (
  'Población inicial',
  'Población máxima',
  'Posicion objetivo X',
  'Posicion objetivo Y',
)

class Grafico:

  @staticmethod
  def crear_formulario(ventana):
    """Funcion para crear el formulario dentro de la ventana de Tkinter

    Args:
      ventana (Tkinter): Ventana de Tkinter

    Returns:
      entries (list): Campos a solicitar
    """
    title = Label(ventana, text="Modelación", width=20)
    title.pack()
    entries = {}
    for parametro in PARAMETROS:
      cuerpo_ventana = Frame(ventana)
      label = Label(cuerpo_ventana, width=30, text=f"{parametro}: ", anchor="w")
      inputs = Entry(cuerpo_ventana)
      cuerpo_ventana.pack(side=TOP, fill="both", padx=5, pady=5)
      label.pack(side=LEFT)
      inputs.pack(side=RIGHT, expand=YES, fill="both")
      entries[parametro] = inputs
    return entries

  @staticmethod
  def graficar_evolucion(generaciones, maxs, mins, avgs):
    """Funcion para mostrar la evolucion de aptitud en una grafica.
    1. Las generaciones transcurridas seran el eje X.
    2. Aptitud máxima, minima y promedio seran el eje Y.

    Args:
      generaciones (list): Lista que incluye las iteraciones realizadas.
      maxs (list): Lista que incluye las mejores aptitudes.
      mins (list): Lista que incluye las peores aptitudes.
      avgs (list): Lista que incluye el promedio de aptitudes.
    """
    plt.plot(generaciones, maxs, markerfacecolor='blue', markersize=6, color='skyblue', linewidth=3, label='Maximos')
    plt.plot(generaciones, mins, markerfacecolor='blue', markersize=6, color='yellowgreen', linewidth=3, label='Peores')
    plt.plot(generaciones, avgs, markerfacecolor='blue', markersize=6, color='orangered', linewidth=3, label='Promedio')
    plt.subplots_adjust(right=0.815)
    plt.title('Evolución de la aptitud')
    plt.ylabel('Aptitud')
    plt.xticks(arange(1, max(generaciones)+1, step=1))
    plt.xlabel('Generaciones')
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0.)
    plt.show()