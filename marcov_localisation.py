import numpy as np
import random
from matplotlib import pyplot as plt

def init_gridpmap(size=50):
    return [1/size] * size

def plot_bar(prob_list, title):
    plt.title(title)
    plt.xlabel('Cells')
    plt.ylabel('Probability')
    bars   = [x for x in range(50)]
    y_pos  = np.arange(len(bars))
    plt.bar(y_pos, prob_list)
    plt.xticks(y_pos, bars)
    plt.show()

if __name__ == '__main__':
    grid_map = init_gridpmap()
    plot_bar(grid_map, 'Inital Pose')

