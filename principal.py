from tkinter import *
from tkinter import messagebox
import numpy as np
import random
import math

root = Tk()
lSelection = []
lCross = []
lMutation = []
lTop = []
lGen = []
countPob = 0
countGen = 0
grav = 9.81

fields = (
    'Población inicial',
    'Población máxima',
    'Posición objetivo X', 
    'Posición objetivo Y',
    'Velocidad del viento',
    'Prob de mutación de bits',
    'Prob de mutación de individuo'
)

def printList(list):
    for i in range(len(list)):
        print(list[i])

def calculateXMax(Vo, tetha):
    Xmax = ((math.pow(Vo,2) * math.sin(2*tetha))/grav)
    return abs(Xmax)

def calculateFitness(Xmax, Xobj):
    fitness = abs(Xobj - Xmax)
    return fitness

def poda(ite):
    global lSelection
    global lGen
    global countPob
    auxGen = lGen
    auxGen = sorted(auxGen, key=lambda x: x['fitnessM'])
    lSelection.clear()
    for i in range(ite):
        if auxGen[i]['fitnessP'] < auxGen[i]['fitnessH']:
            dictSel = {'ID':i+1, 'Vo': auxGen[i]['VoP'], 'Ele': auxGen[i]['EleP'], 'Xmax': 0, 'Fitness': 0, 'Prob': 0, 'Count': 0}
        else:
            dictSel = {'ID':i+1, 'Vo': auxGen[i]['VoH'], 'Ele': auxGen[i]['EleH'], 'Xmax': 0, 'Fitness': 0, 'Prob': 0, 'Count': 0}
        lSelection.append(dictSel)
        countPob += 1
    for i in range(2, len(auxGen)):
        dictSel = {'ID':i+1, 'Vo': auxGen[i]['VoH'], 'Ele': auxGen[i]['EleH'], 'Xmax': 0, 'Fitness': 0, 'Prob': 0, 'Count': 0}
        lSelection.append(dictSel)
    print('------------------ Poda ------------------')
    printList(lGen)
    lGen.clear()

def cleanLists():
    global lSelection
    global lCross
    global lMutation
    global contPob
    lSelection.clear()
    lCross.clear()
    lMutation.clear()
    contPob = 0

def mutation(inp):
    global lMutation
    global lGen
    Pmi = float(inp['Prob de mutación de individuo'].get())
    Pmb = float(inp['Prob de mutación de bits'].get())
    Pm = (Pmi/100) * (Pmb/100)
    for i in range(len(lMutation)):
        randomGen = (random.randint(1,100)/100)
        alter = random.randint(-5,5)
        if randomGen < Pm and (i+1) % 2 == 0:
            lMutation[i]['VoR'] = lMutation[i]['VoC'] + alter
            lMutation[i]['EleR'] = lMutation[i]['EleC']
        elif randomGen < Pm and (i+1) % 2 != 0:
            lMutation[i]['VoR'] = lMutation[i]['VoC']
            lMutation[i]['EleR'] = lMutation[i]['EleC'] + alter
        else:
            lMutation[i]['VoR'] = lMutation[i]['VoC']
            lMutation[i]['EleR'] = lMutation[i]['EleC']
    for i in range(len(lMutation)):
        auxMax = calculateXMax(random.randint(1,100), random.uniform(0,90))
        lMutation[i]['Fitness'] = calculateFitness(auxMax, float(inp['Posición objetivo X'].get()))
        lGen[i]['VoH'] = lMutation[i]['VoR']
        lGen[i]['EleH'] = lMutation[i]['EleR']
        lGen[i]['fitnessH'] = lMutation[i]['Fitness']
        if lGen[i]['fitnessH'] < lGen[i]['fitnessP']:
            lGen[i]['VoM'] = lGen[i]['VoH']
            lGen[i]['EleM'] = lGen[i]['EleH']
            lGen[i]['fitnessM'] = lGen[i]['fitnessH']
        else:
            lGen[i]['VoM'] = lGen[i]['VoP']
            lGen[i]['EleM'] = lGen[i]['EleP']
            lGen[i]['fitnessM'] = lGen[i]['fitnessP']
    printList(lMutation)
    cleanLists()
    poda(2)

