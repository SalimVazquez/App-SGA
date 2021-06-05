import tkinter
from tkinter import *
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plot
import random
import math
# import scipy.stats as ss

root = Tk()
lSelection = []
lCross = []
lMutation = []
lTop = []
lGen = []
countPob = 0
countGen = 0
grav = 9.81
rangobj = 0

fields = (
    'Población inicial',
    'Población máxima',
    'Posición objetivo X', 
    'Posición objetivo Y',
    'Velocidad del viento',
)

def printList(list):
    for i in range(len(list)):
        print(list[i])

# convert polar coordinates to cartesians
def polarToCartesianX(vMax, tetha):
    x = vMax * math.cos(tetha)
    return x

def polarToCartesianY(vMax, tetha):
    y = vMax * math.sin(tetha)
    return y

# The horizontal range of each of the projectiles
def rangeProjectils(Vo, tetha):
    global grav
    # Vo² * sin(θ) / g
    vMax = (math.pow(Vo,2) * math.sin((2*tetha)) / grav)
    return vMax

# distance between 2 points
def calculateFitness(X2, Y2, X1, Y1):
    # global rangobj
    # sqrt((x2 - x1)^2 + (y2 - y1)^2)
    fitness = math.sqrt(math.pow((X2-X1),2) + math.pow((Y2-Y1), 2))
    # noise affecting the shot
    # Normal distribution
    # Sr = rangobj*0.1
    # X = ss.norm(0,Sr)
    # y = random.uniform((-3*Sr), (3*Sr)) # entre -3Sr,+3Sr
    # noise = X.ppf(y)
    noise = 0
    fitness = fitness - noise
    return fitness

def poda(ite):
    global lSelection
    global lGen
    global countPob
    auxGen = lGen
    auxGen = sorted(auxGen, key=lambda x: x['fitB'])
    lSelection.clear()
    for i in range(ite):
        if auxGen[i]['fitP'] < auxGen[i]['fitH']:
            dictSel = {'ID':i+1, 'Vo': auxGen[i]['VoP'], 'Ele': auxGen[i]['EleP'], 'Az': auxGen[i]['AzP'], 'R': 0, 'X': 0, 'Y': 0, 'Fitness': 0, 'Prob': 0, 'Count': 0}
        else:
            dictSel = {'ID':i+1, 'Vo': auxGen[i]['VoH'], 'Ele': auxGen[i]['EleH'], 'Az': auxGen[i]['AzH'], 'R': 0, 'X': 0, 'Y': 0, 'Fitness': 0, 'Prob': 0, 'Count': 0}
        lSelection.append(dictSel)
        countPob += 1
    for i in range(2, len(auxGen)):
        dictSel = {'ID':i+1, 'Vo': auxGen[i]['VoH'], 'Ele': auxGen[i]['EleH'], 'Az': auxGen[i]['AzH'], 'R': 0, 'X': 0, 'Y': 0, 'Fitness': 0, 'Prob': 0, 'Count': 0}
        lSelection.append(dictSel)
    print('------------------ Poda ------------------')
    printList(lGen)
    lGen.clear()

def cleanLists():
    global lSelection
    global lCross
    global lMutation
    global countPob
    lSelection.clear()
    lCross.clear()
    lMutation.clear()
    countPob = 0

def mutation(inp):
    # h = h1 + y*R
	# 	- y: numero aleatorio entre (-1,1)
	# 	- R: rango/2
    global lMutation
    global lGen
    global rangobj
    for i in range(len(lMutation)):
        yVo = random.uniform(-1,1)
        lMutation[i]['VoH'] = lMutation[i]['Vo'] + yVo * (rangobj/2)
        yTetha = random.uniform(-1,1)
        lMutation[i]['EleH'] = lMutation[i]['Ele'] + yTetha * (rangobj/2)
        yAz = random.uniform(-1,1)
        lMutation[i]['AzH'] = lMutation[i]['Az'] + yAz * (rangobj/2)
    for i in range(len(lMutation)):
        lMutation[i]['Rh'] = round(rangeProjectils(lMutation[i]['VoH'], lMutation[i]['EleH']),2)
        lMutation[i]['Xh'] = round(polarToCartesianX(lMutation[i]['Rh'], lMutation[i]['AzH']),2)
        lMutation[i]['Yh'] = round(polarToCartesianY(lMutation[i]['Rh'], lMutation[i]['AzH']),2)
        lMutation[i]['FitH'] = round(calculateFitness(float(inp['Posición objetivo X'].get()), float(inp['Posición objetivo Y'].get()), lMutation[i]['Xh'], lMutation[i]['Yh']),4)
        lGen[i]['VoH'] = lMutation[i]['VoH']
        lGen[i]['EleH'] = lMutation[i]['EleH']
        lGen[i]['AzH'] = lMutation[i]['AzH']
        lGen[i]['fitH'] = lMutation[i]['FitH']
        if lGen[i]['fitH'] < lGen[i]['fitP']:
            lGen[i]['VoB'] = lGen[i]['VoH']
            lGen[i]['EleB'] = lGen[i]['EleH']
            lGen[i]['AzB'] = lGen[i]['AzH']
            lGen[i]['fitB'] = lGen[i]['fitH']
        else:
            lGen[i]['VoB'] = lGen[i]['VoP']
            lGen[i]['EleB'] = lGen[i]['EleP']
            lGen[i]['AzB'] = lGen[i]['AzP']
            lGen[i]['fitB'] = lGen[i]['fitP']
    printList(lMutation)
    cleanLists()
    poda(2)

