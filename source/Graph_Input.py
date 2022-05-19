import sys
from tkinter import *
from tkinter.ttk import Combobox
from turtle import right
from Main_Page import directed, weighted
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
GOAL_NODES = []

alg = Algorithms()

def submitStartNode():
    global START_NODE
    startNode = start.get()
    START_NODE = Node.get_node(int(startNode))
    nx.set_node_attributes(G,{START_NODE.name:{'color': "cyan"}})
    updateGraph()


def submitGoalNode():
    global GOAL_NODES
    goalNode = goal.get()
    tempNode = Node.get_node(int(goalNode))
    GOAL_NODES.append(tempNode)
    nx.set_node_attributes(G, {tempNode.name: {'color': "orange"}})
    updateGraph()

def printGraph():

    for node in adj_list:
        for edges in adj_list[node]:
            print(node, "-->", edges[0], edges[1])

def run_DFS():
    alg.reset()                                 # consider moving this to the beginning of the algorithm itself Todo
    alg.dfs(START_NODE, GOAL_NODES)
    animate_solution(alg.get_visited_path())


def run_ID():
    alg.reset()                                 # consider moving this to the beginning of the algorithm itself Todo
    alg.iterative_deepening(START_NODE, GOAL_NODES, sys.maxsize)
    animate_solution(alg.get_visited_path())

def run_BFS():
    alg.reset()                                 # consider moving this to the beginning of the algorithm itself Todo
    alg.bfs(START_NODE, GOAL_NODES)
    animate_solution(alg.get_visited_path())

def run_greedy_best_first_search():
    alg.reset()                                 # consider moving this to the beginning of the algorithm itself Todo
    alg.greedy_best_first_search(START_NODE, GOAL_NODES)
    animate_solution(alg.get_visited_path())

def run_A_star():
    alg.reset()                                 # consider moving this to the beginning of the algorithm itself Todo
    alg.A_star_search(START_NODE, GOAL_NODES)
    animate_solution(alg.get_visited_path())    

def run_dijkstra():
    alg.reset()                                 # consider moving this to the beginning of the algorithm itself Todo
    alg.dijkstra(START_NODE, GOAL_NODES)
    animate_solution(alg.get_visited_path())


def openPopup():
    


    def closeWindow():
        heuristicsPage.destroy()
        heuristicsPage.update()
    
    def reset():
        for widgets in heuristicsPage.winfo_children():
            widgets.destroy()
        putInput(0)
    
    def putInput(i):
        if i >= len(nodes):
            submitAll = Button( heuristicsPage, text = "Submit All Values", command= closeWindow)
            clearAll = Button( heuristicsPage, text = "Clear All Values", command= reset)

            submitAll.pack()
            clearAll.pack()

            return
        
        addHeurLabel = Label (heuristicsPage, text = nodes[i].name)
        HeurInput = Text(heuristicsPage, height = 1, width = 4)

        submitHeuristic = Button( heuristicsPage, text = "Submit Heuristic", 
        command= lambda: setHeur(HeurInput, submitHeuristic,nodes[i], i) )

        addHeurLabel.pack()
        HeurInput.pack()
        submitHeuristic.pack()


    def setHeur(heurInput: Text, submitHeuristic:Button, node:Node, i):
        node.heuristic = int (heurInput.get('1.0', END))
        heurInput["state"] = DISABLED
        submitHeuristic["state"] = DISABLED
        putInput(i+1)


    heuristicsPage = Toplevel(GraphInputPage)
    heuristicsPage.title('Heuristics Input')   
    putInput(0)
    GraphInputPage.wait_window(heuristicsPage)



def runAlgo():
    alg.START_NODE = START_NODE                # this if for depth limited path calculation Todo
    algo = selectedAlgorithm.get()
    if algo == "Iterative Deepening":
        run_ID()
    
    elif algo == "Depth First Search":
        run_DFS()
    
    elif algo == "Breadth First Search":
        run_BFS()
    
    elif algo == "Dijkstra":
        run_dijkstra()
    
    elif algo == "Depth Limited":
        print ("dL")
    
    elif algo == "Greedy Best First Search":
        openPopup()
        run_greedy_best_first_search()

    elif algo == "A*":
        openPopup()
        run_A_star()
    
    totalLabel['text'] = "Total cost = " + str(alg.get_total_cost())

        

G=nx.Graph()

if (directed):
    G = nx.DiGraph()

path = []
visited_ID = []  # iterative deepening visited lists
color_map = []
i = int(-1)
ani = None


