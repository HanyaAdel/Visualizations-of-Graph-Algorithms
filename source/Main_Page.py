import tkinter as tk

directed = False
weighted = False



root = tk.Tk()
root.geometry('700x550')
root.title('Main Page')


var2 = tk.BooleanVar(root)
var1 = tk.BooleanVar(root)

def setDirectedOrNot():
    directed = var1.get()

def setWeightedOrNot():
    weighted = var2.get()

def gotoGraphInput():
    root.destroy()
    import Graph_Input

title = tk.Label(root, text = "Simulate Graph Search Algorithms!")
title.config(font=("Courier", 23))
title.pack() 



DirectedOrNot = tk.Label(root, text = "Is the graph directed?")
DirectedOrNot.config(font=("Courier", 15))
DirectedOrNot.pack() 


R1 = tk.Radiobutton(root, text="YES", variable=var1, value=True,
                  command=setDirectedOrNot)
R1.pack()

R2 = tk.Radiobutton(root, text="NO", variable=var1, value=False,
                  command=setDirectedOrNot)
R2.pack()



WeightedOrNot = tk.Label(root, text = "Is the graph weighted?")
WeightedOrNot.config(font=("Courier", 15))
WeightedOrNot.pack() 


R3 = tk.Radiobutton(root, text="YES", variable=var2, value=True,
                  command=setWeightedOrNot)
R3.pack()

R4 = tk.Radiobutton(root, text="NO", variable=var2, value=False,
                  command=setWeightedOrNot)
R4.pack()






button1= tk.Button(root, text="Graph!", command= gotoGraphInput)
button1.pack(pady=10)


root.mainloop()