def cross(inp):
    # h = a*p1 + (1-a) * p2
    #   - a: numero aleatorio entre (0,1)
    global lCross
    global lMutation
    position = 0
    for i in range(0, len(lCross), 2):
        auxVo1 = lCross[i]['VoP']
        auxVo2 = lCross[i+1]['VoP']
        aVo = random.uniform(0,1)
        lCross[i]['Vo'] = aVo*auxVo1 + (1-aVo) * auxVo2
        lCross[i+1]['Vo'] = aVo*auxVo2 + (1-aVo) * auxVo1
        auxTetha1 = lCross[i]['EleP']
        auxTetha2 = lCross[i+1]['EleP']
        aEle = random.uniform(0,1)
        lCross[i]['Ele'] = aEle*auxTetha1 + (1-aEle) * auxTetha2
        lCross[i+1]['Ele'] = aEle*auxTetha2 + (1-aEle) * auxTetha1
        auxAz1 = lCross[i]['AzP']
        auxAz2 = lCross[i+1]['AzP']
        aZ = random.uniform(0,1)
        lCross[i]['Az'] = aZ*auxAz1 + (1-aZ) * auxAz2
        lCross[i+1]['Az'] = aZ*auxAz2 + (1-aZ) * auxAz1
    for i in range(len(lCross)):
        lCross[i]['R'] = round(rangeProjectils(lCross[i]['Vo'], lCross[i]['Ele']), 2)
        lCross[i]['X'] = round(polarToCartesianX(lCross[i]['R'], lCross[i]['Az']),2)
        lCross[i]['Y'] = round(polarToCartesianY(lCross[i]['R'], lCross[i]['Az']),2)
        lCross[i]['Fit'] = round(calculateFitness(float(inp['Posición objetivo X'].get()), float(inp['Posición objetivo Y'].get()), lCross[i]['X'], lCross[i]['Y']),4)
        dictMut = {'ID': position+1, 'Vo': lCross[i]['Vo'], 'Ele': lCross[i]['Ele'], 'Az':  lCross[i]['Az'], 'VoH': 0, 'EleH': 0, 'AzH': 0, 'Rh': 0, 'Xh': 0, 'Yh': 0, 'FitH': 0}
        lMutation.append(dictMut)
        position += 1
    printList(lCross)

def selection():
    global lSelection
    global lCross
    global lGen
    position = 0
    for i in range(len(lSelection)):
        if lSelection[i]['Count'] != 0:
            for j in range(lSelection[i]['Count']):
                dictCross = {'ID':position+1, 'VoP': lSelection[i]['Vo'], 'EleP': lSelection[i]['Ele'], 'AzP': lSelection[i]['Az'], 'Vo': 0, 'Ele': 0, 'Az': 0, 'R': 0, 'X': 0, 'Y': 0, 'Fit': 0}
                lCross.append(dictCross)
                dictGen = {'ID': position+1, 'VoP': lSelection[i]['Vo'], 'EleP': lSelection[i]['Ele'], 'AzP': lSelection[i]['Az'], 'fitP': lSelection[i]['Fitness'], 'VoH': 0, 'EleH': 0, 'AzH': 0, 'fitH': 0, 'VoB': 0, 'EleB': 0, 'AzB': 0, 'fitB': 0}
                lGen.append(dictGen)
                position += 1

def getFitnessMaxSelec():
    global lSelection
    best = 0
    position = 0
    for i in range(len(lSelection)):
        if i == 0:
            best = lSelection[i]['Fitness']
        else:
            if best > lSelection[i]['Fitness']:
                best = lSelection[i]['Fitness']
                position = i
    return position

def getProbAcu(limit):
    global lSelection
    a = 0
    for i in range(0, limit, 1):
        a += lSelection[i]['Prob']
    return a

