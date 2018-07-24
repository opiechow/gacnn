class Individual(object):
    def __init__(self, id, genotype):
        self.id = id
        self.genotype = genotype
        self.score = None
        self.loss = None

    def __str__(self):
        return "Id: {} Layers: {} Score: {} Loss: {}".format(self.id, self.genotype, self.score, self.loss)


class Job(object):
    def __init__(self, individual, epochs = 1, seed = 1337):
        self.individual = individual
        self.epochs = epochs
        self.seed = seed

    def __str__(self):
        return "Individual: {} Epochs: {} Seed: {}".format(self.individual.genotype, self.epochs, self.seed)