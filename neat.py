from tkinter import Tk, Canvas, Frame, BOTH, Entry, Scrollbar
from random import random, randint
import math

class Genome():
    def __init__(self):
        self.nodeGenes = [NodeGene(_id=i, _type='input') for i in range(4)]
        self.nodeGenes[2].type='hidden'
        self.nodeGenes[3].type='output'
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
        self.x = 0
        self.y = 0

class NEATPanel(Frame):
    def __init__(self, tile_size):
        self.root = Tk()
        self.root.geometry("780x640")
        self.root.update()
        self.root.config(bg='gray')
        self.entry = Entry(self.root)
        self.entry.grid(row=0, column=2)
        self.root.bind('<Return>', self.hit_enter)
        self.canvas = Canvas(self.root, width=640, height=640, bg='light gray')
        self.canvas.grid(row=0, column=0)

    def start(self):
        self.root.mainloop()

    def hit_enter(self, event, genomes=[]):
        _input = int(self.entry.get())
        self.display_genome(genomes[_input])
        #self.canvases[_input].place(x=0,y=0)
    
    def display_genome(self,genome):
        nodes = {
            'input':[],
            'hidden':[],
            'output':[]
        }

        for i in genome.nodeGenes:
            nodes[i.type].append(i)
        
        for i,v in enumerate(nodes['input']):
            v.x = 40
            v.y = i*(640/len(nodes['input']))
        
        for i,v in enumerate(nodes['output']):
            v.x = 600
            v.y = (i+1)*(640/len(nodes['output'])+1)
        
        for i in genome.nodeGenes:
            self.canvas.create_oval(i.x-15, i.y-15, i.x+15, i.y+15, fill='red')

if __name__ == "__main__":
    
    g = Genome()
    g.mutate_add_connection()
    g.mutate_add_node()

    NEATPanel(120).start()

    