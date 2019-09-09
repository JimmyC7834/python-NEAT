from tkinter import Tk, Canvas, Frame, BOTH, Entry, Scrollbar
from random import random, randint
import math

global_inn_number = 0

class Genome():
    def __init__(self):
        self.nodeGenes = [NodeGene(_id=i, _type='input') for i in range(4)]
        self.nodeGenes[2].type='hidden'
        self.nodeGenes[3].type='output'

        self.nodeGenes[0].connect(self.nodeGenes[2])
        self.nodeGenes[1].connect(self.nodeGenes[2])
        self.nodeGenes[2].connect(self.nodeGenes[3])

        self.connectionGenes = []
        self.add_connectionGene(ConnectionGene(self.nodeGenes[0], self.nodeGenes[2], _id=0, inn_number=0))
        self.add_connectionGene(ConnectionGene(self.nodeGenes[1], self.nodeGenes[2], _id=1, inn_number=0))
        self.add_connectionGene(ConnectionGene(self.nodeGenes[2], self.nodeGenes[3], _id=2, inn_number=0))
    
    def add_nodeGene(self, nodeGene):
        nodeGene.id = len(self.nodeGenes)
        self.nodeGenes.append(nodeGene)
        print('added node', nodeGene.id)

    def add_connectionGene(self, connectionGene):
        connectionGene.id = len(self.connectionGenes)
        global global_inn_number
        connectionGene.inn_number = global_inn_number
        global_inn_number += 1
        self.connectionGenes.append(connectionGene)
        print('connected nodes', connectionGene.in_node.id, ',', connectionGene.out_node.id)

    def get_random_nodeGene(self, reject_type=[]):
        n = self.nodeGenes[randint(0, len(self.nodeGenes)-1)]
        while n.type in reject_type:
            n = self.nodeGenes[randint(0, len(self.nodeGenes)-1)]
        return n
    
    def get_nodeGene_by_id(self, id):
        for i in self.nodeGenes:
            if i.id == id:
                return i
        return None

    def mutate_add_node(self):
        c = self.connectionGenes[randint(0, len(self.connectionGenes)-1)]
        c.disable()

        new_nodeGene = NodeGene(_id=len(self.nodeGenes), _type='hidden')
        new_connectionGene1 = ConnectionGene(c.in_node, new_nodeGene, weight=1, inn_number=0)
        new_connectionGene2 = ConnectionGene(new_nodeGene, c.out_node, weight=c.weight, inn_number=0)

        c.in_node.connect(new_nodeGene)
        new_nodeGene.connect(c.out_node)

        self.add_nodeGene(new_nodeGene)
        self.add_connectionGene(new_connectionGene1)
        self.add_connectionGene(new_connectionGene2)

    def mutate_add_connection(self):
        nodeGene1 = self.get_random_nodeGene(['output'])
        nodeGene2 = self.get_random_nodeGene(['input']) 

        while nodeGene1.id == nodeGene2.id:
            nodeGene2 = self.get_random_nodeGene(['input']) 

        if nodeGene2.id in nodeGene1.connected_ids:
            return

        nodeGene1.connect(nodeGene2)
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
        print('disabled', self.id)
    
    def enable(self):
        self.expressed = True
        print('enabled', self.id)

class NodeGene():
    def __init__(self, _id=0, _type=None):
        TYPES = ['input', 'hidden', 'output']
        self.type = _type if _type != None else TYPES[randint(0, len(TYPES)-1)]
        self.id = _id
        self.x = 0
        self.y = 0
        self.connected_ids = []
    
    def connect(self, nodeGene):
        self.connected_ids.append(nodeGene.id)
        nodeGene.connected_ids.append(self.id)

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

    def hit_enter(self, event):
        # _input = int(self.entry.get())
        g = Genome()
        self.canvas.delete("all")

        g.mutate_add_connection()
        g.mutate_add_node()

        self.display_genome(g)

        #self.canvases[_input].place(x=0, y=0)
    
    def display_genome(self, genome):
        nodes = {
            'input':[], 
            'hidden':[], 
            'output':[]
        }

        for i in genome.nodeGenes:
            nodes[i.type].append(i)
        
        for i, v in enumerate(nodes['input']):
            v.x = 40
            v.y = (i+.5)*(640/len(nodes['input']))
        
        for i, v in enumerate(nodes['output']):
            v.x = 600
            v.y = (i+.5)*(640/len(nodes['output']))
                
        for i in nodes['hidden']:
            x, y = 0, 0
            connected_num = len(i.connected_ids)

            for j in i.connected_ids:
                n = genome.get_nodeGene_by_id(j)
                x += n.x
                y += n.y

            x /= connected_num
            y /= connected_num
            i.x = x
            i.y = y

        for i in genome.connectionGenes:
            self.canvas.create_line(i.in_node.x, i.in_node.y, i.out_node.x, i.out_node.y, width=i.weight*5, fill='blue')
            self.canvas.create_text((i.in_node.x+i.out_node.x)/2, (i.in_node.y+i.out_node.y)/2, text=i.id, fill='black')

        for i in genome.nodeGenes:
            self.canvas.create_oval(i.x-15, i.y-15, i.x+15, i.y+15, fill='red', outline='red')
            self.canvas.create_text(i.x, i.y, text=i.id, fill='white')

if __name__ == "__main__":
    global_inn_number = 0
    g = Genome()
    
    np = NEATPanel(120)
    np.display_genome(g)
    np.start()
    
    