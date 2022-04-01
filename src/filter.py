
"""
Smooth out image
"""

import pygame as pg
import matplotlib.pyplot as plt
import numpy as np
import math


def create_map(map, size, color):
    m = []

    for i in range(size[1]):
        m.append([])

        for j in range(size[0]):

            m[-1].append(color.get(map[i*size[0]+j].get_real_temp()))

    return m


def mid(*v):
    return int(sum(v)/len(v))

def middle(*p):
    return (mid(*[i[0] for i in p]), mid(*[i[1] for i in p]), mid(*[i[2] for i in p]))


def interpolate(map):
    start_length = len(map)
    m = [[] for i in range(len(map))]

    # in col direction
    for row in range(len(map)):

        for col in range(len(map[row])):

            if col < len(map[row])-1:
                m[row].append(map[row][col])
                m[row].append(middle(map[row][col], map[row][col+1]))

    # in row direction
    inbetween = [[] for i in range(len(map)-1)]
    for row in range(len(inbetween)):

        for col in range(len(m[0])):

            inbetween[row].append(middle(m[row][col], m[row+1][col]))

    # zip both list
    map = []
    for row in range(len(m)+len(inbetween)):

        if row % 2 == 0:
            map.append(m[math.ceil(row/2)])
        else:
            map.append(inbetween[math.floor(row/2)])

    return map


def smooth(map, factor):
    """
    Givet en 2 dimensionel liste, map, tegn et billed
    med en sløring, altså en jævning af værdierne

    Listen er givet såldes:
        map = [
            0,0,0
            0,2,0
            0,0,0
        ]

    Resultatet burde være (med en faktor på 2)
        map = [
            0,0,0,0,0
            0,0,1,0,0
            0,1,2,1,0
            0,0,1,0,0
            0,0,0,0,0
        ]

    Algoritmen kan køres n gange for at få en upscaling på ønsket
    Algoritmen gøres altså størrer for hver gang.

    Algoritmen fungerer således:
        for alle værdier i listen
            tag naboens værdi til højre og skab en ny med halvdelen af naboen og egen værdi
        for alle værdier i listen (nu er listen størrer)
            tag naboens værdi nederst og skab en ny værdi imellem

        Kør algoritemn til der er opnået en opfaktorering
    """

    #factor = math.log10(len(map)*upscale)/math.log10(len(map[0]))

    #return map
    for _ in range(factor):
        map = interpolate(map)

    return map



# VERSION 2 WITHOUT EXPANSION
def middle_square(map, row, col):
    n = [
        map[row][col], #use it twice for double effect -ish
        map[row][col],
        map[row][col+1],
        map[row][col-1],
        map[row+1][col],
        map[row-1][col]
    ]
    return middle(*n)


def interpolate_middle(map):

    m = [[] for i in range(len(map))]
    for row in range(len(map)):

        for col in range(len(map[row])):

            if len(map)-1 > row > 0   and   len(map[0])-1 > col > 0:
                m[row].append(middle_square(map, row, col))
            else:
                m[row].append(map[row][col])

    return m

def smooth_middle(map, times):

    for i in range(times):
        map = interpolate_middle(map)

    return map

# create a large map using the same methods as draw
def enlarge(map, factor):
    m = [[] for i in range(len(map)*factor)]

    for row in range(len(map)):

        for col in range(len(map[row])):

            # create a grid of factor x factor
            for cr in range(factor):

                for _ in range(factor):
                    m[row*factor+cr].append(map[row][col])

    return m



# full tour
def makeup(map, size, color, upscale):
    map = create_map(map, size, color)
    map = smooth(map, 1)
    #map = smooth_middle(map, 1)
    map = enlarge(map, math.floor(600/len(map)))
    map = smooth_middle(map, 1)
    return map

if __name__ == '__main__':
    #plot = plt.imshow(np.array())
    #plt.show()
    pass
