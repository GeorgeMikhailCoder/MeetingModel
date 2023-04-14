import networkx as nx
import matplotlib.pyplot as plt
   
class myGraph():
    def __init__(self, names_M, names_G, colors, pause, display=True):
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
        self.display = display
    
    def setPauseBlink(self, pause):
        self.pauseBlink=pause
    
    def setVertexColor(self, vertex, color):
        self.colorMap[list(self.B.nodes).index(vertex)] = color
    
    def addConstEdge(self, edge):
        self.constEdges += [edge]
        self.B.add_edges_from([edge])
    
    def draw(self):
        if self.display:
            plt.clf()
            nx.draw(self.B, with_labels=True, font_weight='bold', pos=self.pos, node_color=self.colorMap, node_size=2000)
            plt.show(block=False)
    
    def drawTmpEdges(self, edgesDashed):
        if self.display:
            plt.clf()
            self.draw()        
            self.B.add_edges_from(edgesDashed)
            nx.draw_networkx_edges(self.B,pos=self.pos, style='dashed')
            plt.show(block=False)
            self.B.remove_edges_from(edgesDashed)
    
    def blinkEdge(self, edgesDashed1, edgeBlink, numOfBlink=3):
        if self.display:
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
            