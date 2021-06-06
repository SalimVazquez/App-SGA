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
    x = vMax * math.cos(math.radians(tetha))
    return x

def polarToCartesianY(vMax, tetha):
    y = vMax * math.sin(math.radians(tetha))
    return y

# The horizontal range of each of the projectiles
def rangeProjectils(Vo, tetha):
    global grav
    # Vo² * sin(2*θ) / g
    vMax = (math.pow(Vo,2) * math.sin(math.radians((2*tetha))) / grav)
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
    for i in range(ite, len(auxGen)):
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
    rangobj = getRange(float(inp['Posición objetivo X'].get()), float(inp['Posición objetivo Y'].get()))
    R = rangobj/2
    for i in range(len(lMutation)):
        yVo = random.uniform(-1,1)
        lMutation[i]['VoH'] = round((lMutation[i]['Vo'] + (yVo * R)),2)
        yTetha = random.uniform(-1,1)
        lMutation[i]['EleH'] = round((lMutation[i]['Ele'] + (yTetha * R)),2)
        yAz = random.uniform(-1,1)
        lMutation[i]['AzH'] = round((lMutation[i]['Az'] + (yAz * R)),2)
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
        lCross[i]['Vo'] = round(aVo*auxVo1 + (1-aVo) * auxVo2,2)
        lCross[i+1]['Vo'] = round(aVo*auxVo2 + (1-aVo) * auxVo1,2)
        auxTetha1 = lCross[i]['EleP']
        auxTetha2 = lCross[i+1]['EleP']
        aEle = random.uniform(0,1)
        lCross[i]['Ele'] = round(aEle*auxTetha1 + (1-aEle) * auxTetha2,2)
        lCross[i+1]['Ele'] = round(aEle*auxTetha2 + (1-aEle) * auxTetha1,2)
        auxAz1 = lCross[i]['AzP']
        auxAz2 = lCross[i+1]['AzP']
        aZ = random.uniform(0,1)
        lCross[i]['Az'] = round(aZ*auxAz1 + (1-aZ) * auxAz2,2)
        lCross[i+1]['Az'] = round(aZ*auxAz2 + (1-aZ) * auxAz1,2)
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
        lSelection[i]['Prob'] = round(lSelection[i]['Fitness'] / totFitness, 4)
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
        dictPob = {'ID':i+1, 'Vo': round(random.uniform(1,100),2), 'Ele': round(random.uniform(0,90),2), 'Az': round(random.uniform(0,360),2), 'R': 0, 'X': 0, 'Y': 0, 'Fitness': 0, 'Prob': 0, 'Count': 0}
        aux.append(dictPob)
        countPob += 1
    return aux

def getRange(X, Y):
    rang = math.sqrt(math.pow((X-0),2) + (math.pow((Y-0), 2)))
    return rang

def initialize(inp):
    global lSelection
    rangobj = getRange(float(inp['Posición objetivo X'].get()), float(inp['Posición objetivo Y'].get()))
    print('Obj\nX:',float(inp['Posición objetivo X'].get()), ' Y:',float(inp['Posición objetivo Y'].get()))
    print('Rango a origen:', rangobj)
    lSelection = createIndividues(int(inp['Población inicial'].get()))

def graphEvolution(inp):
    global lTop
    maxs = []
    mins = []
    proms = []
    generations = []
    
    for i in range(len(lTop)):
        maxs.append(lTop[i]['Best'])
        mins.append(lTop[i]['Worst'])
        proms.append(lTop[i]['Prom'])
        generations.append(i+1)
    plot.plot(generations, maxs, 'b-x', linewidth=2, label="Mejores")
    plot.plot(generations, mins, 'r-o', linewidth=2, label="Peores")
    plot.plot(generations, proms, 'g-s', linewidth=2, label="Promedio")
    plot.legend(loc='upper left')
    plot.xlabel('Generaciones')
    plot.ylabel('Fitness')
    plot.title("Evolución del Fitness")
    plot.grid()
    plot.show()

def graphParabolic():
    global lTop
    global grav
    dt = 0.01
    ptsX = []
    ptsY = []
    auxTop = lTop
    auxTop = sorted(auxTop, key=lambda x: x['Gen #'], reverse=True)
    for i in range(5):
        t = 0
        x = 0
        y = 0

        vx = auxTop[i]['Vo']*math.cos(math.radians(auxTop[i]['Ele']))
        vy = auxTop[i]['Vo']*math.sin(math.radians(auxTop[i]['Ele']))
        ptsX.clear()
        ptsY.clear()

        while y>=-0.01:
            t = t + dt
            x = x+vx*t
            y = y+vy*t-grav*t*t
            ptsX.append(x)
            ptsY.append(y)
        plot.plot(ptsX,ptsY, label="Gen" + str(auxTop[i]['Gen #']))
    plot.legend(loc='upper left')
    plot.title("Movimiento Parabólico")
    plot.xlabel("Posición horizontal(m)")
    plot.ylabel("Altura (m)")
    plot.show()

def evaluateFitness():
    global lSelection
    auxGen = lSelection
    auxGen = sorted(auxGen, key=lambda x: x['Fitness'])
    return auxGen[0]['Fitness']

def start(input):
    global countGen
    global lTop
    global lGen
    band = 1.0
    initialize(input)
    while band > 0.6 and countGen < 150:
        print('------------------ Selection #',countGen+1,' ------------------')
        evaluation(input)
        band = evaluateFitness()
        print('------------------ Cross #',countGen+1,' ------------------')
        cross(input)
        print('------------------ Mutation #',countGen+1,' ------------------')
        mutation(input)
        countGen += 1
    else: 
        print('------------------ Mejores Resultados ------------------')
        printList(lTop)
        graphEvolution(lTop)
        graphParabolic()
        messagebox.showinfo('Mejor fitness de todas las generaciones', band)

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