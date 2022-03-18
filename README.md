# Labyrinth Generator

This is a program made in python and visualized in pygame that creates a random Labyrinth inside a grid.

## Use

The user first decides the size of the grid of the labyrinth. The width:height ratio is 3:2.
Then by pressing on a random block inside the grid, creates the starting point of the labyrinth.
Pressing space clears the grid, pressing r takes the user back to choosing the grid size.
There also options to change the parameters d which indicates the probability of the path to continue straight and
p which indicates the probability a new branch-path can be generated from a current path. When the labyrinth has been
finished the user can click again to empty blocks to create or add new paths and complexity to the labyrinth.
Finally the save button saves the grid in a csv file and the current labyrinth image in png form.

## Algorithm

The main classes used are Labyrinth and Node. Labyrinth initializes the grid and inserts Nodes to the path.
The class Node describes each block of the path and has some useful methods like has_children , can_insert ect.

The algorithm used to generate the labyrinth is using a queue logic. The labyrinth at the beginning is empty.
By choosing a starting point the user creates the first Node and added to a queue. The first Node from the queue is
removed and inserted in the labyrinth grid if possible (if there are no adjacent nodes , apart from parent). Each Node 
added checks its neighbors inside the labyrinth,if they are empty adds them to a list of children. Then a new node from
that list, is chosen to be added to the queue. If d is high, a child that continues with the same direction as the
previous two nodes, is chosen (if it exists). Otherwise, another child is chosen at random. If the parameter p is high a
second child will be chosen, creating a new path. The new Nodes are added to the queue and tha process is repeated until
until the queue is empty.
