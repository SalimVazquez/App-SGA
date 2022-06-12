from tkinter import Frame, Entry, Label, TOP, RIGHT, LEFT, YES, messagebox
from matplotlib import pyplot as plt
from numpy import arange

PARAMETROS = (
  'Población inicial',
  'Población máxima',
  'Posicion objetivo X',
  'Posicion objetivo Y',
)

class Grafico:

  @staticmethod
  def mostrar_alerta(tipo, mensaje):
    if tipo == 'Info':
      messagebox.showinfo('Información', mensaje)
    elif tipo == 'Warning':
      messagebox.showwarning('Warning', mensaje)
    else:
      messagebox.showerror('Error', mensaje)

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
    plt.plot(generaciones, maxs, markerfacecolor='blue', markersize=6, color='yellowgreen', linewidth=3, label='Maximos')
    plt.plot(generaciones, mins, markerfacecolor='blue', markersize=6, color='skyblue', linewidth=3, label='Peores')
    plt.plot(generaciones, avgs, markerfacecolor='blue', markersize=6, color='orangered', linewidth=3, label='Promedio')
    plt.subplots_adjust(right=0.815)
    plt.title('Evolución de la aptitud')
    plt.ylabel('Aptitud')
    plt.xticks(arange(1, max(generaciones)+1, step=1))
    plt.xlabel('Generaciones')
    plt.legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0.)
    plt.show()

  @staticmethod
  def graficar_impacto(puntos_x, puntos_y, obj_x, obj_y, poblacion):
    for i in range(5):
      plt.plot(puntos_x, puntos_y, label=f"VO: {poblacion[i]['Vo']}, Elevacion: {poblacion[i]['Elevacion']}, Azimuth: {poblacion[i]['Azimuth']}")
    plt.legend(loc='upper left')
    plt.title("Movimiento Parabólico")
    plt.xlabel("Posición horizontal(m)")
    plt.ylabel("Altura (m)")

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for iterador in range(5):
      plt.scatter(poblacion[iterador]['Fenotipo X'], poblacion[iterador]['Fenotipo Y'], s=100, marker='o', label=f"Impacto: ({poblacion[iterador]['Fenotipo X']},{poblacion[iterador]['Fenotipo Y']})")
    plt.scatter(obj_x, obj_y, s=100, marker ='^', c='yellow', edgecolors='red', label=f"Objetivo ({obj_x, obj_y})")
    plt.scatter(0, 0, s=100, marker ='s', c='purple', edgecolors='green', label=f"Cañon (0,0)")
    left,right = ax.get_xlim()
    low,high = ax.get_ylim()
    plt.arrow(left, 0, right -left, 0, length_includes_head=True, head_width=0.15)
    plt.arrow(0, low, 0, high-low, length_includes_head=True, head_width=0.15)
    plt.grid()
    plt.legend(loc='upper left')
    plt.title("Plano cartesiano de impactos")
    plt.xlabel("Posición horizontal(m)")
    plt.ylabel("Altura (m)")
    plt.show()