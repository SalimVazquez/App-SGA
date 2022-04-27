# Tiro al blanco
Algoritmo tipo evolutivo y realiza un procedimiento de optimización inspirado en la teoría biológica de los genotipos o individuos, o soluciones potenciales más aptos que se utilizarán en la creación de los descendientes.

Se usan procesos como lo son: **Cruza, Mutación, Clonación**. Así como también una **Selección** de acuerdo con algún criterio a satisfacer (maximizar o minimizar), en función del cual se decide cuáles son los individuos más adaptados, y cuáles los menos aptos.

### Requerimientos
```
Python >= 3.8
Tkinter >= 8.6
Numpy >= 1.19.5
Matplotlib >= 3.3.4
```
De igual forma se anexo un txt con los plugins necesarios, puede instarlos con `pip install -r requerimientos.txt`.
Luego de esto, ejecuta `principal.py`.

### Criterio de aceptación
Dada la posición de un objetivo fijo y un cañón que lanza balas en un mundo 2D **determinar cual debe ser la configuración del cañón**, para acertar el impacto al objetivo.

Considerando que el tiro parabólico está afectado por ruido (viento).

En esta problematica se presenta la opción de minimizar, lo que indica que nuestros mejores individuos serán los que tengan el puntaje más bajo en el **Fitness**.
___
Esta es una aplicación de algoritmos geneticos, con base a una [actividad previa](https://github.com/SvS30/SGA).