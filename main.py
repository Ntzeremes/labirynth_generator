import random
import pygame
import copy
import time

pygame.init()


class Node:
    """A node is a part of the path. Each node is connected with the previous one, called parent.
    All the nodes connected create the path"""

    def __init__(self, parent, pos, grid_size):
        self.parent = parent
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.grid_size = grid_size

    def neighbors(self, labyrinth):
        """checking the grid positions on the top, bottom, left and right of the Node.
        The parent node is excluded."""

        neighbors = []

        # Adding neighbors that are on top, bottom , right and left in the labyrinth
        # and we have not visited them so far.

        # top
        if self.pos_y - 1 >= 0:
            if labyrinth.grid[self.pos_x][self.pos_y - 1] is None:
                neighbors.append((self.pos_x, self.pos_y - 1))
        # bottom
        if self.pos_y + 1 < self.grid_size:
            if labyrinth.grid[self.pos_x][self.pos_y + 1] is None:
                neighbors.append((self.pos_x, self.pos_y + 1))
        # left
        if self.pos_x - 1 >= 0:
            if labyrinth.grid[self.pos_x - 1][self.pos_y] is None:
                neighbors.append((self.pos_x - 1, self.pos_y))
        # right
        if self.pos_x + 1 < self.grid_size:
            if labyrinth.grid[self.pos_x + 1][self.pos_y] is None:
                neighbors.append((self.pos_x + 1, self.pos_y))

        checked = copy.deepcopy(neighbors)
        for neighbor in neighbors:
            n = 0
            for i in range(2):
                for j in range(2):
                    x = neighbor[0] + i * (-1) ** j
                    y = neighbor[1] + (1 - i) * (-1) ** j
                    if 0 <= x < labyrinth.size and 0 <= y < labyrinth.size:
                        if labyrinth.grid[x][y] is not None:
                            n += 1
            if n > 1:
                checked.remove(neighbor)

        return checked

    def child(self, lab):
        """choosing the child node of the current node"""
        neighbors = self.neighbors(lab)

        if not neighbors:
            return None
        print(neighbors)

        # Giving the same direction coming from parent a higher chance
        if self.parent:
            direction = [-self.parent[0] + self.pos_x, -self.parent[1] + self.pos_y]

            i = random.random()
            # keep parent's direction,it has a higher chance
            parents_direction_node = (self.pos_x + direction[0], self.pos_y + direction[1])
            if parents_direction_node in neighbors:
                if len(neighbors) == 1 or i < 0.6:
                    return Node((self.pos_x, self.pos_y), parents_direction_node, self.grid_size)
                # else choose randomly between the other neighbors
                else:
                    neighbors.remove(parents_direction_node)
                    return Node((self.pos_x, self.pos_y), random.choice(neighbors), self.grid_size)
            else:
                return Node((self.pos_x, self.pos_y), random.choice(neighbors), self.grid_size)
        else:
            return Node((self.pos_x, self.pos_y), random.choice(neighbors), self.grid_size)


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
    def insert(self, node):
        """inserts a node in grid and prints it"""
        self.grid[node.pos_x][node.pos_y] = 0
        if self.screen:
            pygame.draw.rect(self.screen, (150, 150, 150),
                             (node.pos_x * self.block + 1, node.pos_y * self.block + 1, self.block - 1, self.block - 1))

    def print_grid(self):
        for i in range(self.size):
            print(self.grid[i])
            print()

    def set_visual_p(self, screen, block):
        self.screen = screen
        self.block = block

    def path(self, length):
        """This function generates a random path inside the grid.
        The path starts at a random point at the edge of a grid and has fixed length"""

        # Choosing starting point at the edge of the grid. Corners are excluded
        side = random.choice([0, 1, 2, 3])  # 0 is left side, 1 is top etc
        position = random.randint(1, self.size - 1)

        if side == 0:
            start = (0, position)
        elif side == 1:
            start = (position, 0)
        elif side == 2:
            start = (self.size - 1, position)
        else:
            start = (position, self.size - 1)

        current_node = Node(None, start, self.size)

        while current_node:
            self.insert(current_node)
            current_node = current_node.child(self)
            if current_node is None:
                print("No node")
                break

            yield self.grid


def visualize_path_creation(labyrinth, screen_size):
    """It is a helper function that visualizes the creation of the path.
    Created to check the process for bugs."""

    screen = pygame.display.set_mode(screen_size)
    screen.fill((50, 50, 50))
    terminate = False

    # creating the grid
    block = screen_size[0]//labyrinth.size
    for i in range(labyrinth.size - 1):
        pygame.draw.line(screen, (0, 0, 0), ((i + 1)*block, 0), ((i + 1)*block, screen_size[0]))
        pygame.draw.line(screen, (0, 0, 0), (0, (i + 1)*block), (screen_size[0], (i + 1)*block))

    labyrinth.set_visual_p(screen, block)
    path = labyrinth.path(40)

    pygame.display.flip()
    clock = pygame.time.Clock()

    while not terminate:
        clock.tick(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate = True

        try:
            next(path)
        except StopIteration:
            pass

        pygame.display.flip()


lab = Labyrinth(20)
visualize_path_creation(lab, (800, 800))
