from audioop import add
from tkinter import *
from Main_Page import directed, weighted

nodes = list()
currLetter = "A"
adj_list = {}

GraphInputPage = Tk()
GraphInputPage.geometry('200x550')
GraphInputPage.title('Graph Input')

def addNode():
    global nodes
    global currLetter
    nodes.append(currLetter)
    currLetter = chr(ord(currLetter)+1) 
    print(currLetter)

def printGraph():
  for node in adj_list:
    print(node, " ---> ", [i for i in adj_list[node]])

def AddEdge(node1, node2, weight):
    print ("clickedd")
    temp = []
    if node1 in nodes and node2 in nodes:
        if node1 not in adj_list:
            temp.append([node2,weight])
            adj_list[node1] = temp
   
        elif node1 in adj_list:
            temp.extend(adj_list[node1])
            temp.append([node2,weight])
            adj_list[node1] = temp
    
    printGraph()


def ShowAddingEdgesMenu():
    src = StringVar() 
    src.set( "Select Source" )
    srcDrop = OptionMenu( GraphInputPage , src , *nodes )
    srcDrop.pack() 

    dest = StringVar() 
    dest.set( "Select Destination" )
    destDrop = OptionMenu( GraphInputPage , dest , *nodes )
    destDrop.pack()   

    weight = 0
    if weighted == TRUE:
        label = Label(GraphInputPage, text = "enter weight")
        T = Text(GraphInputPage, height = 5, width = 10)  
        label.pack()
        T.pack()
        weight = T.get("1.0",END)
    
    addBtn = Button(GraphInputPage, text = "Add", command = AddEdge(src, dest, weight))
    addBtn.pack()


def LockNodes():
    print("Locked Nodes")  
    addEdgesBtn= Button(GraphInputPage, text="Add Edge", command= ShowAddingEdgesMenu)
    addEdgesBtn.pack()
    



label = Label(GraphInputPage, text = " ")
label.pack()
button1= Button(GraphInputPage, text="Add Node", command= addNode)
button1.pack(ipadx=10, ipady=10)

label2 = Label(GraphInputPage, text = " ")
label2.pack()
LockNodesBtn= Button(GraphInputPage, text="Lock Nodes", command= LockNodes)
LockNodesBtn.pack(ipadx=10, ipady=10)


GraphInputPage.mainloop()