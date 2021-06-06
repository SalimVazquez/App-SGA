## Aplicación de Algoritmos genéticos - Tiro al blanco
Dada la posición de un objeto fijo y un cañón lanza balas en un mundo 2D.
Tomando en cuenta la distancia del objeto al punto donde cae la bala. **determinar cual debe ser la configuración del cañón**

Considerar que el tiro parabólico está afectado por ruido (viento)

### Criterio de aceptación
En esta problematica se presenta la opción de minimizar, lo que indica que nuestros mejores individuos serán los que tengan el puntaje más bajo en el Fitness (calcular distancia de impacto al objetivo).

### Requerimientos
```
Python >= 3.6
Tkinter >= 8.6
Numpy >= 1.19.5
Matplotlib >= 3.3.4
```

### Configuración cañon
- [Azimuth: \alpha (Orientación del cañon)](https://www.photopills.com/es/articulos/entendiendo-el-azimut-la-elevacion)
- [Elevación: \Theta (Angulo vertical)](https://www.photopills.com/es/articulos/entendiendo-el-azimut-la-elevacion)
- Velocidad inicial: Vo

### Ecuaciones
- Alcance máximo
	xMax = Vo² &bull; sin(2&bull;\Theta) / g

- Convertir coordenada polar a cartesiana
	- X: xMax &bull; cos(\alpha)
	- Y: xMax &bull; sen(\alpha)

- Distancia entre 2 puntos
	- fitness: \surd(X<sub>2</sub>-X<sub>1</sub>)² + (Y<sub>2</sub>-Y<sub>1</sub>)²

- Cruza
	- a&bull;p1 + (1-a)&bull;p2
		- a: numero aleatorio entre (0,1)
		- p1: gen individuo 1
		- p2: gen individuo 2

- Mutación
	- h1 + y&bull;R
		- h1: gen individuo
		- y: numero aleatorio entre (-1,1)
		- R: rango/2