def cross(inp):
    global lCross
    global lMutation
    position = 0
    for i in range(0, len(lCross), 2):
        auxVo1 = lCross[i]['Vo']
        auxVo2 = lCross[i+1]['Vo']
        lCross[i]['VoC'] = auxVo2
        lCross[i+1]['VoC'] = auxVo1
        # auxTetha1 = lCross[i]['Ele']
        # auxTetha2 = lCross[i+1]['Ele']
        lCross[i]['EleC'] = lCross[i]['Ele']
        lCross[i+1]['EleC'] = lCross[i+1]['Ele']
    
    for i in range(len(lCross)):
        auxMax = calculateXMax(random.randint(1,100), random.uniform(0,90))
        lCross[i]['Fitness'] = calculateFitness(auxMax, float(inp['Posición objetivo X'].get()))
        dictMut = {'ID': position+1, 'VoC': lCross[i]['VoC'], 'EleC': lCross[i]['EleC'], 'VoR':  0, 'EleR': 0, 'Fitness': 0}
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
                dictCross = {'ID':position+1, 'Vo': lSelection[i]['Vo'], 'Ele': lSelection[i]['Ele'], 'VoC': 0, 'EleC': 0, 'Fitness': 0}
                lCross.append(dictCross)
                dictGen = {'ID': position+1, 'VoP': lSelection[i]['Vo'], 'EleP': lSelection[i]['Ele'], 'fitnessP': lSelection[i]['Fitness'], 'VoH': 0, 'EleH': 0, 'fitnessH': 0, 'VoM': 0, 'EleM': 0, 'fitnessM': 0}
                lGen.append(dictGen)
                position += 1

def getFitnessMaxSelec():
    global lSelection
    maximo = 0
    position = 0
    for i in range(len(lSelection)):
        if i == 0:
            maximo = lSelection[i]['Fitness']
        else:
            if maximo > lSelection[i]['Fitness']:
                maximo = lSelection[i]['Fitness']
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
        lSelection[i]['Xmax'] = calculateXMax(lSelection[i]['Vo'], lSelection[i]['Ele'])
        lSelection[i]['Fitness'] = calculateFitness(lSelection[i]['Xmax'], float(inp['Posición objetivo X'].get()))
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
            maxFitness = lSelection[0]['Fitness']
            VoMax = lSelection[0]['Vo']
            EleMax = lSelection[0]['Ele']
            minFitness = lSelection[0]['Fitness']
        else:
            # Minimizando
            # Invertir operadores en if's si desea maximizar
            if maxFitness > lSelection[i]['Fitness']:
                maxFitness = lSelection[i]['Fitness']
                VoMax = lSelection[i]['Vo']
                EleMax = lSelection[i]['Ele']
            if minFitness < lSelection[i]['Fitness']:
                minFitness = lSelection[i]['Fitness']
    dictTop = {'Gen #': countGen+1, 'Mejor': maxFitness, 'Peor': minFitness, 'Promedio': (totFitness/len(lSelection))}
    lTop.append(dictTop)
    print('Sum fitness: ',totFitness)
    print('Prom fitness: ',(totFitness/len(lSelection)))
    print('Generation: ', countGen+1,' Vo: ', VoMax,' Ele:', EleMax, ' maxFitness: ', maxFitness, ' minFitness: ', minFitness)
    selection()

def createIndividues(pobIni):
    global countPob
    aux = []
    for i in range(pobIni):
        dictPob = {'ID':i+1, 'Vo': random.randint(1,100), 'Ele': random.uniform(0,90), 'Xmax': 0, 'Fitness': 0, 'Prob': 0, 'Count': 0}
        aux.append(dictPob)
        countPob += 1
    return aux

def initialize(inp):
    global lSelection
    lSelection = createIndividues(int(inp['Población inicial'].get()))

def start(input):
    global countGen
    initialize(input)
    while countGen < 5:
        print('------------------ Selection #',countGen+1,' ------------------')
        evaluation(input)
        print('------------------ Cross #',countGen+1,' ------------------')
        cross(input)
        print('------------------ Mutation #',countGen+1,' ------------------')
        mutation(input)
        countGen += 1
    else: 
        print('------------------ Mejores Resultados ------------------')
        printList(lTop)

def validModelation(input):
    try:
        float(input)
        return True
    except:
        return False
    if input.isdigit():
        return True
    else:
        messagebox.showerror('Error en modelación', 'Se esperaba un tipo de dato: Integer')
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