def evaluation(inp):
    global lSelection
    global lTop
    global countPob
    global countGen
    count = 0
    totFitness = 0
    promFitness = 0
    for i in range(len(lSelection)):
        lSelection[i]['R'] = round(rangeProjectils(lSelection[i]['Vo'], lSelection[i]['Ele']), 2)
        lSelection[i]['X'] = round(polarToCartesianX(lSelection[i]['R'], lSelection[i]['Az']),2)
        lSelection[i]['Y'] = round(polarToCartesianY(lSelection[i]['R'], lSelection[i]['Az']),2)
        lSelection[i]['Fitness'] = round(calculateFitness(float(inp['Posición objetivo X'].get()), float(inp['Posición objetivo Y'].get()), lSelection[i]['X'], lSelection[i]['Y']),4)
    for i in range(len(lSelection)):
        totFitness += lSelection[i]['Fitness']
    for i in range(len(lSelection)):
        lSelection[i]['Prob'] = lSelection[i]['Fitness'] / totFitness
    auxPob = int(inp['Población máxima'].get()) - int(inp['Población inicial'].get())
    randNumbers = np.random.rand(auxPob)
    for i in range(len(randNumbers)):
        aux = []
        for j in range(len(lSelection)):
            if j == 0:
                aux = [0, float(lSelection[j]['Prob'])]
            else:
                prob = getProbAcu(j)
                aux = [float(prob), float((prob + lSelection[j]['Prob']))]
            if randNumbers[i] >= aux[0] and randNumbers[i] <= aux[1] and count <= int(inp['Población inicial'].get()):
                if count < (int(inp['Población inicial'].get())-1):
                    # print('Se encontro',randNumbers[i], ' en aux:',aux,'\nPoblación act: ',countPob)
                    lSelection[j]['Count'] += 1
                    countPob += 1
                    count += 1
                    break
                else:
                    pos = getFitnessMaxSelec()
                    lSelection[pos]['Count'] += 1
                    countPob += 1
                    count += 1
    printList(lSelection)
    for i in range(len(lSelection)):
        if i == 0:
            bestFitness = lSelection[0]['Fitness']
            VoMax = lSelection[0]['Vo']
            EleMax = lSelection[0]['Ele']
            AzMax = lSelection[0]['Az']
            worstFitness = lSelection[0]['Fitness']
        else:
            # Minimizing
            # Invert operators in if's if you want to maximize
            if bestFitness > lSelection[i]['Fitness']:
                bestFitness = lSelection[i]['Fitness']
                VoMax = lSelection[i]['Vo']
                EleMax = lSelection[i]['Ele']
                AzMax = lSelection[i]['Az']
            if worstFitness < lSelection[i]['Fitness']:
                worstFitness = lSelection[i]['Fitness']
    dictTop = {'Gen #': countGen+1, 'Vo': VoMax, 'Ele': EleMax, 'Az': AzMax, 'Best': bestFitness, 'Worst': worstFitness, 'Prom': (totFitness/len(lSelection))}
    lTop.append(dictTop)
    print('Sum fitness: ',totFitness)
    print('Prom fitness: ',(totFitness/len(lSelection)))
    print('Generation: ', countGen+1,' Vo: ', VoMax,' Ele:', EleMax, ' Az:', AzMax, ' betterFitness: ', bestFitness, ' worstFitness: ', worstFitness)
    selection()

def createIndividues(pobIni):
    global countPob
    aux = []
    for i in range(pobIni):
        dictPob = {'ID':i+1, 'Vo': round(random.randint(1,15),2), 'Ele': round(random.uniform(0,90),2), 'Az': round(random.uniform(0,360),2), 'R': 0, 'X': 0, 'Y': 0, 'Fitness': 0, 'Prob': 0, 'Count': 0}
        aux.append(dictPob)
        countPob += 1
    return aux

def getRange(X, Y):
    rang = math.sqrt(math.pow((X-0),2) + (math.pow((Y-0), 2)))
    return rang

def initialize(inp):
    global lSelection
    rangobj = getRange(float(inp['Posición objetivo X'].get()), float(inp['Posición objetivo Y'].get()))
    print('Rango:', rangobj)
    lSelection = createIndividues(int(inp['Población inicial'].get()))

def ecuationTray(a,b,x):
    return(a*x-b*x**2)

