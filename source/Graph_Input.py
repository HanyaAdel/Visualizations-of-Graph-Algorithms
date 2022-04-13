import simpleguitk as simplegui

# Constants
HEIGHT = 400
WIDTH = 500
NODE_SPACE_ALLOWANCE = 20
NODE_COLOR = "Red"
EDGE_COLOR = "Yellow"
EDGE_SIZE = 2
NODE_LABEL_COLOR = "White"

setNodesRelation = False
draw_relations = False
draw_mark_relations =  False
placeNodes = True
setGoal = False
setStart = False
displayResult = False
pos_lock = False
lock_nodes = False

nodes = []
pos1 = [0,0]
pos2 = [0,0]
current_node_letters_up = []
current_node_letters_low = []
letter_label_default = '@'
letter_pos = 1

class Point:
    def __init__(self,pos,node_colour):
        self.pos = pos
        self.children = []
        self.radius = 5
        self.colour = node_colour
        self.index = 0
        self.is_mark = False
        self.label = '@'

    def draw(self,canvas):
        canvas.draw_circle(self.pos, self.radius, 6, self.colour)


def button_refresh_new_relation():
    global pos_lock, pos1, pos2, nodes, draw_relations, draw_mark_relations
    
    if lock_nodes == False and setNodesRelation == True:
        pos_lock = False
        draw_mark_relations = False
        draw_relations = False
        pos1[0] = 0
        pos1[1] = 0
        pos2[0] = 0
        pos2[1] = 0

        # This empties the list of children attribute of Point class
        for i, child in enumerate(nodes):
            del nodes[i].children[:]
    else:
        print ("Warning: This action is not allowed.")


def button_lock_nodes():
    global placeNodes, setNodesRelation, current_node_letters_up, nodes, current_node_letters_low
    
    # Can only lock nodes if the set-up is right
    # Prevents locking nodes later in the program
    if placeNodes == True and setNodesRelation == False and setStart == False and setGoal == False:
        placeNodes = False
        setNodesRelation = True
        
        # Fills two new lists of all node labels(letters) 
        # for later use in input start and goal
        if nodes:
            for n, obj in enumerate(nodes):
                current_node_letters_up.append(nodes[n].label)

            for let in current_node_letters_up:
                current_node_letters_low.append(let.lower())

        print ("The nodes are now locked in!")
    else:
        print ("Warning: This action is not allowed.")

def button_lock_graph():
    global placeNodes, setNodesRelation, nodes, lock_nodes
    
    if setNodesRelation is True:
        placeNodes = False
        setNodesRelation = False
        lock_nodes = True

        # Sets the index of nodes list and apply it to each index attribute of Point class
        # for index/element reference only, for later use in BFS and DFS functions
        for d, dot in enumerate(nodes):
            nodes[d].index = d
            print ("node"+str(d+1)+":", nodes[d].label)
            
            # This is important
            # This sorts the elements of children attribute list in ascending order
            nodes[d].children.sort()

        print ("Graph is now set!")
    else:
        print ("Warning: This action is not allowed.")


def input_start_handler(start_string):
    global start, nodes, setStart
    
    setStart = False
    if start_string.isdigit():
        # Allows number as input for starting node
        # 1 for A, 2 for B and so on and so forth
        temp_start = int(start_string) - 1
        for element, num in enumerate(nodes):
            if temp_start == element:
                
                # Minus one because node label starts at 1 not zero(index)
                start = temp_start
                print ("Start:", chr(start+65))
                setStart = True
                break 
        if setStart == False:  
            print ("Warning: This number is outside of the nodes!")
    else:
        # Allows letter as input for starting node
        if start_string in current_node_letters_up:
            start = ord(start_string) - 65
            setStart = True
            print ("Start:", chr(start+65))
        else:
            if start_string in current_node_letters_low:
                start = ord(start_string) - 97
                setStart = True
                print ("Start:", chr(start+65))
            else:
                print ("Warning: Unknown input. Enter a number or the node letter.")


def input_goal_handler(goal_string):
    global goal, nodes, setGoal
    
    setGoal = False
    if goal_string.isdigit():
        
        # Allows number as input for goal node
        # 1 for A, 2 for B and so on and so forth
        temp_goal = int(goal_string) - 1
        for element, num in enumerate(nodes):
            if temp_goal == element:
                #minus one because node label starts at 1 not zero(index)
                goal = temp_goal
                print ("Goal:", chr(goal+65))
                setGoal = True
                break
        if setGoal == False:
            print ("Warning: This number is outside of the nodes!")
    else:
        # Allows letter as input for goal node
        if goal_string in current_node_letters_up:
            goal = ord(goal_string) - 65
            setGoal = True
            print ("Goal:", chr(goal+65))
        else:
            if goal_string in current_node_letters_low:
                goal = ord(goal_string) - 97
                setGoal = True
                print ("Goal:", chr(goal+65))
            else:
                print ("Warning: Unknown input. Enter a number or the node letter.")



