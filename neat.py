import math
from random import *

class Genomes():
    def __init__(self,nodeGenesNum,connectionGenesNum):
        self.nodeGenes = [NodeGene(_id=i) for i in range(nodeGenesNum)]
        self.connectionGenes = 0
    
    def get_random_nodeGene(self,reject_type=[]):
        n = self.nodeGenes[random.randint(0,len(self.nodeGenes)-1)]
        while n.type in reject_type:
            n = self.nodeGenes[random.randint(0,len(self.nodeGenes)-1)]
        return n
    
    def mutate_add_connection(self):
        nodeGene1 = self.get_random_nodeGene(['output'])
        nodeGene2 = self.get_random_nodeGene(['input'])
        for i in self.connectionGenes:
            if nodeGene1 == i.in_node and nodeGene2 == i.out_node:
                return
        self.connectionGenes.append(ConnectionGene(nodeGene1,nodeGene2))

class ConnectionGene():
    def __init__(self,in_node,out_node,weight = None,expressed=True,inn_number=0):
        self.in_node = in_node
        self.out_node= out_node
        self.weight = weight if weight != None else random()
        self.expressed = expressed
        self.inn_number = inn_number

class NodeGene():
    def __init__(self,_id,_type=None):
        TYPES = ['input','hidden','output']
        self.type = _type if _type != None else TYPES[randint(0,len(TYPES)-1)]
        self.id = _id

g = Genomes(3,2)

