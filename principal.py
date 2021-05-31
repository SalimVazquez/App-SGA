from tkinter import *
from tkinter import messagebox
import numpy as np
import random
import math

root = Tk()
lSelection = []
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

def getProbAcu(limit):
    global lSelection
    a = 0
    for i in range(0, limit, 1):
        a += lSelection[i]['Prob']
    return a

def evaluation(inp):
    global lSelection
    global countPob
    global countGen
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
            if randNumbers[i] >= aux[0] and randNumbers[i] <= aux[1] and countPob <= int(inp['Población máxima'].get()):
                lSelection[j]['Count'] += 1
                countPob += 1
                # print('Se encontro',randNumbers[i], ' en aux:',aux,'\nPoblación act: ',countPob)
                break
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
    print('Sum fitness: ',totFitness)
    print('Prom fitness: ',(totFitness/len(lSelection)))
    print('Generation: ', countGen+1,' Vo: ', VoMax,' Ele:', EleMax, ' maxFitness: ', maxFitness, ' minFitness: ', minFitness)

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
    initialize(input)
    evaluation(input)

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