def draw():
    global color_map
    positions = graphviz_layout(G, prog="dot", root=0)
    nx.draw(G, pos=positions, with_labels=True, node_color=color_map, edgecolors="black")
    if (weighted == True):
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
    updateGraph()


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
    updateGraph()


def updateGraph():
    global color_map
    plt.clf()
    color_map = list(nx.get_node_attributes(G, "color").values())
    draw()
    canvas.draw()



def addNode():
    global currNum
    nodeValues.append(currNum)
    tempNode = Node(currNum, 1)
    nodes.append(tempNode)

    currNum = currNum+1 

    updateComboBoxes()
    G.add_node(tempNode.name, heuristic=tempNode.heuristic, color="white")
    updateGraph()


def updateComboBoxes():
    src.set( "Select Source" )

    dest.set("Select Destination")
    srcDrop['values'] = nodeValues
    destDrop['values'] = nodeValues

    startNodeDrop['values'] = nodeValues
    goalNodeDrop['values'] = nodeValues
    weightInput.delete('1.0', END)
    resetSandG()


def addEdge():
    srcNode, destNode = src.get(), dest.get()
    srcNode = Node.get_node(int(srcNode))
    destNode = Node.get_node(int(destNode))
        
    weight = 0

    if weighted:
        weight = int (weightInput.get("1.0",END))

    temp = [destNode, weight]
    adj_list[srcNode].append (temp)

    if directed == FALSE: 
        temp = [srcNode, weight]
        adj_list[destNode].append (temp)

    updateComboBoxes()

    
    G.add_edge(srcNode.name, destNode.name,
               w=weight)  # w instead of weight to avoid graphvis dot layout from changing edge lengths

    updateGraph()

def resetSandG_colors():
    global START_NODE, GOAL_NODES
    if (START_NODE != 0):
        nx.set_node_attributes(G, {START_NODE.name: {'color': "white"}})
    for node in GOAL_NODES:
        nx.set_node_attributes(G, {node.name: {'color': "white"}})
    updateGraph()

def resetSandG():
    start.set( "Select Start Node" )

    goal.set("Select Goal Node")

    global START_NODE, GOAL_NODES
    resetSandG_colors()
    START_NODE = 0
    GOAL_NODES.clear()

def resetGraph():
    global currNum, START_NODE
    nodes.clear()
    currNum = 0
    nodeValues.clear()
    START_NODE = 0
    GOAL_NODES.clear()
    adj_list.clear()
    updateComboBoxes()
    G.clear()
    updateGraph()

    print("RESET SUCCESSFUL")

GraphInputPage = Tk()
GraphInputPage.title('Graph Input')


fig = plt.figure()
canvas = FigureCanvasTkAgg(fig, GraphInputPage)
canvas.draw()
canvas.get_tk_widget().pack(side=RIGHT, fill=Y)

nodesAndEdgesFrame =  Frame(GraphInputPage, width=350)
nodesAndEdgesFrame.pack( side=LEFT, fill=Y)

##########################################  ADDING NODES #############################################################

nodesFrame = Frame(nodesAndEdgesFrame, highlightbackground="black", highlightthickness=1, width=350, height=80)
nodesFrame.pack(ipady=7)
nodesFrame.pack_propagate(0)

addNodesLabel = Label (nodesFrame, text = "Adding Nodes")
addNodesLabel.pack(ipady=8)

addNodesBtn= Button(nodesFrame, text="Add a new Node", command= addNode)
addNodesBtn.pack(ipadx=3, ipady=3)


##########################################  ADDING EDGES #############################################################


edgesFrame = Frame(nodesAndEdgesFrame, highlightbackground="black", highlightthickness=1, width=350, height=130)
edgesFrame.pack(ipady=20)
edgesFrame.pack_propagate(0)

addEdgesLabel = Label (edgesFrame, text = "Adding Edges")
addEdgesLabel.pack(ipady=10)

src = StringVar()
src.set( "Select Source" )

dest = StringVar() 
dest.set( "Select Destination" )

weightFrame = Frame(edgesFrame, width=250)
label = Label(weightFrame, text = "Enter Weight")
weightInput = Text(weightFrame, height = 1, width = 4)
label.pack(side=LEFT, ipadx= 3)
weightInput.pack(side=LEFT)

srcDrop = Combobox(edgesFrame, textvariable = src, values= nodeValues)
srcDrop['state'] = "readonly"
srcDrop.pack(ipady=2) 

destDrop = Combobox(edgesFrame, textvariable = dest, values= nodeValues)
destDrop['state'] = "readonly"
destDrop.pack(ipady=2)  


