from asyncio.windows_events import NULL
from tkinter import *
from Main_Page import directed, weighted
from collections import defaultdict


nodes = []
currLetter = "A"

adj_list = defaultdict(list)


class Node:
    def __init__(self, name : str, heur : int) :
        self.name = name
        self.heur = heur


def addNode():

    addNodesBtn['state'] = DISABLED
    singleNodeFrame = Frame(nodesFrame, width = 70, height=120)
    global currLetter
    CurrNodeLabel = Label(singleNodeFrame, text = currLetter)
    CurrNodeLabel.pack()

    heurLabel = Label(singleNodeFrame, text = "Enter Node Heuristic")
    heurInput = Text(singleNodeFrame, height = 1, width = 4)  
    heurLabel.pack()
    heurInput.pack()  

    def submitNode():
        addNodesBtn['state'] = NORMAL
        submitNodeBtn['state'] = DISABLED
        heurInput.config(state = DISABLED)

        global currLetter
        nodes.append(Node(currLetter, heurInput.get("1.0",END)))
        currLetter = chr(ord(currLetter)+1) 
        
        
    submitNodeBtn = Button(singleNodeFrame, text = "Submit Node", command = submitNode)
    submitNodeBtn.pack()

    singleNodeFrame.pack(side = LEFT)


def LockNodes():
    addEdgesBtn['state'] = NORMAL
    addNodesBtn["state"] = DISABLED
    LockNodesBtn['state'] = DISABLED




def addEdge():
    printGraph()
    addEdgesBtn['state'] = DISABLED

    singleEdgeFrame = Frame(GraphInputPage, width=100, height=170)  

    nodeValues = []
    for node in nodes:
        nodeValues.append(node.name)
    

    src = StringVar()
    src.set( "Select Source" )
    srcDrop = OptionMenu( singleEdgeFrame , src , *nodeValues )
    srcDrop.pack() 

    dest = StringVar() 
    dest.set( "Select Destination" )
    destDrop = OptionMenu( singleEdgeFrame , dest , *nodeValues )
    destDrop.pack()   

    label = Label(singleEdgeFrame, text = "enter weight")
    weightInput = Text(singleEdgeFrame, height = 1, width = 4)  
    if weighted == TRUE:
        label.pack()
        weightInput.pack()
        
    def submitEdge():
        addEdgesBtn["state"] = NORMAL
        submitEdgeBtn['state'] = DISABLED
        weightInput.config(state = DISABLED)

        srcNode, destNode = NULL, NULL

        for node in nodes:
            if node.name == src.get():
                srcNode = node
            if node.name == dest.get():
                destNode = node
        
        weight = int (weightInput.get("1.0",END))

        temp = [destNode, weight]
        adj_list[srcNode].append (temp)

        if directed == FALSE: 
            temp = [srcNode, weight]
            adj_list[destNode].append (temp)
        

    submitEdgeBtn = Button(singleEdgeFrame, text = "Submit Edge", command = submitEdge)
    submitEdgeBtn.pack()

    singleEdgeFrame.pack(side = LEFT)

def lockEdges():
    print("nodes locked")

def printGraph():
    for node in adj_list:
        for edges in adj_list[node]:
            print(node.name, "-->", edges[0].name, edges[1])




GraphInputPage = Tk()
GraphInputPage.geometry('700x550')
GraphInputPage.title('Graph Input')

nodesFrame = Frame(GraphInputPage, width=550, height=200)
nodesFrame.pack()
nodesFrame.pack_propagate(0)

addNodesLabel = Label (nodesFrame, text = "Adding Nodes")
addNodesLabel.pack()

addNodesBtn= Button(nodesFrame, text="Click to add new node", command= addNode)
addNodesBtn.pack(ipadx=10, ipady=10)

LockNodesBtn= Button(nodesFrame, text="Click to lock all nodes", command= LockNodes)
LockNodesBtn.pack(ipadx=10, ipady=10)

addEdgesBtn= Button(GraphInputPage, text="Click to add new edge", state = DISABLED, command= addEdge)
addEdgesBtn.pack()

LockEdgesBtn= Button(GraphInputPage, text="Click to lock all edges", command= lockEdges)
LockEdgesBtn.pack()


GraphInputPage.mainloop()