from tkinter import *
from tkinter import messagebox
import random
import math

root = Tk()
individues = []
lSelection = []
countPob = 0
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

def evaluation(inp):
    global lSelection
    global countPob
    global individues
    totFitness = 0
    promFitness = 0
    for i in range(len(individues)):
        individues[i]['Xmax'] = calculateXMax(individues[i]['Vo'], individues[i]['Ele'])
        individues[i]['Fitness'] = calculateFitness(individues[i]['Xmax'], float(inp['Posición objetivo X'].get()))
    printList(individues)

def createIndividues(pobIni):
    global countPob
    aux = []
    for i in range(pobIni):
        dictPob = {'ID':i+1, 'Vo': random.randint(1,100), 'Ele': random.uniform(0,90), 'Xmax': 0, 'Fitness': 0, 'Prob': 0, 'Count': 0}
        aux.append(dictPob)
        countPob += 1
    return aux

def initialize(inp):
    global individues
    individues = createIndividues(int(inp['Población inicial'].get()))

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