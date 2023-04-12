from numpy.random import randint, shuffle
from numpy import linspace
import networkx as nx
import matplotlib.pyplot as plt

class Pupil:
    def __init__(self, name, gender, prioList) -> None:
        self.Name = name
        self.gender = gender
        self.k_priorities = len(prioList)
        self.priorities = prioList + ["No one"]
        
        self.current_priority = -1
        self.queue = []
        self.married = False
        
    def __str__(self) -> str:
        if self.married:
            return self.Name + " married " + self.priorities[self.current_priority]
        else:
            return self.Name + " has no one"
        
    def __repr__(self) -> str:
        if self.married:
            return self.Name + " married "+str(self.current_priority+1)+" " + self.priorities[self.current_priority]
        else:
            return self.Name + " has no one"

        # return self.Name + " \ncurrent_priority = "+str(self.current_priority)+"married = "+str(self.married)+"\npriorities = "+str(self.priorities) + "\nqueue = "+str(self.queue)

def myShuffle(seq):
    seq2 = seq.copy()
    shuffle(seq2)
    return seq2


def randPeople(names_M, names_G):
    k_priorities_M = [randint(1,len(names_G)) for name in names_M];
    k_priorities_G = [randint(1,len(names_M)) for name in names_G];

    mass_M = [ Pupil(name, 'M', myShuffle(names_G)[0:randint(1, len(names_G))])
              for name in names_M
            ]
    mass_G = [ Pupil(name, 'G', myShuffle(names_M)[0:randint(1, len(names_M))])
              for name in names_G
            ]
    return mass_M, mass_G

def randNames(nM,nG=-1):
    if(nG==-1):
        nG=nM
    names_M = ["Pupil_M"+str(i) for i in range(nM)]
    names_G = ["Pupil_G"+str(i) for i in range(nG)]
    return names_M,names_G
    
def drawTmpEdges(B, edgesList, pos):
    
    plt.clf()
    nx.draw(B, with_labels=True, font_weight='bold', pos=pos,node_size=2000)
    B.add_edges_from(edgesList)
    nx.draw_networkx_edges(B,pos=pos,style='dashed')
    plt.show(block=False)
    plt.pause(1)
    
    B.remove_edges_from(edgesList) 
    plt.clf()
    nx.draw(B, with_labels=True, font_weight='bold', pos=pos,node_size=2000)
    plt.show(block=False)


################# main

# names_M = ["Misha", "Yegor", "Aleksey", "Andey","Pavel"]
# names_G = ["Marina", "Masha", "Yulia", "Daria", "Lera"]

names_M,names_G = randNames(50)
mass_M_origin, mass_G_origin = randPeople(names_M, names_G)
mass_M, mass_G = mass_M_origin, mass_G_origin


B = nx.Graph()
B.add_nodes_from(names_M, bipartite=0)
B.add_nodes_from(names_G, bipartite=1)
pos = {}
pos.update((node, (1, index)) for index, node in enumerate(names_M))
pos.update((node, (2, index)) for index, node in enumerate(names_G))

marriedList = []
while not (len(mass_G)==0 or len(mass_M)==0):
    # boys ask
    conEdges = []
    for boy in mass_M:
        boy.current_priority+=1
        girl_name = boy.priorities[boy.current_priority]
        conEdges.append((boy.Name, girl_name))
        if(girl_name in [g.Name for g in mass_G]):
            girl = [ g for g in mass_G if g.Name==girl_name][0]
            girl.queue.append(boy.Name)
            print(boy.Name + " goes to "+girl.Name)
    # drawTmpEdges(B,conEdges, pos)

    # girls answer
    for girl in mass_G:
        g_priority = -1
        for best_boy in girl.priorities:
            g_priority += 1
            if(best_boy in girl.queue):
                break
        else:
            continue
        
        boy = [ m for m in mass_M if m.Name==best_boy][0]
        boy.married = True
        
        girl.current_priority = g_priority
        girl.married = True
        
        marriedList.append((boy.Name, girl.Name))
        print(f"{girl.Name} say 'Yes' to {boy.Name}, they married")
    
    
    mass_M = [m for m in mass_M if m.married==False and m.current_priority<len(m.priorities)-2]
    mass_G = [g for g in mass_G if g.married==False and g.current_priority<len(g.priorities)-2]
    # B.add_edges_from(marriedList)
    # nx.draw(B, with_labels=True, font_weight='bold', pos=pos,node_size=2000)
    # plt.show(block=False)
    # plt.pause(1)
    print("p")

mass_M = mass_M_origin
mass_G = mass_G_origin

# set to -1 who not married
for m in mass_M:
    if(not m.married):
        m.current_priority=-1
for g in mass_G:
    if(not g.married):
        g.current_priority=-1



print("Results:")
print(mass_M_origin)
print(mass_G_origin)
print("end")
# plt.show()


plt.figure()
plt.hist([m.current_priority for m in mass_M], bins=linspace(-1-0.5, len(mass_G)+1+0.5      ))
plt.hist([m.current_priority for m in mass_M if m.current_priority==-1], bins=linspace(-1-0.5, len(mass_G)+1+0.5      ))
plt.axis([-2,55,0,55])
plt.figure()
plt.hist([g.current_priority for g in mass_G],  bins=linspace(-1-0.5, len(mass_M)+1+0.5      ))
plt.hist([g.current_priority for g in mass_G if g.current_priority==-1], bins=linspace(-1-0.5, len(mass_M)+1+0.5      ))
plt.axis([-2,55,0,55])
plt.show()










