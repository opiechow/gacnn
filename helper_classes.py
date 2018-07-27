import random

class Individual(object):
    def __init__(self, genotype):
        self.genotype = genotype
        self.score = None
        self.loss = None

    @classmethod
    def random(cls, m, layers):
        return cls(tuple([random.randint(1, 2**m-1) for i in range(layers)]))

    def __str__(self):
        return "Layers: {} Score: {} Loss: {}".format(self.genotype, self.score, self.loss)


class Job(object):
    def __init__(self, individual, epochs = 1, seed = 1337):
        self.individual = individual
        self.epochs = epochs
        self.seed = seed

    def __str__(self):
        return "Individual: {} Epochs: {} Seed: {}".format(self.individual.genotype, self.epochs, self.seed)