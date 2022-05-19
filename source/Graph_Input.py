import sys
from tkinter import *
from tkinter.ttk import Combobox

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
directed = False
weighted = False
START_NODE = 0
GOAL_NODES = []

alg = Algorithms()
algo = ""           #algorithm being used

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
    alg.reset()                             
    alg.dfs(START_NODE, GOAL_NODES)
    animate_solution(alg.get_visited_path())


def run_ID():
    alg.reset()                                
    alg.iterative_deepening(START_NODE, GOAL_NODES)
    animate_solution(alg.get_visited_path())

def run_BFS():
    alg.reset()                               
    alg.bfs(START_NODE, GOAL_NODES)
    animate_solution(alg.get_visited_path())

def run_greedy_best_first_search():
    alg.reset()                                
    alg.greedy_best_first_search(START_NODE, GOAL_NODES)
    animate_solution(alg.get_visited_path())

def run_A_star():
    alg.reset()                                
    alg.A_star_search(START_NODE, GOAL_NODES)
    animate_solution(alg.get_visited_path())    

def run_dijkstra():
    alg.reset()                              
    alg.dijkstra(START_NODE, GOAL_NODES)
    animate_solution(alg.get_visited_path())


def noSolutionPopup():
    noSolution = Toplevel(GraphInputPage)
    noSolution.title('Error')   

    label4 = Label (noSolution, text = "There's No path")
    label4.pack(ipadx= 50, ipady=50)
    GraphInputPage.wait_window(noSolution)


def runAlgo():
    global algo
    alg.START_NODE = START_NODE             
    algo = selectedAlgorithm.get()
    if algo == "Iterative Deepening":
        run_ID()

    elif algo == "Depth First Search":
        run_DFS()
    
    elif algo == "Breadth First Search":
        run_BFS()
    
    elif algo == "Dijkstra":
        run_dijkstra()

    elif algo == "Greedy Best First Search":
        run_greedy_best_first_search()

    elif algo == "A*":
        run_A_star()

    if (alg.found == False):
        noSolutionPopup()

    totalLabel['text'] = "Total cost = " + str(alg.get_total_cost())

G=nx.Graph()

path = []
visited_ID = []  # iterative deepening visited lists
color_map = []
edge_colors = []
i = int(-1)
ani = None

def generate_labels():
    global nodeValues
    labels = {}
    heuristics = nx.get_node_attributes(G,'heuristic')
    for node in nodeValues:
        temp = str(node)+"\nh : "+str(heuristics[node])
        labels[node]=temp
    return labels

def draw():
    global color_map
    positions = graphviz_layout(G, prog="dot", root=0)
    nx.draw(G, pos=positions,labels = generate_labels(), with_labels=True, node_color=color_map, edgecolors="black",
            node_size=2000,edge_color=edge_colors)
    if (weighted == True):
        nx.draw_networkx_edge_labels(G, positions, edge_labels=nx.get_edge_attributes(G, 'w'), font_size=10,
                                 rotate=False)
   


def animate(frame):
    global i
    global G
    global color_map
    global path
   

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
 
    ani = animation.FuncAnimation(fig, animate, frames=len(path), interval=700, repeat=False)
    updateGraph()

def set_path_edge_colors():
    global edge_colors
    temp = alg.get_path()
    for i in range(0,len(temp)-1):
        nx.set_edge_attributes(G, {(temp[i], temp[i + 1]): {"color":"yellow"}})
    edge_colors = [G[u][v]['color'] for u, v in G.edges]

def reset_path_edge_colors():
    global edge_colors
    temp = alg.get_path()
    for i in range(0, len(temp) - 1):
        nx.set_edge_attributes(G, {(temp[i], temp[i + 1]): {"color": "black"}})
    edge_colors = [G[u][v]['color'] for u, v in G.edges]

def show_solution_path(solution_path=alg.get_path()):
    global color_map
    color_map = list(nx.get_node_attributes(G, "color").values())
    set_path_edge_colors()
    for node in solution_path:
        color_map[int(node)] = "yellow"
    draw()
    canvas.draw()  # check if you need this
    reset_path_edge_colors()


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

def display_visited():
    global algo
    if(algo=="Iterative Deepening"):
        show_visited_ID()
    else:
        show_visited()

def updateGraph():
    global color_map, edge_colors
    plt.clf()
    color_map = list(nx.get_node_attributes(G, "color").values())
    edge_colors = list(nx.get_edge_attributes(G,"color").values())
    draw()
    canvas.draw()



def addNode():
    global currNum
    nodeValues.append(currNum)
    heur = int (HeurInput.get("1.0",END))
    tempNode = Node(currNum, heur)
    nodes.append(tempNode)
    print(tempNode.heuristic)
    currNum = currNum+1

    HeurInput.delete('1.0', END)
    HeurInput.insert(END, '0')
    G.add_node(tempNode.name, heuristic=tempNode.heuristic, color="white")
    updateGraph()
    updateComboBoxes()


def updateComboBoxes():
    src.set( "Select Source" )

    dest.set("Select Destination")
    srcDrop['values'] = nodeValues
    destDrop['values'] = nodeValues

    startNodeDrop['values'] = nodeValues
    goalNodeDrop['values'] = nodeValues
    weightInput.delete('1.0', END)
    resetSandG()                    # Todo Consider removing this method call


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
               w=weight,color = "black")

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


