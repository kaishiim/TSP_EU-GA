"""
Genetic Algorithms are a family of evolutionary algorithms which can be implemented in any language (including python)
they solve problems which have no clear solution by generating random solutions and picking the best results 
then applying a crossover and a mutation to the best solutions before starting the process again. 
"""

import csv
import numpy as np
from matplotlib import pyplot as plt
from math import sqrt
from random import randint, shuffle


num_pop = 50000
num_gen = 150


def getfloat(x):
    return float(x.replace(",", '.'))


def createtour(numcities):
    tour = [i for i in range(1, numcities)]
    shuffle(tour)
    tour = [0] + tour
    return tour
    

def tourlen(tour, dist):
    numcities = len(tour)
    sum = 0
    for i in range(numcities):
        fra, til = tour[i], tour[(i+1)%numcities]
        sum += dist[fra] [til]
    return(sum)


def creategenome(dist):
    numcities = len(dist)
    tour = createtour(numcities)
    tlength = tourlen(tour, dist) # Afstand/Fitness score
    return (tour, tlength)


def overcross(tour1, tour2):
    r = randint(1, numcities-1) # random integer [0:36]
    #print("kryds =", tour1[0:r], tour2[r:]+tour2[0:r]) 
    tour3 = tour1[0:r]  #splejs tour
    for i in range(numcities):
        x = tour2[(r + i) % numcities] # element med index r + i og modulo
        if x not in tour3:  # Betingelse som sikrer at en by ikke forekommer 2 gange 
            tour3.append(x)  
    return tour3


##### Main code


"""
# Data structures

coordinates: list of tuple(lattitude, longtitude)

dist: array of array of distance from city to city

tour: list of citynumber(0...37)

pop: list of tuple(tour, length)

"""

with open('capitals.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    header = next(reader)
    rows2 = []
    for row in reader:
        name, lat, lng, pop = row[0], getfloat(row[1]), getfloat(row[2]), int(row[3])
        rows2.append([name, lat, lng, pop])
#print(rows2)


# adjacency-distance matrix
citynames = []
coordinates = [] 
for row in rows2:
    name, lat, lng, pop = row
    #print(name, lat, lng, pop) 
    citynames += [name] # assign citynamems elements
    coordinates.append((lat, lng)) # assign coordinates in same order as citynames elements
#print("Citynames =", citynames)
#print("City coordinates =", coordinates)


#plot capitals routine
if True:
    xx = [x[1] for x in coordinates]
    yy = [y[0] for y in coordinates]
    plt.title('Europe capitals')
    plt.xlabel('Longtitude')
    plt.ylabel('Lattitude')
    plt.scatter(xx, yy)    
    plt.show()
    #plt.draw()
    #plt.pause(5)
    #plt.close()


# Initialize list of city names and matrix of adjacent distances 
numcities = len(rows2)
dist = np.zeros((numcities, numcities))  # Matrix creation
for i in range(numcities):  # For all origin cities do
    c_ix, c_iy = coordinates[i][0], coordinates[i][1] # assign x,y coordinates for origin city 
    for j in range(numcities):  # For alle destionation cities do
        c_jx, c_jy = coordinates[j][0], coordinates[j][1]  # assign x,y coordinates for destination city
        dist[i][j] = sqrt((c_ix - c_jx)*(c_ix - c_jx) + (c_iy - c_jy)*(c_iy - c_jy))  # calculate distance between origin and destination city
#print("dist =",dist)


## create population
pop = [(creategenome(dist)) for i in range(num_pop)] # pop: list of tuples of tour and length
pop.sort(key = lambda x:x[1])  # sorting to find minimum distance
best_tour = pop[0]
best_length_list = [best_tour[1]]


# Plotting of iterative generations
fig, (ax1, ax2) = plt.subplots(1, 2, width_ratios=(4, 3), figsize=(12, 5))
plt.title('Europe TSP')
plt.xlabel('Longtitude')
plt.ylabel('Lattitude')
plt.title("Tour length over generations")
plt.xlabel("Generation")
plt.ylabel("Tour length")
for generation in range(1, num_gen+1):
    new_pop = []
    for k in range(num_pop):
        i, j = randint(1, num_pop-1), randint(1, num_pop-1)
        tour = overcross(pop[i][0], pop[j][0])
        tlength = tourlen(tour, dist)
        new_pop.append((tour, tlength))
    pop += new_pop  # Doubling of population (variation)
    pop.sort(key = lambda x:x[1])  # sorting to find minimum distance (selection)
    pop = pop[0:num_pop]
    best_tour = pop[0]
    best_length_list.append(best_tour[1])
    print("gen, best_tour =", generation, best_tour)
    colours = ["r", "g", "b"]
    xx = [coordinates[city][1] for city in best_tour[0]]
    yy = [coordinates[city][0] for city in best_tour[0]] 
    plt.axes(ax1)
    plt.gca().clear()
    plt.title('Europe TSP %d: %f' % (generation, best_tour[1]))
    for i in range(numcities+1):
        i0 = i%numcities
        i1 = (i+1)%numcities
        plt.plot([xx[i0], xx[i1]], [yy[i0], yy[i1]], marker="o", c=colours[i%len(colours)])
    plt.plot(xx[0], yy[0], marker="o", c="black")    
    plt.draw()
    plt.axes(ax2)
    plt.plot(best_length_list)
    plt.pause(0.01)
plt.show()

