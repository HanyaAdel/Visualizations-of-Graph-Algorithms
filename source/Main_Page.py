import tkinter as tk
from PIL import ImageTk, Image

directed = False
weighted = False

root = tk.Tk()
root.geometry('700x550')
root.title('Main Page')

root.config(bg = 'white')
def gotoGraphInput():
    root.destroy()
    import Graph_Input
    

title = tk.Label(root, text = "Simulate Graph Search Algorithms!")
title.config(font=("Courier", 23), bg='white')
title.pack(ipadx= 10,  ipady= 10) 


img = ImageTk.PhotoImage(Image.open("source/image.png"))
label = tk.Label(root, image = img)
label.config(bg='white')
label.pack()


button1= tk.Button(root, text="Start Graphing!", command= gotoGraphInput)
button1.config(font=("Courier", 15))
button1.pack(pady=20, ipadx=10)

root.mainloop()