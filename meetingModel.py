
from numpy.random import randint, shuffle
from myGraph import myGraph

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
    
    
class MeetingModel:
    def __init__(self, nM=5, nG=5,  names_M=None, names_G=None, consoleOutput=True, graphOutput=True, consoleShortDelay=0.1, consoleLongDelay=2) -> None:
        rand_M, rand_G = MeetingModel.randNames(nM,nG)
        if(isinstance(names_M, list)):
            self.names_M = names_M
        else:
            self.names_M = rand_M
        
        if(isinstance(names_G, list)):
            self.names_G = names_G
        else:
            self.names_G = rand_G
        
        self.consoleOutput=consoleOutput
        self.graphOutput=graphOutput
        self.secFast=consoleShortDelay
        self.secSlow=consoleLongDelay
        
        self.mass_M = []
        self.mass_G = []
        self.marriedList = []
    
    def loadTestNames(self):
        self.names_M = ["Misha", "Yegor", "Aleks", "Andey","Pavel"]
        self.names_G = ["Marin", "Masha", "Yulia", "Daria", "Lerra"]
    
    def waitPrint(self, message="", sec=-1):
        if self.consoleOutput or not self.consoleOutput and self.graphOutput:
            if not self.consoleOutput and self.graphOutput:
                sec=self.secFast
            if(message=="" and sec==-1):
                sec=self.secFast
            if(sec==-1):
                sec=self.secSlow
            if(sec == 'Fast'):
                sec=self.secFast
            if(sec == 'Slow'):
                sec=self.secSlow
                
            if self.consoleOutput:  
                print(message)
            plt.pause(sec)
            
    
    def myShuffle(seq):
        seq2 = seq.copy()
        shuffle(seq2)
        return seq2
    
    def randNames(nM,nG=-1):
        if(nG==-1):
            nG=nM
        names_M = ["Pupil_M"+str(i) for i in range(nM)]
        names_G = ["Pupil_G"+str(i) for i in range(nG)]
        return names_M,names_G
    
    def randPeople(self):
        k_priorities_M = [randint(1,len(self.names_G)) for name in self.names_M];
        k_priorities_G = [randint(1,len(self.names_M)) for name in self.names_G];

        mass_M = [ Pupil(name, 'M', MeetingModel.myShuffle(self.names_G)[0:randint(1, len(self.names_G))])
                for name in self.names_M
                ]
        mass_G = [ Pupil(name, 'G', MeetingModel.myShuffle(self.names_M)[0:randint(1, len(self.names_M))])
                for name in self.names_G
                ]
        return mass_M, mass_G
    
    def processModel(self, consoleOutput=None, graphOutput=None):
        if not consoleOutput is None: self.consoleOutput=consoleOutput
        if not graphOutput is None: self.graphOutput=graphOutput
        
        mass_M_origin, mass_G_origin = self.randPeople()
        mass_M, mass_G = mass_M_origin, mass_G_origin

        self.mass_M = mass_M_origin
        self.mass_G = mass_G_origin

        for m in mass_M:
            self.waitPrint(m.selfDescribe(),'Fast')
        self.waitPrint(sec='Fast')
        for g in mass_G:
            self.waitPrint(g.selfDescribe(),'Fast')
        self.waitPrint(sec='Fast')

        B = myGraph(self.names_M, self.names_G, ['#00A2E8' for node in self.names_M + self.names_G], self.secFast, self.graphOutput)

        marriedList = []
        tmpEdges = []
        dayNum = 0
        while not (len(mass_G)==0 or len(mass_M)==0):
            dayNum+=1
            self.waitPrint(f"process, day {dayNum}")
            
            # boys ask    
            for boy in mass_M:
                while boy.current_priority < len(boy.priorities):
                    girl_name = boy.priorities[boy.current_priority]
                    if(girl_name in [g.Name for g in mass_G]):
                        girl = [ g for g in mass_G if g.Name==girl_name][0]
                        if not boy.Name in girl.queue: girl.queue.append(boy.Name)
                        if not (boy.Name, girl_name) in tmpEdges: tmpEdges.append((boy.Name, girl_name)) # for graph
                        B.drawTmpEdges(tmpEdges)
                        self.waitPrint(boy.Name + " goes to "+girl.Name) # for console
                        break
                    else:
                        boy.current_priority+=1
                if(boy.current_priority == len(boy.priorities)-1):
                    B.setVertexColor(boy.Name, 'red')
                    self.waitPrint(f"{boy.Name} out")
            B.drawTmpEdges(tmpEdges) # for graph
            self.waitPrint()
            
            # girls answer
            for girl in mass_G:
                
                # define self priority
                while girl.priorities[girl.current_priority] not in [m.Name for m in mass_M] and girl.current_priority<len(girl.priorities)-2:
                    girl.current_priority+=1
                self.waitPrint(f"{girl.Name} checkout priority {girl.current_priority}")
                
                # say 'no'
                for boy_name in girl.queue:
                    if(boy_name in [m.Name for m in mass_M]):
                        boy = [ m for m in mass_M if m.Name==boy_name][0]
                        
                        if not boy_name in girl.priorities: 
                            boy.current_priority+=1
                            girl.queue.pop(girl.queue.index(boy_name)) # correct mistake
                            tmpEdges.pop(tmpEdges.index((boy.Name, girl.Name)))
                            
                            self.waitPrint(f"{girl.Name} say 'No' to {boy_name}",'Fast')
                            B.blinkEdge(tmpEdges,(boy.Name,girl.Name))
                            B.drawTmpEdges(tmpEdges)
                            
                    
                    else:
                        self.waitPrint("Error")
                    
                
                for boy_name in girl.queue:
                    if(boy_name in [m.Name for m in mass_M]):
                        boy = [ m for m in mass_M if m.Name==boy_name][0]
                        
                        
                        if(boy_name == girl.priorities[girl.current_priority]):
                        
                            # Say yes to him
                            
                            boy.married = True
                            girl.married = True
                            
                            self.waitPrint(f"{girl.Name} say 'Yes' to {boy.Name}, they married", 'Fast')
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
                                    
                                    self.waitPrint(f"{girl.Name} say 'No' to {boy_name2}", 'Fast')
                                    B.blinkEdge(tmpEdges,(boy.Name,girl.Name))
                                    tmpEdges.pop(tmpEdges.index((boy.Name, girl.Name)))
                                    B.drawTmpEdges(tmpEdges)
                                    
                            girl.queue.clear()
                        else:              
                            self.waitPrint(f"{girl.Name} say 'Wait' to {boy.Name}", 'Fast')
                            B.blinkEdge(tmpEdges,(boy.Name,girl.Name))
                    
                    
                    else:
                        self.waitPrint("Error")
                        
                        

            self.waitPrint() 
            
            for m in mass_M:
                if(m.current_priority==len(m.priorities)-1):
                    B.setVertexColor(m.Name, 'red')        
                    self.waitPrint(f"{m.Name} out")
            for g in mass_G:
                if(g.current_priority==len(g.priorities)-1):
                    B.setVertexColor(g.Name, 'red')
                    self.waitPrint(f"{g.Name} out")
            
            # deliting married (and out)
            mass_M = [m for m in mass_M if m.married==False and m.current_priority<len(m.priorities)-1]
            mass_G = [g for g in mass_G if g.married==False and g.current_priority<len(g.priorities)-1]

            B.draw()
            self.waitPrint()
            

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


        self.waitPrint("Results:",'Fast')
        self.waitPrint(mass_M_origin,'Fast')
        self.waitPrint(mass_G_origin,'Fast')
        self.waitPrint("end",0)
        
        self.marriedList = marriedList
        B.display=True
        return mass_G.copy(), mass_M.copy(), marriedList.copy(), B