def graphParabolic(list):
    global grav
    for i in range(len(list)):
        vi = list[i]['Vo']
        inc = list[i]['Ele']
        tetha = ((inc*math.pi)/100)
        a = math.tan(tetha)
        b = ((grav)/((2*vi**2)*math.cos(inc)**2))
        ymax = (vi**2)*(np.sin(inc)*math.sin(inc))/(2*grav)
        xmax = (vi**2)*(np.sin(2*inc))/(grav)
        tmax=(vi*math.sin(inc))/(grav)
        tv=2*(tmax)
        x = np.linspace(0,xmax, 500)
        plot.figure("App-SGA", figsize=(10,8), dpi=80, facecolor="y",edgecolor="c")
        # plot.axes(axisbg="orange")
        # añadimos el titulo
        # title("Tiro al blanco", 
            # fontsize=15,color="blue",verticalalignment="baseline",horizontalalignment = "center")  
        # añadimos el subtitulo
        plot.suptitle("App-SGA",fontsize=20,color="red")
        # xlabel("xmax",fontsize=20,color="red")                                      
        # ylabel("ymax",fontsize=20,color="blue")
        #añadimos texto
        plot.text(((np.argmax(ecuationTray(a,b,x)))/2),np.max(ecuationTray(a,b,x))+1,"vi=",fontsize=10)
        plot.text(((np.argmax(ecuationTray(a,b,x)))/2)+11,np.max(ecuationTray(a,b,x))+1,(str(vi)+"m/s"),fontsize=10)

        # Añadimos la rejilla en la gráfica
        plot.grid(True)                                                              
        plot.grid(color = '0.5', linestyle = '--', linewidth = 1)
        # Añadimos los ejes 
        # plot.axis("tight")

        # dibujamos y ponemos etiquetas a la gráfica
        plot.text(3,1,inc,fontsize=10)
        plot.plot(x, ecuationTray(a,b,x), "red", linewidth = 2, label = (str(inc)+"º"))   
        # añadimos la leyenda
        plot.legend(loc = 4,fontsize=10)                                                         
        #anotaciones en el gráfico
        # plot.annotate('Altura Máxima',
        #     xy = (xmax/2, ymax),
        #     xycoords = 'data',
        #     xytext = (-70, -50),
        #     textcoords = 'offset points',
        #     arrowprops = dict(arrowstyle = "->",
        #     connectionstyle = "arc, angleA = 0,armA = 30,rad = 50"),
        #     # dibujar tabla dentro del gráfico
        #     valores = [[format(np.max(xmax),".2f"), format(np.min(ymax),".2f")]],
        #     etiquetas = ["xmax (m)", "ymax (m)"])
        etiquetas = ["xmax (m)", "ymax (m)"]
        valores = [[format(np.max(xmax),".2f"), format(np.min(ymax),".2f")]],
        plot.table(cellText=valores, colLabels = etiquetas, colWidths = [0.15]*len(ecuationTray(a,b,x)),loc='upper right')
        # guarda la gráfica con 300dpi (puntos por pulgada)en python34-ejemplos curso python
        # plot.savefig("figura_Lanzamiento Proyectiles_1.pdf", dpi = 300)            
        # mostramos en pantalla la gráfica
        plot.show()

def start(input):
    global countGen
    global lTop
    initialize(input)
    evaluation(input)
    cross(input)
    mutation(input)
    # while countGen < 5:
    #     print('------------------ Selection #',countGen+1,' ------------------')
    #     evaluation(input)
    #     print('------------------ Cross #',countGen+1,' ------------------')
    #     cross(input)
    #     print('------------------ Mutation #',countGen+1,' ------------------')
    #     mutation(input)
    #     countGen += 1
    # else: 
    #     print('------------------ Mejores Resultados ------------------')
    #     printList(lTop)
    #     graphParabolic(lTop)

def validModelation(input):
    try:
        float(input)
        return True
    except:
        return False
    if input.isdigit():
        return True
    else:
        messagebox.showerror('Error en modelación', 'Revisar tipo de datos ingresados')
        return False

def makeform(root, fields):
    title = Label(root, text="Inicialización", width=20, font=("bold",20))
    title.pack()
    entries = {}
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=30, text=field+": ", anchor='w')
        ent = Entry(row, validate="key", validatecommand=(row.register(validModelation), '%P'))
        row.pack(side = TOP, fill = X, padx = 5 , pady = 5)
        lab.pack(side = LEFT)
        ent.pack(side = RIGHT, expand = YES, fill = X)
        entries[field] = ent
    return entries

if __name__ == '__main__':
    root.title("App-SGA - UPCH IA")
    root.geometry("300x320")
    root.resizable(0,0)
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e = ents: fetch(e)))
    b1 = Button(root, text = 'Iniciar',
       command=(lambda e = ents: start(e)), bg="green",fg='white')
    b1.pack(side = LEFT, padx = 5, pady = 5, expand = YES)
    b3 = Button(root, text = 'Quit', command = root.quit, bg="red",fg='white')
    b3.pack(side = LEFT, padx = 5, pady = 5, expand = YES)
    root.mainloop()