if weighted == TRUE:
    weightFrame.pack(ipady = 5)


addEdgeBtn = Button(edgesFrame, text = "Add Edge", command = addEdge)
addEdgeBtn.pack(ipadx=3, ipady=3)



##########################################  SELECTING START AND GOAL #########################################################


startAndGoalFrame = Frame(nodesAndEdgesFrame, highlightbackground="black", highlightthickness=1, width=350, height=110)
startAndGoalFrame.pack()


startFrame = Frame(startAndGoalFrame, width=350)
startFrame.pack()

startNodeLabel = Label(startFrame, text = "Start Node: ")
start = StringVar()
start.set("Select Start Node")
startNodeDrop = Combobox(startFrame, textvariable = start, values= nodeValues, width=15)
startNodeDrop['state'] = 'readonly'
startNodeLabel.pack(side=LEFT, ipadx=5)
startNodeDrop.pack(side=LEFT)
submitStartNodeBtn = Button(startFrame, text="Submit Start Node", state=NORMAL, command=submitStartNode)
submitStartNodeBtn.pack(ipady=3, side=RIGHT)


goalFrame = Frame(startAndGoalFrame, width=350)
goalFrame.pack()

goalNodeLabel = Label(goalFrame, text = "Goal Node(s): ")
goal = StringVar()
goal.set("Select Goal Node")
goalNodeDrop = Combobox(goalFrame, textvariable = goal, values= nodeValues, width=15)
goalNodeDrop['state'] = 'readonly'
goalNodeLabel.pack(side=LEFT, ipadx=5)
goalNodeDrop.pack(side=LEFT)
submitStartNodeBtn = Button(goalFrame, text="Submit Goal Node", state=NORMAL, command=submitGoalNode)
submitStartNodeBtn.pack(ipady=3, side=RIGHT)


resetStartAndGoal = Button(startAndGoalFrame, text = "Reset Start and Goal Nodes", command= resetSandG)
resetStartAndGoal.pack(side=BOTTOM, ipady=3)

startAndGoalFrame.pack_propagate(0)



##########################################  SELECTING ALGORITHM #############################################################

algoFrame = Frame(nodesAndEdgesFrame, highlightbackground="black", highlightthickness=1, width=350, height=70)
algoFrame.pack(ipady=10)
algoFrame.pack_propagate(0)

label3 = Label(algoFrame, text = "Select an Algorithm")
selectedAlgorithm = StringVar()
selectedAlgorithm.set("Select Algorithm")
algorithmsDrop = Combobox(algoFrame, textvariable = selectedAlgorithm, values= [
    "Iterative Deepening", 
    "Depth First Search",
    "Breadth First Search",
    "Dijkstra",
    "Depth Limited",
    "Greedy Best First Search",
    "A*"
    ])
algorithmsDrop['state'] = 'readonly'

testAlgoBtn = Button(algoFrame, text="Test Algorithm", state=NORMAL, command=runAlgo)

label3.pack(ipady=3)
algorithmsDrop.pack()
testAlgoBtn.pack(side=BOTTOM, ipady=3)

##########################################  SOLUTION ANIMATIONS #############################################################

solutionsAnimationsFrame = Frame(nodesAndEdgesFrame,  highlightbackground="black", highlightthickness=1, width=350, height=110)
solutionsAnimationsFrame.pack(ipady=10)
solutionsAnimationsFrame.pack_propagate(0)

testAlgo = Button(solutionsAnimationsFrame, text="Show Path", state=NORMAL, command=show_solution_path)
testAlgo.pack()

testAlgo = Button(solutionsAnimationsFrame, text="Show Visited", state=NORMAL, command=show_visited)
testAlgo.pack()

testAlgo = Button(solutionsAnimationsFrame, text="Show Visited ID", state=NORMAL, command=show_visited_ID)
testAlgo.pack()

totalLabel = Label (solutionsAnimationsFrame, text = "Total Cost= 0")
totalLabel.pack()

resetGraphBtn = Button(solutionsAnimationsFrame, text="RESET GRAPH", fg= "red", state=NORMAL, command=resetGraph)
resetGraphBtn.pack(ipady=5, ipadx=5, side=BOTTOM)


GraphInputPage.mainloop()

# Todo
# can there be no path from source to destination node (source node is a leaf node in a directed graph)
# can there be isolated parts in the graph (node with no edges connected to it, or an isolated tree)?
# there will be a button for only showing the visited nodes for iterative deepening 
# (this one is different from the one used in the other algorithms)
# add back button for changing the graph type (directed, undirected, weighted, unweighted)

