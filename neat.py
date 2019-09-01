import math
from random import *

class Genomes():
    def __init__(self):
        self.nodeGenes = [NodeGene(_id=i,_type='input') for i in range(3)]
        self.nodeGenes[2].type='output'
        self.connectionGenes = []
    
    def add_nodeGene(self,nodeGene):
        nodeGene.id = len(self.nodeGenes)
        self.nodeGenes.append(nodeGene)

    def add_connectionGene(self,connectionGene):
        connectionGene.id = len(self.connectionGenes)
        self.connectionGenes.append(connectionGene)

    def get_random_nodeGene(self,reject_type=[]):
        n = self.nodeGenes[randint(0,len(self.nodeGenes)-1)]
        while n.type in reject_type:
            n = self.nodeGenes[randint(0,len(self.nodeGenes)-1)]
        return n
    
    def mutate_add_node(self):
        c = self.connectionGenes[randint(0,len(self.connectionGenes)-1)]
        c.disable
        new_nodeGene = NodeGene(_type='hidden')
        new_connectionGene1 = ConnectionGene(c.in_node,new_nodeGene,weight=1)
        new_connectionGene2 = ConnectionGene(new_nodeGene,c.out_node,weight=c.weight)
        self.add_nodeGene(new_nodeGene)
        self.add_connectionGene(new_connectionGene1)
        self.add_connectionGene(new_connectionGene2)

    def mutate_add_connection(self):
        nodeGene1 = self.get_random_nodeGene(['output'])
        nodeGene2 = self.get_random_nodeGene(['input'])
        for i in self.connectionGenes:
            if nodeGene1 == i.in_node and nodeGene2 == i.out_node:
                return
        self.add_connectionGene(ConnectionGene(nodeGene1,nodeGene2))


class ConnectionGene():
    def __init__(self,in_node,out_node,_id=0,weight=None,expressed=True,inn_number=0):
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
    def __init__(self,_id=0,_type=None):
        TYPES = ['input','hidden','output']
        self.type = _type if _type != None else TYPES[randint(0,len(TYPES)-1)]
        self.id = _id

g = Genomes()
g.mutate_add_connection()
g.mutate_add_node()
print(len(g.connectionGenes),',',len(g.nodeGenes))