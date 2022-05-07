from tkinter import *
from Main_Page import directed, weighted
from collections import defaultdict

currNum = 1

nodeValues = []
adj_list = defaultdict(list)

START_NODE = 0
GOAL_NODE = 0

def addNode():

    singleNodeFrame = Frame(nodesFrame, width = 70, height=70)
    global currNum
    CurrNodeLabel = Label(singleNodeFrame, text = currNum)
    CurrNodeLabel.pack()

    nodeValues.append(currNum)

    currNum = currNum+1 
    

    # ---------- Will use this in entering heuristics -------------------
    # heurLabel = Label(singleNodeFrame, text = "Enter Node Heuristic")
    # heurInput = Text(singleNodeFrame, height = 1, width = 4)  
    # heurLabel.pack()
    # heurInput.pack()  

    # def submitNode():
    #     addNodesBtn['state'] = NORMAL
    #     submitNodeBtn['state'] = DISABLED
    
    # submitNodeBtn = Button(singleNodeFrame, text = "Submit Node", command = submitNode)
    # submitNodeBtn.pack()

    singleNodeFrame.pack(side = LEFT)


def LockNodes():
    addEdgesBtn['state'] = NORMAL
    addNodesBtn["state"] = DISABLED
    LockNodesBtn['state'] = DISABLED




def addEdge():
    addEdgesBtn['state'] = DISABLED

    singleEdgeFrame = Frame(GraphInputPage, width=100, height=170)  
    
    src = StringVar()
    src.set( "Select Source" )
    srcDrop = OptionMenu( singleEdgeFrame , src , *nodeValues)
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
        LockEdgesBtn["state"] = NORMAL
        weightInput.config(state = DISABLED)

        srcNode, destNode = src.get(), dest.get()
        
        weight = 0

        if weighted:
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
    printGraph()

    start = StringVar()
    goal = StringVar()

    start.set("Select Start Node")
    goal.set("Select Goal Node")
    startAndGoalFrame = Frame(GraphInputPage, width=30, height=30)
    startNodeDrop = OptionMenu(startAndGoalFrame, start, *nodeValues)
    goalNodeDrop = OptionMenu(startAndGoalFrame, goal, *nodeValues)

    startNodeDrop.pack()
    goalNodeDrop.pack()



    def submitStartAndEnd():
        global START_NODE
        global GOAL_NODE
        START_NODE = start.get()
        GOAL_NODE = goal.get()

    submitStartAndEndBtn = Button(startAndGoalFrame, text = "Submit Start and Goal Node", command = submitStartAndEnd)
    submitStartAndEndBtn.pack()

    startAndGoalFrame.pack(side = BOTTOM)
        # ---------- Will use this in entering heuristics -------------------
    # heurLabel = Label(singleNodeFrame, text = "Enter Node Heuristic")
    # heurInput = Text(singleNodeFrame, height = 1, width = 4)  
    # heurLabel.pack()
    # heurInput.pack()  

    # def submitNode():
    #     addNodesBtn['state'] = NORMAL
    #     submitNodeBtn['state'] = DISABLED
    
    # submitNodeBtn = Button(singleNodeFrame, text = "Submit Node", command = submitNode)
    # submitNodeBtn.pack()

def printGraph():

    for node in adj_list:
        for edges in adj_list[node]:
            print(node, "-->", edges[0], edges[1])




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

LockEdgesBtn= Button(GraphInputPage, text="Click to lock all edges",  state = DISABLED, command= lockEdges)
LockEdgesBtn.pack()


GraphInputPage.mainloop()