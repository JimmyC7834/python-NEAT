from tkinter import Tk, Canvas, Frame, BOTH, Entry, Scrollbar
from random import random, randint
import math

class Genomes():
    def __init__(self):
        self.nodeGenes = [NodeGene(_id=i, _type='input') for i in range(3)]
        self.nodeGenes[2].type='output'
        self.connectionGenes = []
    
    def add_nodeGene(self, nodeGene):
        nodeGene.id = len(self.nodeGenes)
        self.nodeGenes.append(nodeGene)

    def add_connectionGene(self, connectionGene):
        connectionGene.id = len(self.connectionGenes)
        self.connectionGenes.append(connectionGene)

    def get_random_nodeGene(self, reject_type=[]):
        n = self.nodeGenes[randint(0, len(self.nodeGenes)-1)]
        while n.type in reject_type:
            n = self.nodeGenes[randint(0, len(self.nodeGenes)-1)]
        return n
    
    def mutate_add_node(self):
        c = self.connectionGenes[randint(0, len(self.connectionGenes)-1)]
        c.disable
        new_nodeGene = NodeGene(_type='hidden')
        new_connectionGene1 = ConnectionGene(c.in_node, new_nodeGene, weight=1)
        new_connectionGene2 = ConnectionGene(new_nodeGene,  c.out_node,  weight=c.weight)
        self.add_nodeGene(new_nodeGene)
        self.add_connectionGene(new_connectionGene1)
        self.add_connectionGene(new_connectionGene2)

    def mutate_add_connection(self):
        nodeGene1 = self.get_random_nodeGene(['output'])
        nodeGene2 = self.get_random_nodeGene(['input'])
        for i in self.connectionGenes:
            if nodeGene1 == i.in_node and nodeGene2 == i.out_node:
                return
        self.add_connectionGene(ConnectionGene(nodeGene1, nodeGene2))

class ConnectionGene():
    def __init__(self, in_node, out_node, _id=0, weight=None, expressed=True, inn_number=0):
        self.in_node = in_node
        self.out_node= out_node
        self.id = _id
        self.weight = weight if weight != None else random()
        self.expressed = expressed
        self.inn_number = inn_number
    
    def disable(self):
        self.expressed = False
    
    def enable(self):
        self.expressed = True

class NodeGene():
    def __init__(self,  _id=0,  _type=None):
        TYPES = ['input', 'hidden', 'output']
        self.type = _type if _type != None else TYPES[randint(0, len(TYPES)-1)]
        self.id = _id

class NEATPanel(Frame):
    def __init__(self, tile_size, Genomes=[]):
        self.root = Tk()
        self.root.geometry("780x720")
        self.root.update()
        self.genoemes_num = len(Genomes)
        self.genoemes = Genomes
        self.tile_num = 5
        self.tile_size = tile_size
        self.entry = Entry(self.root)
        self.entry.grid(row=0, column=4)
        self.root.bind('<Return>', self.hit_enter)

        canvas_main = Canvas(self.root, width=620, height=720)
        canvas_main.grid(row=0, column=0, sticky='news')

        scroll_bar = Scrollbar(self.root, orient="vertical", command=canvas_main.yview)
        scroll_bar.grid(row=0, column=1, sticky='ns')
        canvas_main.configure(yscrollcommand=scroll_bar.set)

        self.frame=Frame(self.root,width=600,height=math.ceil(self.genoemes_num/self.tile_num)*120)
        canvas_main.create_window((0, 0), window=self.frame, anchor='nw')

        self.canvases = [Canvas(self.frame, width = self.tile_size, height = self.tile_size, bg='gray') for _ in range(self.genoemes_num)]
    
        counter = 0
        for i in range(math.ceil(self.genoemes_num/self.tile_num)):
            for j in range(self.tile_num):
                self.canvases[counter].grid(row=i, column=j, sticky='news')
                if counter == self.genoemes_num-1:
                    break
                counter += 1

        canvas_main.config(scrollregion=canvas_main.bbox("all"))
        self.frame.update_idletasks()

    def start(self):
        self.root.mainloop()

    def hit_enter(self, event):
        _input = int(self.entry.get())
        #self.canvases[_input].place(x=0,y=0)
        self.canvases[_input].grid(row=0, column=0, columnspan = 2, rowspan = 2, padx=5, pady=5)
        self.canvases[_input].config(width=320, height=320)
        self.frame.update_idletasks()

if __name__ == "__main__":
    
    g = Genomes()
    g.mutate_add_connection()
    g.mutate_add_node()

    NEATPanel(120,[Genomes() for _ in range(80)]).start()

    