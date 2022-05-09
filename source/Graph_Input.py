import sys
from tkinter import *
from Main_Page import directed, weighted
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg
)
from networkx.drawing.nx_pydot import graphviz_layout

from Graph import Node, nodes,adj_list
from Algorithms import Algorithms

currNum = 0

nodeValues = []

START_NODE = 0
GOAL_NODE = 0

def addNode():

    singleNodeFrame = Frame(nodesFrame, width = 70, height=70)
    global currNum
    CurrNodeLabel = Label(singleNodeFrame, text = currNum)
    CurrNodeLabel.pack()

    nodeValues.append(currNum)
    tempNode = Node(currNum, 1)
    nodes.append(tempNode)
    add_node(tempNode.name, tempNode.heuristic)

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
        srcNode = Node.get_node(int(srcNode))
        destNode = Node.get_node(int(destNode))
        
        weight = 0

        if weighted:
            weight = int (weightInput.get("1.0",END))


        temp = [destNode, weight]
        adj_list[srcNode].append (temp)
        add_edge(srcNode.name,destNode.name,weight)
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
        START_NODE = Node.get_node(int(START_NODE))
        GOAL_NODE = Node.get_node(int(GOAL_NODE))
    submitStartAndEndBtn = Button(startAndGoalFrame, text = "Submit Start and Goal Node", command = submitStartAndEnd)
    submitStartAndEndBtn.pack()

    startAndGoalFrame.pack(side = BOTTOM)
def printGraph():

    for node in adj_list:
        for edges in adj_list[node]:
            print(node, "-->", edges[0], edges[1])

def testAlgo():
        alg = Algorithms()
        alg.iterative_deepening(START_NODE,GOAL_NODE,sys.maxsize)
        animate_solution(alg.get_visited_path(),alg.get_path())


G = nx.DiGraph()

path = []
sol = []
color_map = []
i = int(-1)
ani = None


def draw():
    global color_map
    positions = graphviz_layout(G, prog="dot", root=0)
    nx.draw_networkx(G, pos=positions, with_labels=True, node_color=color_map, edgecolors="black")
    nx.draw_networkx_edge_labels(G, positions, edge_labels=nx.get_edge_attributes(G, 'w'), font_size=10,
                                 rotate=False)
    # nx.draw_networkx_labels(G,pos=h_positions,labels=nx.get_node_attributes(G,"heuristic"))


def animate(frame):
    global i
    global G
    global color_map
    global path
    global sol
    # G = G.to_undirected()             # consider this for changing the graph from directed to undirected

    color_map = list(nx.get_node_attributes(G, "color").values())
    fig.clear()
    if i >= len(path):
        for node in sol:
            color_map[int(node)] = "yellow"
    else:
        color_map[int(path[i])] = "red"
    i += 1
    draw()


def animate_solution(visited_path, solution_path):
    global path
    global sol
    global i
    i = int(-1)
    path = visited_path
    sol = solution_path
    # nx.draw_networkx(G, pos=positions, with_labels=True)
    ani = animation.FuncAnimation(fig, animate, frames=len(path) + 1, interval=700, repeat=False)
    update()


def add_node(node_name, heuristic):
    G.add_node(node_name, heuristic=heuristic, color="white")
    update()


def add_edge(source, destination, weight):
    G.add_edge(source, destination, w=weight)    # w instead of weight to avoid graphvis dot layout from changing edge lengths
    update()


def update():
    global color_map
    plt.clf()
    color_map = list(nx.get_node_attributes(G, "color").values())
    draw()
    canvas.draw()


GraphInputPage = Tk()
GraphInputPage.geometry('700x550')
GraphInputPage.title('Graph Input')
fig = plt.figure()
canvas = FigureCanvasTkAgg(fig, GraphInputPage)
canvas.draw()
canvas.get_tk_widget().pack()

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

testAlgo= Button(GraphInputPage, text="Test Algorithm",  state = NORMAL, command= testAlgo)
testAlgo.pack()

GraphInputPage.mainloop()