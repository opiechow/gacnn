class Individual(object):
    def __init__(self, genotype):
        self.genotype = genotype
        self.score = None
        self.loss = None

class Job(object):
    def __init__(self, individual, epochs = 1, seed = 1337):
        self.individual = individual
        self.epochs = epochs
        self.seed = seed
