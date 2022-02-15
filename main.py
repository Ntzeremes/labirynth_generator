import random
import pygame
import copy
import time

pygame.init()


class Node:
    """A node is a part of the path. Each node is connected with the previous one, called parent.
    All the nodes connected create the path"""

    propagate_chance = 0.5
    parents_direction = 0.65

    def __init__(self, parent, pos):
        self.parent = parent
        self.pos_x = pos[0]
        self.pos_y = pos[1]

    def can_insert(self, labyrinth):
        n = 0
        for i in range(2):
            for j in range(2):
                x = self.pos_x + i * (-1) ** j
                y = self.pos_y + (1 - i) * (-1) ** j
                if 0 <= x < labyrinth.size and 0 <= y < labyrinth.size:
                    if labyrinth.grid[x][y] is not None:
                        n += 1
        return True if n == 1 else False

    def neighbors(self, labyrinth):
        """checking the grid positions on the top, bottom, left and right of the Node.
        The parent node is excluded."""

        neighbors = []

        # Adding neighbors that are on top, bottom , right and left in the labyrinth
        # and we have not visited them so far.

        # top
        if self.pos_y - 1 >= 0:
            if labyrinth.grid[self.pos_x][self.pos_y - 1] is None:
                n = 0
                for i in range(2):
                    for j in range(2):
                        x = self.pos_x + i * (-1) ** j
                        y = self.pos_y - 1 + (1 - i) * (-1) ** j
                        if 0 <= x < labyrinth.size and 0 <= y < labyrinth.size:
                            if labyrinth.grid[x][y] is not None:
                                n += 1
                if n == 1:
                    neighbors.append((self.pos_x, self.pos_y - 1))
        # bottom
        if self.pos_y + 1 < labyrinth.size:
            if labyrinth.grid[self.pos_x][self.pos_y + 1] is None:
                n = 0
                for i in range(2):
                    for j in range(2):
                        x = self.pos_x + i * (-1) ** j
                        y = self.pos_y + 1 + (1 - i) * (-1) ** j
                        if 0 <= x < labyrinth.size and 0 <= y < labyrinth.size:
                            if labyrinth.grid[x][y] is not None:
                                n += 1
                if n == 1:
                    neighbors.append((self.pos_x, self.pos_y + 1))
        # left
        if self.pos_x - 1 >= 0:
            if labyrinth.grid[self.pos_x - 1][self.pos_y] is None:
                n = 0
                for i in range(2):
                    for j in range(2):
                        x = self.pos_x - 1 + i * (-1) ** j
                        y = self.pos_y + (1 - i) * (-1) ** j
                        if 0 <= x < labyrinth.size and 0 <= y < labyrinth.size:
                            if labyrinth.grid[x][y] is not None:
                                n += 1
                if n == 1:
                    neighbors.append((self.pos_x - 1, self.pos_y))
        # right
        if self.pos_x + 1 < labyrinth.size:
            if labyrinth.grid[self.pos_x + 1][self.pos_y] is None:
                n = 0
                for i in range(2):
                    for j in range(2):
                        x = self.pos_x + 1 + i * (-1) ** j
                        y = self.pos_y + (1 - i) * (-1) ** j
                        if 0 <= x < labyrinth.size and 0 <= y < labyrinth.size:
                            if labyrinth.grid[x][y] is not None:
                                n += 1
                if n == 1:
                    neighbors.append((self.pos_x + 1, self.pos_y))

        return neighbors

    def children(self, lab):
        """choosing the child node of the current node"""
        neighbors = self.neighbors(lab)

        if not neighbors:
            return None
        second_child = None

        # Giving the same direction coming from parent a higher chance
        if self.parent:

            i = random.random()
            # keep parent's direction,it has a higher chance
            parents_direction_node = (2 * self.pos_x - self.parent[0], 2 * self.pos_y - self.parent[1])
            if parents_direction_node in neighbors:
                if len(neighbors) == 1 or i < Node.parents_direction:
                    first_child = Node((self.pos_x, self.pos_y), parents_direction_node)
                # else choose randomly between the other neighbors
                else:
                    neighbors.remove(parents_direction_node)
                    first_child = Node((self.pos_x, self.pos_y), random.choice(neighbors))
            else:
                first_child = Node((self.pos_x, self.pos_y), random.choice(neighbors))
        else:
            first_child = Node((self.pos_x, self.pos_y), random.choice(neighbors))

        l = len(neighbors)

        if l == 0:
            return None
        elif l > 1:
            propagate = random.random()
            if propagate < Node.propagate_chance :
                neighbors.remove((first_child.pos_x, first_child.pos_y))
                second_child = Node((self.pos_x, self.pos_y), random.choice(neighbors))

        if second_child:
            return [first_child, second_child]

        return [first_child]


class Labyrinth:
    """The class that creates the n x n grid of the labyrinth. Initially it is filled with None values, the path
    is represented by values 0. Also has some basic functions for extra utility and manipulation and the function that
    creates the path."""

    def __init__(self, size):
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.size = size
        self.screen = None
        self.block = None

    # noinspection PyTypeChecker
    def insert(self, x, y):
        """inserts a node in grid and prints it"""
        self.grid[x][y] = 0
        if self.screen:
            pygame.draw.rect(self.screen, (150, 150, 150),
                             (x * self.block + 1, y * self.block + 1, self.block - 1, self.block - 1))

    def print_grid(self):
        for i in range(self.size):
            print(self.grid[i])
            print()

    def set_visual_p(self, screen, block):
        self.screen = screen
        self.block = block

    def path(self, x, y):
        """This function generates a random path inside the grid.
        The path starts at a random point at the edge of a grid and has fixed length"""

        # Choosing starting point at the edge of the grid. Corners are excluded
        side = random.choice([0, 1, 2, 3])  # 0 is left side, 1 is top etc
        position = random.randint(1, self.size - 1)

        current_nodes = [Node(None, (x, y))]
        self.insert(current_nodes[0].pos_x, current_nodes[0].pos_y)
        while current_nodes:
            current_node = current_nodes.pop(0)
            if current_node.can_insert(self):
                self.insert(current_node.pos_x, current_node.pos_y)
            children = current_node.children(self)
            if children:
                current_nodes.extend(children)

            yield None


def visualize_path_creation(screen_size):
    """It is a helper function that visualizes the creation of the path.
    Created to check the process for bugs."""

    screen = pygame.display.set_mode(screen_size)
    screen.fill((50, 50, 50))
    terminate = False
    lab = Labyrinth(20)

    # creating the grid
    block = screen_size[0] // lab.size
    for i in range(lab.size - 1):
        pygame.draw.line(screen, (0, 0, 0), ((i + 1) * block, 0), ((i + 1) * block, screen_size[0]))
        pygame.draw.line(screen, (0, 0, 0), (0, (i + 1) * block), (screen_size[0], (i + 1) * block))

    lab.set_visual_p(screen, block)

    pygame.display.flip()
    clock = pygame.time.Clock()
    start = False
    while not terminate:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate = True

            if not start:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = int((event.pos[0]) // block)
                    y = int((event.pos[1]) // block)
                    path = lab.path(x, y)
                    start = True

        if start:
            try:
                next(path)
            except StopIteration:
                start = False

        pygame.display.flip()


visualize_path_creation((800, 800))

