import pygame
from pygame.locals import *
import random
from pprint import pprint as pp


class GameOfLife:
    def __init__(self, width = 640, height = 480, cell_size = 10, speed = 10):

        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.screen_size = width, height

        self.screen = pygame.display.set_mode(self.screen_size)

        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        self.empty_color = 'white'
        self.line_color = 'black'
        self.cell_color = 'blue'

        self.speed = speed

    def draw_grid(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color(self.line_color), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color(self.line_color), (0, y), (self.width, y))

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        gen = 0
        pygame.display.set_caption('Game of Life: {} generation'.format(gen))
        self.screen.fill(pygame.Color('white'))
        self.clist = self.cell_list()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_cell_list(self.clist)
            pygame.display.set_caption('Game of Life: {} generation'.format(gen))
            gen += 1
            pygame.display.flip()
            clist2 = self.clist.copy()
            self.clist = self.update_cell_list(clist2)
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize=True):
        if randomize:
            self.cell_list = [[random.randrange(0,2) for x in range(self.width // self.cell_size)] for y in range(self.height // self.cell_size)]
            return self.cell_list
        pass

    def draw_cell_list(self, rects):
        x, y = 0, 0
        total = 0
        alive, nd = 0, 0
        for row in range(len(rects)):
            for elem in range(len(rects[row])):
                total += 1
                if rects[row][elem] == 1:
                    pygame.draw.rect(self.screen, pygame.Color(self.cell_color), (x+1, y+1, self.cell_size-1, self.cell_size-1))
                    x += self.cell_size
                    alive+=1

                else:
                    pygame.draw.rect(self.screen,pygame.Color(self.empty_color),(x+1,y+1,self.cell_size-1,self.cell_size-1))
                    x += self.cell_size
                    nd+=1
            x = 0
            y += self.cell_size

    def get_neighbours(self, cell):
        row, col = cell
        neighbours_list = []
        pos = [[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[-1,1],[0,1],[1,1]]
        for j in pos:
            if (0 <= row + j[0] < self.height // self.cell_size) and (0<=col+j[1]<self.width//self.cell_size):
                neighbours_list.append(self.clist[row+j[0]][col+j[1]])
            else:
                neighbours_list.append(0)
        return neighbours_list

    def update_cell_list(self, cells):
        y, x = 0, 0
        updated_cell_list = []
        cell_list = cells.copy()
        for i in range(len(cell_list)):
            updated_cell_list.append([])
            for j in range(len(cell_list[i])):
                updated_cell_list[i].append(0)
        for row in cell_list:
            for col in row:
                if (col == 1):
                    if (1 < self.get_neighbours((y, x)).count(1) < 4):
                        updated_cell_list[y][x] = 1
                    else:
                        updated_cell_list[y][x] = 0
                else:
                    if (self.get_neighbours((y, x)).count(1)==3):
                        updated_cell_list[y][x] = 1
                    else:
                        updated_cell_list[y][x] = 0
                x += 1
            x = 0
            y += 1

        pp(updated_cell_list)

        return updated_cell_list


if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()
