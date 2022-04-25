from tkinter import *
from Main_Page import directed, weighted



GraphInputPage = Tk()
GraphInputPage.geometry('700x550')
GraphInputPage.title('Graph Input')

def addNode():
    print("Add Node")

def LockNodes():
    print("Lock Nodes")    

button1= Button(GraphInputPage, text="Add Node", command= addNode)
button1.pack(pady=10, side = LEFT)

LockNodesBtn= Button(GraphInputPage, text="Lock Nodes", command= LockNodes)
LockNodesBtn.pack(pady=10, side = LEFT)


GraphInputPage.mainloop()