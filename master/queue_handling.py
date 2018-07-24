import time
import abc
import random
import socket
import pickle
from helper_classes import Individual, Job

hosts_pool = ["167.99.251.94",
"167.99.251.92",
"167.99.251.135",
"167.99.251.110",
"167.99.251.31",
"167.99.251.90",
"167.99.251.102",
"167.99.251.95",
"167.99.251.136",
"167.99.251.89"]

class Worker(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def is_available(self):
        return

    @abc.abstractmethod
    def assign_job(self, job):
        return

    @abc.abstractmethod
    def has_result(self):
        return

    @abc.abstractmethod
    def get_result(self):
        return

    @abc.abstractmethod
    def free_worker(self):
        return


class DigitalOceanWorker(Worker):
    def __init__(self, ip):
        self.available = True
        self.result = None

        self._ip = ip
        self._job_port = 4123
        self._result_port = 4124

    def is_available(self):
        return self.available

    def assign_job(self, job):
        self.available = False
        self._remote_dispatch(job)

    def has_result(self):
        result = self._fetch_remote_result()
        if result:
            self.result = result
            return True
        return False

    def get_result(self):
        return self.result

    def free_worker(self):
        self.available = True
        self.result = None

    def _remote_dispatch(self, job):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self._ip, self._job_port))
        s.sendall(pickle.dumps(job))
        s.close()

    def _fetch_remote_result(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self._ip, self._result_port))
        s.sendall(b"RDY?")
        response = s.recv(1024)
        if "BSY" in str(response):
            return None
        else:
            result = pickle.loads(response)
            assert(result.score is not None)
            return result


class DummyWorker(object):
    def __init__(self):
        self.available = True
        self.result = None

    def is_available(self):
        return self.available

    def assign_job(self, job):
        self.available = False
        self.result = sum(job)

    def has_result(self):
        if self.result:
            return True
        else:
            return False

    def get_result(self):
        return self.result

    def free_worker(self):
        self.available = True
        self.result = None


class WorkManager(object):
    def __init__(self):
        self.workers = []
        self.jobs = []
        self.results = []
        self.__initialize_workers()

    def __initialize_workers(self):
        for host in hosts_pool:
            self.workers.append(DigitalOceanWorker(host))

    def evaluate(self, jobs):
        '''

        :param jobs: list of jobs with scores to be computed
        :return: list of Individuals with scores computed
        '''
        expected_results = len(jobs)
        while len(self.results) < expected_results:
            for worker in self.workers:
                if worker.is_available() and jobs:
                    job = jobs.pop()
                    print("Worker available. Assigning job ({}/{}): {}".format(expected_results - len(jobs), expected_results, job))
                    worker.assign_job(job)
            for worker in self.workers:
                if worker.has_result():
                    result = worker.get_result()
                    self.results.append(result)
                    worker.free_worker()
            time.sleep(1)
        return self.results


def map_results_to_dict(results):
    '''

    :param results: list of Individuals
    :return: list of dicts contatining rows for csv writing
    '''
    dicts = []
    for result in results:
        assert(isinstance(result,Individual))
        dicts.append({"id" : result.id, "genotype" : result.genotype, "score" : result.score, "loss" : result.loss})
    return dicts


def save_csv(results):
    dicts = map_results_to_dict(results)

    import csv

    with open('data.csv', 'w') as csvfile:
        fieldnames = ['iter', 'genotype', 'score', 'loss']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for entry in dicts:
            writer.writerow(entry)

random.seed(1337)

jobs = []
for i in range(100):
    jobs.append(Job(Individual(i, tuple([random.randint(1,31) for i in range(4)])),1,1337))
wm = WorkManager()
results = wm.evaluate(jobs)
save_csv(results)


