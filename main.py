from numpy.random import randint, shuffle
from numpy import linspace
import networkx as nx
import matplotlib.pyplot as plt

secFast = 0.1
secSlow = 2
def waitPrint(message="", sec=-1):
    if(message=="" and sec==-1):
        sec=secFast
    if(sec==-1):
        sec=secSlow
    print(message)
    plt.pause(sec)

class Pupil:
    def __init__(self, name, gender, prioList) -> None:
        self.Name = name
        self.gender = gender
        self.k_priorities = len(prioList)
        self.priorities = prioList + ["No one"]
        
        self.current_priority = 0
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
    def selfDescribe(self):
        return self.Name + " has priorities: " + str(self.priorities)
    
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
    
    
class myGraph():
    def __init__(self, names_M, names_G, colors, pause, incoming_graph_data=None, **attr):
        self.B = nx.Graph()
        self.B.add_nodes_from(names_M, bipartite=0)
        self.B.add_nodes_from(names_G, bipartite=1)
        
        pos = {}
        pos.update((node, (1, index+1)) for index, node in enumerate(names_M))
        pos.update((node, (2, index+1)) for index, node in enumerate(names_G))
        self.pos = pos
        
        if(not colors):  
            self.colorMap = ['#00A2E8' for node in names_M + names_G]
        else:
            self.colorMap=colors
        self.constEdges = []        
        self.pauseBlink = pause
    
    def setPauseBlink(self, pause):
        self.pauseBlink=pause
    
    def setVertexColor(self, vertex, color):
        self.colorMap[list(self.B.nodes).index(vertex)] = color
    
    def addConstEdge(self, edge):
        self.constEdges += [edge]
        self.B.add_edges_from([edge])
    
    def draw(self):
        plt.clf()
        nx.draw(self.B, with_labels=True, font_weight='bold', pos=self.pos, node_color=self.colorMap, node_size=2000)
        plt.show(block=False)
    
    def drawTmpEdges(self, edgesDashed):
        plt.clf()
        self.draw()        
        self.B.add_edges_from(edgesDashed)
        nx.draw_networkx_edges(self.B,pos=self.pos, style='dashed')
        plt.show(block=False)
        self.B.remove_edges_from(edgesDashed)
    
    def blinkEdge(self, edgesDashed1, edgeBlink, numOfBlink=3):
        edgesDashed = edgesDashed1.copy()
        while(edgeBlink in edgesDashed):
            edgesDashed.pop(edgesDashed.index(edgeBlink))
        
        for i in range(1,numOfBlink):
            plt.clf()
            self.draw()            
        
            self.B.add_edges_from(edgesDashed)
            nx.draw_networkx_edges(self.B,pos=self.pos,style='dashed')
            plt.pause(self.pauseBlink)
            
            self.B.add_edge(*edgeBlink)
            nx.draw_networkx_edges(self.B,pos=self.pos,style='dashed')
            self.B.remove_edges_from(edgesDashed + [edgeBlink])
            plt.pause(self.pauseBlink)
        
    
    
     
################# main

names_M = ["Misha", "Yegor", "Aleks", "Andey","Pavel"]
names_G = ["Marin", "Masha", "Yulia", "Daria", "Lerra"]

# names_M,names_G = randNames(50)
mass_M_origin, mass_G_origin = randPeople(names_M, names_G)
mass_M, mass_G = mass_M_origin, mass_G_origin

for m in mass_M:
    waitPrint(m.selfDescribe(),secFast)
waitPrint(sec=secFast)
for g in mass_G:
    waitPrint(g.selfDescribe(),secFast)
waitPrint(sec=secFast)

B = myGraph(names_M, names_G, ['#00A2E8' for node in names_M + names_G], secFast)