def mouseclick(pos):
    global pos1, pos2, pos_lock, indx, draw_relations, draw_mark_relations, nodes, indx_mark_color
    global letter_label_default, letter_pos
    
    # Creates new instance of point(node) if the last position of
    # the mouseclick is not on  top of a previous node
    allow_place_node = True
    
    if placeNodes == True:
        if nodes: # Checks if the nodes are not empty
            for p, location in enumerate(nodes):
                if ((pos[0] >= (nodes[p].pos[0]-NODE_SPACE_ALLOWANCE) and pos[0] <= (nodes[p].pos[0]+NODE_SPACE_ALLOWANCE)) and
                    (pos[1] >= (nodes[p].pos[1]-NODE_SPACE_ALLOWANCE) and pos[1] <= (nodes[p].pos[1]+NODE_SPACE_ALLOWANCE))):
                    print ("Warning: Cannot create node on top of another node!")
                    allow_place_node = False
                    break
            # Creates new instance of Point class if no nodes detected in 
            # the vicinity of mouseclick position
            if allow_place_node == True:
                nodes.append(Point(pos,NODE_COLOR))
                nodes[-1].label = chr(ord(letter_label_default) + letter_pos)
                letter_pos += 1
        # Else creates a node for first time 
        else:  
            nodes.append(Point(pos,NODE_COLOR))
            nodes[-1].label = chr(ord(letter_label_default) + letter_pos)
            letter_pos += 1
    
    # Sets up the edges or links
    if setNodesRelation == True:
        
        # If mouseclick pos is on top of a current node mark that node
        for i, position in enumerate(nodes):
            if ((pos[0] >= (nodes[i].pos[0]-NODE_SPACE_ALLOWANCE) and pos[0] <= (nodes[i].pos[0]+NODE_SPACE_ALLOWANCE)) and
                (pos[1] >= (nodes[i].pos[1]-NODE_SPACE_ALLOWANCE) and pos[1] <= (nodes[i].pos[1]+NODE_SPACE_ALLOWANCE))):
                if pos_lock == False:
                    pos1[0] = pos[0]
                    pos1[1] = pos[1]
                    
                    indx = i
                    indx_mark_color = i
                    pos_lock = True
                    draw_mark_relations = True
                    break

                else:
                    # If it is the second node that is not the same of 
                    # the first marked node, then creates a new relation/edge
                    if i != indx:
                        pos2[0] = pos[0]
                        pos2[1] = pos[1]
                        nodes[indx].children.append(i)
                        nodes[i].children.append(indx)
                        
                        pos_lock = False
                        draw_relations = True
                        draw_mark_relations = False
                        break
                    else:
                        print ("Warning: Recursion or self loop is not allowed.")


def draw_handler(canvas):
    global result_string, queue_string, pointer_string
    global placeNodes, setNodesRelation, setStart, setGoal, pos1
    
    # Draws nodes
    if draw_mark_relations == True and setNodesRelation == True:
        canvas.draw_circle(nodes[indx_mark_color].pos, 15, 3, "Yellow", "Black")

    if nodes: 
        for i, vertex in enumerate(nodes):
            nodes[i].draw(canvas)
            canvas.draw_text(nodes[i].label, (nodes[i].pos[0]-30, nodes[i].pos[1]), 20, NODE_LABEL_COLOR)

    # Draws edges
    if draw_relations == True:
        for n, point in enumerate(nodes):
            if nodes[n].children: 
                for child in nodes[n].children:
                    canvas.draw_line(nodes[n].pos, nodes[child].pos, EDGE_SIZE, EDGE_COLOR)

    # Display results
    if displayResult == True:
        canvas.draw_text(pointer_string, (30, 345), 15, NODE_LABEL_COLOR)
        canvas.draw_text(result_string, (30, 370), 15, NODE_LABEL_COLOR)
        canvas.draw_text(queue_string, (30, 395), 15, NODE_LABEL_COLOR)


# Creates the frame window
frame = simplegui.create_frame("Graph Input",WIDTH,HEIGHT)

frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw_handler)

# Button, input and label controls for the frame window
button1 = frame.add_button('Lock in the nodes', button_lock_nodes)
label1 = frame.add_label(' ')

button2 = frame.add_button('Lock in the graph', button_lock_graph)
label2 = frame.add_label(' ')

button3 = frame.add_button('Reset edge drawing', button_refresh_new_relation)
label3 = frame.add_label(' ')

input_start = frame.add_input('Set start', input_start_handler, 50)
label4 = frame.add_label(' ')

input_goal = frame.add_input('Set goal', input_goal_handler, 50)
label5 = frame.add_label(' ')



# Program starts here
frame.start()