def showGraphOptionsPopup():
    def setDirectedOrNot():
        global directed
        directed = var1.get()
        

    def setWeightedOrNot():
        global weighted
        weighted = var2.get()
        
    
    def closeWindow():
        setWeightedOrNot()
        setDirectedOrNot()
        resetGraphOptions()
        
        graphOptions.destroy()
        graphOptions.update()
    

    graphOptions = Toplevel(GraphInputPage)
    graphOptions.title('New Graph Options')  
    x = GraphInputPage.winfo_x()
    y = GraphInputPage.winfo_y()
    graphOptions.geometry("+%d+%d" % (x + 400, y + 100))
    

    label4 = Label (graphOptions, text = "Enter the Options for the next Graph")
    label4.pack(ipadx= 10, ipady=10)
    
    DirectedOrNot = Label(graphOptions, text = "Is the graph directed?")
    DirectedOrNot.pack(ipady=5) 


    var1 = BooleanVar(graphOptions)
    
    R1 = Radiobutton(graphOptions, text="YES", variable=var1, value=True, command=setDirectedOrNot)
    R1.pack()

    R2 = Radiobutton(graphOptions, text="NO", variable=var1, value=False, command=setDirectedOrNot)
    R2.pack()


    WeightedOrNot = Label(graphOptions, text = "Is the graph weighted?")
    WeightedOrNot.pack(ipady=5) 

    var2 = BooleanVar(graphOptions)
    

    R3 = Radiobutton(graphOptions, text="YES", variable=var2, value=True, command=setWeightedOrNot)
    R3.pack()

    R4 = Radiobutton(graphOptions, text="NO", variable=var2, value=False, command=setWeightedOrNot)
    R4.pack()

    button1= Button(graphOptions, text="Graph!", command= closeWindow)
    button1.pack(pady=10)

    GraphInputPage.wait_window(graphOptions)


def resetGraphOptions():
    global weighted, directed

    if weighted == True:
        weightFrame.pack(ipady = 5)
    else:
        weightFrame.pack_forget()
    
    global G
    if (directed == True):
        G = nx.DiGraph()
    else:
        G = nx.Graph()

    
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
    totalLabel['text'] = "Total Cost= 0"
    showGraphOptionsPopup()
    



GraphInputPage = Tk()
GraphInputPage.title('Graph Input')


fig = plt.figure()
canvas = FigureCanvasTkAgg(fig, GraphInputPage)
canvas.draw()
canvas.get_tk_widget().pack(side=RIGHT, fill=Y)

nodesAndEdgesFrame =  Frame(GraphInputPage, width=350)
nodesAndEdgesFrame.pack( side=LEFT, fill=Y)

##########################################  ADDING NODES #########################################################

nodesFrame = Frame(nodesAndEdgesFrame, highlightbackground="black", highlightthickness=1, 
                width=350, height=95)
nodesFrame.pack(ipady=7)
nodesFrame.pack_propagate(0)

addNodesLabel = Label (nodesFrame, text = "Adding Nodes")
addNodesLabel.pack(ipady=8)

addHeurLabel = Label (nodesFrame, text = "Enter Node Heuristic")
HeurInput = Text(nodesFrame, height = 1, width = 4)
HeurInput.insert(END, "0")

addHeurLabel.pack()
HeurInput.pack()

addNodesBtn= Button(nodesFrame, text="Add a new Node", command= addNode)
addNodesBtn.pack(ipadx=3, ipady=3)


##########################################  ADDING EDGES ########################################################


edgesFrame = Frame(nodesAndEdgesFrame, highlightbackground="black", highlightthickness=1, 
            width=350, height=130)
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





addEdgeBtn = Button(edgesFrame, text = "Add Edge", command = addEdge)
addEdgeBtn.pack(ipadx=3, ipady=3)



##########################################  SELECTING START AND GOAL ##########################################


startAndGoalFrame = Frame(nodesAndEdgesFrame, highlightbackground="black", highlightthickness=1,
                     width=350, height=110)
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



##########################################  SELECTING ALGORITHM ##############################################

algoFrame = Frame(nodesAndEdgesFrame, highlightbackground="black", highlightthickness=1, 
                width=350, height=70)
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
    "Greedy Best First Search",
    "A*"
    ])
algorithmsDrop['state'] = 'readonly'

testAlgoBtn = Button(algoFrame, text="Test Algorithm", state=NORMAL, command=runAlgo)

label3.pack(ipady=3)
algorithmsDrop.pack()
testAlgoBtn.pack(side=BOTTOM, ipady=3)

##########################################  SOLUTION ANIMATIONS ################################################

solutionsAnimationsFrame = Frame(nodesAndEdgesFrame,  highlightbackground="black", highlightthickness=1, 
                            width=350, height=110)
solutionsAnimationsFrame.pack(ipady=10)
solutionsAnimationsFrame.pack_propagate(0)

testAlgo = Button(solutionsAnimationsFrame, text="Show Path", state=NORMAL, command=show_solution_path)
testAlgo.pack()

testAlgo = Button(solutionsAnimationsFrame, text="Show Visited", state=NORMAL, command=display_visited)
testAlgo.pack()

totalLabel = Label (solutionsAnimationsFrame, text = "Total Cost= 0")
totalLabel.pack()

resetGraphBtn = Button(solutionsAnimationsFrame, text="RESET GRAPH", fg= "red", state=NORMAL, command=resetGraph)
resetGraphBtn.pack(ipady=5, ipadx=5, side=BOTTOM)

GraphInputPage.after_idle(showGraphOptionsPopup)

GraphInputPage.mainloop()