marriedList = []
tmpEdges = []
dayNum = 0
while not (len(mass_G)==0 or len(mass_M)==0):
    dayNum+=1
    waitPrint(f"process, day {dayNum}")
    
    # boys ask    
    for boy in mass_M:
        while boy.current_priority < len(boy.priorities):
            girl_name = boy.priorities[boy.current_priority]
            if(girl_name in [g.Name for g in mass_G]):
                girl = [ g for g in mass_G if g.Name==girl_name][0]
                if not boy.Name in girl.queue: girl.queue.append(boy.Name)
                if not (boy.Name, girl_name) in tmpEdges: tmpEdges.append((boy.Name, girl_name)) # for graph
                B.drawTmpEdges(tmpEdges)
                waitPrint(boy.Name + " goes to "+girl.Name) # for console
                break
            else:
                boy.current_priority+=1
        if(boy.current_priority == len(boy.priorities)-1):
            B.setVertexColor(boy.Name, 'red')
            waitPrint(f"{boy.Name} out")
    B.drawTmpEdges(tmpEdges) # for graph
    waitPrint()
    
    # girls answer
    for girl in mass_G:
        
        # define self priority
        while girl.priorities[girl.current_priority] not in [m.Name for m in mass_M] and girl.current_priority<len(girl.priorities)-2:
            girl.current_priority+=1
        waitPrint(f"{girl.Name} checkout priority {girl.current_priority}")
        
        # say 'no'
        for boy_name in girl.queue:
            if(boy_name in [m.Name for m in mass_M]):
                boy = [ m for m in mass_M if m.Name==boy_name][0]
                
                if not boy_name in girl.priorities: 
                    boy.current_priority+=1
                    girl.queue.pop(girl.queue.index(boy_name)) # correct mistake
                    tmpEdges.pop(tmpEdges.index((boy.Name, girl.Name)))
                    
                    waitPrint(f"{girl.Name} say 'No' to {boy_name}",secFast)
                    B.blinkEdge(tmpEdges,(boy.Name,girl.Name))
                    B.drawTmpEdges(tmpEdges)
                    
            
            else:
                waitPrint("Error")
            
        
        for boy_name in girl.queue:
            if(boy_name in [m.Name for m in mass_M]):
                boy = [ m for m in mass_M if m.Name==boy_name][0]
                
                
                if(boy_name == girl.priorities[girl.current_priority]):
                
                    # Say yes to him
                    
                    boy.married = True
                    girl.married = True
                    
                    waitPrint(f"{girl.Name} say 'Yes' to {boy.Name}, they married", secFast)
                    B.blinkEdge(tmpEdges,(boy.Name,girl.Name))
                    tmpEdges.pop(tmpEdges.index((boy.Name, girl.Name)))
                    marriedList.append((boy.Name, girl.Name))
                    B.addConstEdge((boy.Name, girl.Name))
                    B.setVertexColor(boy.Name, 'green')
                    B.setVertexColor(girl.Name, 'green')
                    B.drawTmpEdges(tmpEdges)
                    
                    girl.queue.pop(girl.queue.index(boy_name))
                    
                    # Say no to other
                    for boy_name2 in girl.queue:
                        if(boy_name2 in [m.Name for m in mass_M]): 
                            boy = [ m for m in mass_M if m.Name==boy_name2][0]
                            boy.current_priority+=1
                            
                            waitPrint(f"{girl.Name} say 'No' to {boy_name2}", secFast)
                            B.blinkEdge(tmpEdges,(boy.Name,girl.Name))
                            tmpEdges.pop(tmpEdges.index((boy.Name, girl.Name)))
                            B.drawTmpEdges(tmpEdges)
                            
                    girl.queue.clear()
                else:              
                    waitPrint(f"{girl.Name} say 'Wait' to {boy.Name}", secFast)
                    B.blinkEdge(tmpEdges,(boy.Name,girl.Name))
            
            
            else:
                waitPrint("Error")
                
                

    waitPrint() 
    
    for m in mass_M:
        if(m.current_priority==len(m.priorities)-1):
            B.setVertexColor(m.Name, 'red')        
            waitPrint(f"{m.Name} out")
    for g in mass_G:
        if(g.current_priority==len(g.priorities)-1):
            B.setVertexColor(g.Name, 'red')
            waitPrint(f"{g.Name} out")
    
    # deliting married (and out)
    mass_M = [m for m in mass_M if m.married==False and m.current_priority<len(m.priorities)-1]
    mass_G = [g for g in mass_G if g.married==False and g.current_priority<len(g.priorities)-1]

    B.draw()
    plt.pause(1)
    

mass_M = mass_M_origin
mass_G = mass_G_origin

# set to -1 who not married
for m in mass_M:
    if(not m.married):
        B.setVertexColor(m.Name, 'red')
        m.current_priority=-1
for g in mass_G:
    if(not g.married):
        B.setVertexColor(g.Name, 'red')
        g.current_priority=-1


B.draw()


waitPrint("Results:",secFast)
waitPrint(mass_M_origin,secFast)
waitPrint(mass_G_origin,secFast)
print("end")
# plt.show()


plt.figure()
plt.hist([m.current_priority for m in mass_M], bins=linspace(-1-0.5, len(mass_G)+1+0.5      ))
plt.hist([m.current_priority for m in mass_M if m.current_priority==-1], bins=linspace(-1-0.5, len(mass_G)+1+0.5      ))
# plt.axis([-2,55,0,55])
plt.figure()
plt.hist([g.current_priority for g in mass_G],  bins=linspace(-1-0.5, len(mass_M)+1+0.5      ))
plt.hist([g.current_priority for g in mass_G if g.current_priority==-1], bins=linspace(-1-0.5, len(mass_M)+1+0.5      ))
# plt.axis([-2,55,0,55])
plt.show()










