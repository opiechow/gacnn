import random


class Individual(object):
    def __init__(self, phenotype):
        self.phenotype = phenotype
        self.score = None
        self.loss = None
        self.training_history = None

    @classmethod
    def random(cls, m, layers):
        return cls(tuple([random.randint(1, 2**m-1) for i in range(layers)]))

    def __str__(self):
        return "Layers: {} Score: {} Loss: {}".format(self.phenotype, self.score, self.loss)


class Job(object):
    def __init__(self, individual, epochs=1, seed=1337):
        self.individual = individual
        self.epochs = epochs
        self.seed = seed

    def __str__(self):
        return "Individual: {} Epochs: {} Seed: {}".format(self.individual.phenotype, self.epochs, self.seed)

    def get_key(self):
        '''
        Function used for duplicate job filtering
        :return: returns a distinct key for each job
        '''
        return self.individual.phenotype, self.epochs, self.seed