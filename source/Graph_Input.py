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

alg = Algorithms()

def addNode():

    global currNum
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


def LockNodes():
    addEdgesBtn['state'] = NORMAL
    addNodesBtn["state"] = DISABLED
    LockNodesBtn['state'] = DISABLED


def addEdge():
    for widgets in singleEdgeFrame.winfo_children():
      widgets.destroy()

    addEdgesBtn['state'] = DISABLED
    LockEdgesBtn["state"] = DISABLED
    
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

    singleEdgeFrame.pack()

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

def run_DFS():
    alg.reset()                                 # consider moving this to the beginning of the algorithm itself Todo
    alg.dfs(START_NODE, GOAL_NODE)
    # animate_solution(alg.get_visited_path())


def run_ID():
    alg.reset()                                 # consider moving this to the beginning of the algorithm itself Todo
    alg.iterative_deepening(START_NODE, GOAL_NODE, sys.maxsize)
    # animate_solution(alg.get_visited_path())


G = nx.DiGraph()

path = []
visited_ID = []  # iterative deepening visited lists
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
    # G = G.to_undirected()             # consider this for changing the graph from directed to undirected Todo

    color_map = list(nx.get_node_attributes(G, "color").values())
    fig.clear()
    color_map[int(path[i])] = "red"
    i += 1
    draw()


def animate_solution(visited_path = alg.get_visited_path()):
    global path
    global i
    i = int(-1)
    path = visited_path
    # nx.draw_networkx(G, pos=positions, with_labels=True)
    ani = animation.FuncAnimation(fig, animate, frames=len(path), interval=700, repeat=False)
    update()


def show_solution_path(solution_path=alg.get_path()):
    global color_map
    color_map = list(nx.get_node_attributes(G, "color").values())     # consider making this a reset_color_map func Todo
    for node in solution_path:
        color_map[int(node)] = "yellow"
    draw()
    canvas.draw()  # check if you need this


def show_visited(visited=alg.get_visited()):
    global color_map
    color_map = list(nx.get_node_attributes(G, "color").values())
    for node in visited:
        color_map[int(node)] = "green"
    draw()
    canvas.draw()


def animate_visited(frame):
    global i
    global visited_ID
    global color_map
    color_map = list(nx.get_node_attributes(G, "color").values())
    fig.clear()
    for node in visited_ID[i]:
        color_map[int(node)] = "green"
    i += 1
    draw()


def show_visited_ID(visited=alg.get_visited_ID()):  # show visited for iterative improvement
    global visited_ID
    global i
    visited_ID = visited
    i = int(-1)
    ani = animation.FuncAnimation(fig, animate_visited, frames=len(visited), interval=700, repeat=False)
    update()


def add_node(node_name, heuristic):
    G.add_node(node_name, heuristic=heuristic, color="white")
    update()


def add_edge(source, destination, weight):
    G.add_edge(source, destination,
               w=weight)  # w instead of weight to avoid graphvis dot layout from changing edge lengths
    update()


def update():
    global color_map
    plt.clf()
    color_map = list(nx.get_node_attributes(G, "color").values())
    draw()
    canvas.draw()


GraphInputPage = Tk()
GraphInputPage.geometry('900x800')
GraphInputPage.title('Graph Input')
fig = plt.figure()
canvas = FigureCanvasTkAgg(fig, GraphInputPage)
canvas.draw()
canvas.get_tk_widget().pack(side=RIGHT, fill=Y)

nodesAndEdgesFrame =  Frame(GraphInputPage, highlightbackground="blue", highlightthickness=2, width=250, height=600)
nodesAndEdgesFrame.pack(side=LEFT)
nodesAndEdgesFrame.pack_propagate(0)

nodesFrame = Frame(nodesAndEdgesFrame, highlightbackground="red", highlightthickness=2,width=250, height=300)
nodesFrame.pack()
nodesFrame.pack_propagate(0)

addNodesLabel = Label (nodesFrame, text = "Adding Nodes")
addNodesLabel.pack(ipady=20)

addNodesBtn= Button(nodesFrame, text="Click to add new node", command= addNode)
addNodesBtn.pack(ipadx=10, ipady=10)

LockNodesBtn= Button(nodesFrame, text="Click to lock all nodes", command= LockNodes)
LockNodesBtn.pack(ipadx=10, ipady=10)

edgesFrame = Frame(nodesAndEdgesFrame, width=250, height=400)
edgesFrame.pack()
edgesFrame.pack_propagate(0)

singleEdgeFrame = Frame(edgesFrame, width=250, height=200)

addEdgesBtn= Button(edgesFrame, text="Click to add new edge", state = DISABLED, command= addEdge)
addEdgesBtn.pack()

LockEdgesBtn= Button(edgesFrame, text="Click to lock all edges",  state = DISABLED, command= lockEdges)
LockEdgesBtn.pack()

algoFrame = Frame(nodesAndEdgesFrame, width=250, height=200)
algoFrame.pack()
algoFrame.pack_propagate(0)

testAlgo = Button(GraphInputPage, text="Test Algorithm ID", state=NORMAL, command=run_ID)
testAlgo.pack()

testAlgo = Button(GraphInputPage, text="Test Algorithm DFS", state=NORMAL, command=run_DFS)
testAlgo.pack()

testAlgo = Button(GraphInputPage, text="Show Path", state=NORMAL, command=show_solution_path)
testAlgo.pack()

testAlgo = Button(GraphInputPage, text="Show Visited", state=NORMAL, command=show_visited)
testAlgo.pack()

testAlgo = Button(GraphInputPage, text="Show Visited ID", state=NORMAL, command=show_visited_ID)
testAlgo.pack()

testAlgo = Button(GraphInputPage, text="Animate Solution", state=NORMAL, command=animate_solution)
testAlgo.pack()

GraphInputPage.mainloop()

# Todo
# I can't see the test algo button (I changed it to be in the main frame for now)
# can there be no path from source to destination node (source node is a leaf node in a directed graph)
# can there be isolated parts in the graph (node with no edges connected to it, or an isolated tree)?
# the select source/goal for the algorithm can be just disabled (there is currently a bug where whenever you click on lock edges a new instance of those is created)
# there is no need for the lock nodes/edges buttons
# there will be a button for only showing the visited nodes for iterative deepening (this one is different from the one used in the other algorithms)
# increase graph canvas area
# when the window is minimized some buttons (the ones responsible for the source/goal nodes) are partially hidden by the canvas
# fix the multiple windows bug
# there is no need for the add edge button you can just reset the two lists when you hit submit edge
# should we show the algorithm animation by default or have a button for it
# we can probably add nodes and edges simultaneously
# should we include all the algorithms in one class?
# add reset graph button
# add back button for changing the graph type (directed, undirected, weighted, unweighted)

