#!/usr/bin/python

'''Куб.
Зело забавен тем что демонстрирует честную трехмерную графику в масштабе трех с половиной строчек'''

from tkinter import Canvas, Tk, ALL
import time
import numpy
import numpy.matrixlib


c_size_half = 700 / 2


class Vertex:
    '''Вершина'''

    def __init__(self, coord_x=0, coord_y=0, coord_z=0):

        self.coord_x = coord_x
        self.coord_y = coord_y
        self.coord_z = coord_z
        self.depth = 0


class Cube:
    '''Кубик. Или не кубик.'''

    def __init__(self, vertices=[Vertex()]):

        self.vertices = vertices
        self.indices = [0, 1, 2, 3, 0, 4, 5, 6, 7, 4, 7, 6, 2, 6, 5, 1, 2, 3, 7]

    def get_depth(self):
        '''сасай'''

        for i in range(8):
            self.vertices[i].depth = 0

        zmin = -1000
        imin = 0

        for i in range(8):
            if zmin < self.vertices[i].coord_z:
                zmin = self.vertices[i].coord_z
                imin = i

        self.vertices[imin].depth = -1


    def draw(self):
        '''Рисовалка'''

        self.get_depth()
        for i in range(len(self.indices) - 1):
            if self.vertices[self.indices[i]].depth > -1 and self.vertices[self.indices[i + 1]].depth > -1:
                canvas.create_line(
                    self.vertices[self.indices[i]].coord_x + c_size_half,
                    self.vertices[self.indices[i]].coord_y + c_size_half,
                    self.vertices[self.indices[i + 1]].coord_x + c_size_half,
                    self.vertices[self.indices[i + 1]].coord_y + c_size_half,
                    fill="white")


def rotate(cube, a=1, axis=0):
    '''pep8 пидор'''

    a = (numpy.pi / 180) * a
    if axis == 0:
        rotate_mat = numpy.matrix([
            [1, 0, 0],
            [0, numpy.cos(a), -numpy.sin(a)],
            [0, numpy.sin(a), numpy.cos(a)]
        ])
    else:
        rotate_mat = numpy.matrix([
            [numpy.cos(a), 0, numpy.sin(a)],
            [0, 1, 0],
            [-numpy.sin(a), 0, numpy.cos(a)]
        ])

    for i in range(8):
        z = numpy.matrix([cube.vertices[i].coord_x,
                          cube.vertices[i].coord_y,
                          cube.vertices[i].coord_z])

        res = (z * rotate_mat).getT()
        cube.vertices[i].coord_x = float(res[0])
        cube.vertices[i].coord_y = float(res[1])
        cube.vertices[i].coord_z = float(res[2])


root = Tk()
root.title("Кубик")
canvas = Canvas(root, width=700, height=700, bg="black")
canvas.pack()

vertices = [
    Vertex(coord_x=-100, coord_y=-100, coord_z=-100),  # A
    Vertex(coord_x=-100, coord_y=-100, coord_z=100),  # B
    Vertex(coord_x=100, coord_y=-100, coord_z=100),  # C
    Vertex(coord_x=100, coord_y=-100, coord_z=-100),  # D

    Vertex(coord_x=-100, coord_y=100, coord_z=-100),  # E
    Vertex(coord_x=-100, coord_y=100, coord_z=100),  # F
    Vertex(coord_x=100, coord_y=100, coord_z=100),  # G
    Vertex(coord_x=100, coord_y=100, coord_z=-100),  # H
]

cube = Cube(vertices)

def motion(event):
    rotate(cube, a=-(event.x) / 100, axis=1)
    rotate(cube, a=(event.y) / 100, axis=0)


root.bind("<B1-Motion>", motion)

while True:

    canvas.delete(ALL)
    cube.draw()
    root.update()
    time.sleep(0.01)
