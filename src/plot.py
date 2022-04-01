
# valtert 2022
# 3d plot extra package

import matplotlib.pyplot as plt
import numpy as np
from random import randint
import os

def render_3d_plot(array, size, color, path):
    # get 1d array + size

    # find max temperature
    max_temp = max(map(int, array))

    # turn map into 2d
    mp = []
    for i in range(size[1]):
        mp.append([])
        for j in range(size[0]):
            mp[-1].append(int(array[i*size[0]+j].get_real_temp()))
    array = mp

    WIDTH = len(array[0])
    HEIGHT = len(array)
    voxels = np.zeros((WIDTH, HEIGHT, max_temp), dtype=bool)
    colors = np.empty(voxels.shape, dtype=tuple)
    for row in range(HEIGHT):
        for col in range(WIDTH):
        
            #voxels[row, col, :array[row][col]] = True

            for height in range(array[row][col]):
                voxels[row, col, height] = True
                colors[row, col, height] = color.get(height, True)


    # and plot everything
    try:
        ax = plt.figure().add_subplot(projection='3d')
        ax.voxels(voxels, facecolors=colors, edgecolor='k', linewidth=0)
        #ax.voxels(voxels, edgecolor='k')
        ax.set_title('Heat distribution')
        plt.savefig(os.path.join(path,'res.png'))
        os.system('open '+ os.path.join(path,'res.png'))
    except IndexError:
        pass


if __name__ == '__main__':
    render_3d_plot([[0,1,0], [1,2,1], [0,1,0]])