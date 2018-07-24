import random

#Misc genetic algorithm functions
def calculatePopulationAverage(robots):
    '''
    Calculates the average distance of all robots
    :param robots: Current list of robots
    :return:
    '''
    count = 0
    sum = 0
    for robot in robots:
        sum += robot.distance
        count += 1
    return float(sum)/count

def sortPopulation(population):
    '''
    Sorts the robot population by rating.
    :param population: unsorted cnn population.
    :return: sorted cnn list.
    '''
    population = sorted(population, key=lambda individual: individual.score)   # sort by rating
    return population

def crossChromosomes(c1, c2, cxP):
    '''
    Crosses two given chromosomes.
    :param c1: First parent chromosome.
    :param c2: Second parent chromosome.
    :param cxP: List of crossing points.
    :return: Two crossed chromosomes.
    '''
    #first pad the chromosomes to full lenght
    cLong1 = c1 + [NO_MOVE] * (maxMoves - len(c1))
    cLong2 = c2 + [NO_MOVE] * (maxMoves - len(c2))
    slices1 = []
    slices2 = []
    slices1.append(cLong1[:cxP[0]])
    slices2.append(cLong2[:cxP[0]])
    for i in range(len(cxP) - 1):
        slices1.append(cLong1[cxP[i]:cxP[i + 1]])
        slices2.append(cLong2[cxP[i]:cxP[i + 1]])
    slices1.append(cLong1[cxP[len(cxP) - 1]:])
    slices2.append(cLong2[cxP[len(cxP) - 1]:])
    dRoute1 = []
    dRoute2 = []
    for i in range(len(slices1)):
        if i % 2 == 1:
            dRoute1.extend(slices1[i])
            dRoute2.extend(slices2[i])
        else:
            dRoute1.extend(slices2[i])
            dRoute2.extend(slices1[i])
    return dRoute1, dRoute2

#Algorithm parameters:
generatedDescendants = 50
crossingPoints = (100, 300)
numIterations = 100
mutation_probability = 0.2
population = 1000
replaceEachGeneration = 30
keep = 20

if __name__ == '__main__':
    #INITIALIZE FIRST GENERATION
    robots = []
    for i in range(population):
        moves = []
        current_position = start
        for x in range(maxMoves):
            if current_position == finish:
                moves.append(NO_MOVE)
            else:
                direction = random.choice([EAST,WEST,NORTH,SOUTH])
                current_position = robotMove(current_position, direction, worldMap)
                moves.append(direction)
        robots.append(Robot(moves,worldMap))

    robots = sortPopulation(robots)
    currentGeneration = robots

    step = 0
    bestDistance = []
    avgDistance = []
    once = False

    bestDistance.append(robots[0].distance)
    avgDistance.append(calculatePopulationAverage(currentGeneration))
    #main loop begins here
    while True:
        descendants = []
        #crossing - create descendants from parents by crossing chromosomes
        while len(descendants) < generatedDescendants:
            p1 = random.choice(currentGeneration)     #take random parents from current generation
            p2 = random.choice(currentGeneration)
            dRoute1, dRoute2 = crossChromosomes(p1.route, p2.route, crossingPoints)
            descendants.extend([Robot(dRoute1,worldMap),Robot(dRoute2,worldMap)])
        #mutation - only for new descendants
        for descendant in descendants:
            if random.random() > (1 - mutation_probability):
                insertIndex = random.randint(0, (len(descendant.route)-1))
                possibleDirs = [EAST,WEST,NORTH,SOUTH]
                possibleDirs.remove(descendant.route[insertIndex])
                insertThis = random.choice(possibleDirs)
                descendant.route[insertIndex] = insertThis
                descendant.recalculateParams()
        #keep best from previous generation
        descendants.extend(currentGeneration[:keep])
        #replace the old worst with the best new
        descendants = sortPopulation(descendants)
        currentGeneration[-replaceEachGeneration:] = descendants[:replaceEachGeneration]
        currentGeneration = sortPopulation(currentGeneration)
        #plot the best route
        if step % showEach == 0 or (currentGeneration[0].distance == 0 and not once):
            if currentGeneration[0].distance == 0:
			    if not once:
			        print "Found route, iteration: " + str(step)
			        once = True
            mapWithRoute = markRouteOnMap(worldMap,currentGeneration[0].route)
            plotWorldMap(mapWithRoute)
        #add data for this step
        bestDistance.append(currentGeneration[0].distance)
        avgDistance.append(calculatePopulationAverage(currentGeneration))
        step += 1
        #break loop if requirements are met
        if step == numIterations:
            break
#        if currentGeneration[0].distance == 0:
#            break

    print "Final iteration: " + str(step)
    generations = []
    gen_count = 0
    for rating in bestDistance:
        generations.append(gen_count)
        gen_count += 1

    #plot gathered data
    fig = plt.figure()

    ax1 = fig.add_subplot(211)
    ax1.plot(generations, bestDistance)
    ax1.axis([0, max(generations), -1, max(bestDistance)+1])
    ax1.set_ylabel('Best distance')

    ax2 = fig.add_subplot(212)
    ax2.plot(generations, avgDistance)
    ax2.axis([0, max(generations), -1, max(avgDistance)+1])
    ax2.set_xlabel('Generations')
    ax2.set_ylabel('Average distance')
    currentGeneration[0].tellMeYourRoute

    plt.show()