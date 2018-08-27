m = 5                       # number of bits to encode one layer, eg. for m = 5 we get layers in (1;31)
layers = 4                  # number of conv layers
N = 100                     # population size
max_iter = 100              # max iterations because of time and cost constraints
max_no_improvement = 50     # number of iterations after which to stop
std_dev = 0.0019255         # std deviation calculated from 100 samples of tf learnings without setting the seed
eps = 4*std_dev             # improvement threshold
crossover_prob = 0.9        # crossover probability
mutation_prob = 0.3         # mutation probability
keep = 30                   # keep best in each population
genetic_read_csv = 'cnn1.csv'
genetic_write_csv = 'cnn1.csv'
seed = 1337