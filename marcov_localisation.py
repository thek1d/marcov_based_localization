import numpy as np
import random
from matplotlib import pyplot as plt

def calc_prior_believe(size, prior_believe, gridmap, motion_model):
    for cell in range(size):
            prior_believe[cell] = gridmap[cell-3] * motion_model[0] + \
                                  gridmap[cell-4] * motion_model[1] + \
                                  gridmap[cell-5] * motion_model[2] + \
                                  gridmap[cell-6] * motion_model[3] + \
                                  gridmap[cell-7] * motion_model[4]

def calc_posterior_believe(size, sensor_distance, prior_believe, probability_map, pillars):
    posterior_not_normalized = [0.0] * size
    
    for cell in range(size):
        
        if not measurement_possible(cell, pillars, sensor_distance):
            continue

        if cell + sensor_distance > size - 1:
            posterior_not_normalized[cell] = probability_map[(cell  + sensor_distance) - size] * \
                                             prior_believe[cell]
        else:
         posterior_not_normalized[cell] = probability_map[cell + sensor_distance] * \
                                          prior_believe[cell]
        
    eta = 1 / np.sum(posterior_not_normalized)
    return list(map(lambda x: x * eta, posterior_not_normalized))

def measurement_possible(cell, pillars, sensor_distance):
    area = 0
    acutal_pos = 0
    next_pillar = 0
    pillar_after_next_region = 0

    if cell >= 0 and cell < pillars[0] or cell == pillars[4] and cell <=49:
        area = 0
    elif cell >= pillars[0] and cell < pillars[1]:
        area = 1 
    elif cell >= pillars[1] and cell < pillars[2]:
        area = 2 
    elif cell >= pillars[2] and cell < pillars[3]:
        area = 3 
    elif cell >= pillars[3] and cell < pillars[4]:
        area = 4
    
    acutal_pos = cell
    next_pillar = pillars[area]
    pillar_after_next_region = [pillars[(area + 1) % len(pillars)]-1] + [pillars[(area + 1) % len(pillars)]] + [pillars[(area + 1) % len(pillars)]+1]

    
    if acutal_pos + sensor_distance > next_pillar and acutal_pos + sensor_distance in pillar_after_next_region:
        return False
    else:
        return True

''' Creating a map with the probabilities 
    probabilites of the pillar position is 0.5
    position previous and afterwards are 0.25
    this is needed for the posterior'''
def create_probability_map(size):
    probability_map = [pow(10,-5)] * size
    pillar_index = 0
        
    for cell in range(size):
        while pillar_index < len(pillars):
            if cell == pillars[pillar_index]-1:
                probability_map[cell] = .25
            elif cell == pillars[pillar_index]:
                probability_map[cell] = .5
            elif cell == pillars[pillar_index] + 1:
                probability_map[cell] = .25
            break

        if pillar_index < len(pillars) and cell == pillars[pillar_index] + 1:
            pillar_index +=1
    
    return probability_map
        
def plot_bar(prob_list, title):
    plt.title(title)
    plt.xlabel('Cells')
    plt.ylabel('Probability')
    bars   = [x for x in range(50)]
    y_pos  = np.arange(len(bars))
    plt.bar(y_pos, prob_list)
    plt.xticks(y_pos, bars)
        
if __name__ == '__main__':
    ''' initialization '''
    MAP_SIZE          = 50
    gridmap           = [1/MAP_SIZE] * MAP_SIZE #posterior
    prior_believe     = [.0] * 50
    motion_model      = [.1, .2, .4, .2, .1]
    sensor_model      = [.25, .5, .25]
    sensor_distances  = [5, 10, 7, 2, 10]
    pillars           = [4, 13, 20, 31, 45]
    probability_map   = []

    plt.figure(1)
    plot_bar(prob_list=gridmap, title='Initial Belive')

    for distance in range(len(sensor_distances)):
        calc_prior_believe(MAP_SIZE, prior_believe, \
                        gridmap, motion_model)

        plt.figure(2+distance)
        plot_bar(prob_list=prior_believe, title='Prior_Step%s' %distance)

        probability_map = create_probability_map(MAP_SIZE)
        
        gridmap = calc_posterior_believe(MAP_SIZE, \
                                    sensor_distances[distance], \
                                    prior_believe,
                                    probability_map,
                                    pillars)
        plt.figure(8+distance)
        plot_bar(prob_list=gridmap, title= 'Posterior_Step%s' %distance)

    plt.show()

