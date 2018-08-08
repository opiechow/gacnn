import sys
import time
import abc
import socket
import pickle
from math import sin, pi

sys.path.append("..")

job_port = 4123
result_port = 4124


def host_available(host):
    try:
        for port in job_port, result_port:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((host, port))
            sock.send(b"UP?")
            response = sock.recv(1024)
            sock.close()
            if not b"UP" in response:
                return False
    except Exception as e:
        # print('Worker %s not available.' % host)
        return False
    return True


class TimeoutException(Exception):
    pass


class Worker(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def is_available(self):
        return

    @abc.abstractmethod
    def assign_job(self, job):
        """
        Returns True if job succesfuly assigned, False otherwise
        :rtype: bool
        """
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

    @abc.abstractmethod
    def get_current_job(self):
        return


class RemoteWorker(Worker):
    def __init__(self, ip):
        self.available = True
        self.result = None
        self.job = None

        self.ip = ip
        self._job_port = job_port
        self._result_port = result_port
        self._start = None
        self.timeout = 10000  # after 60 minutes something is wrong

    def __eq__(self, other):
        return self.ip == other.ip

    def __str__(self):
        return "Available: {} | Result : {} | Job: {} : IP: {}".format(self.available, self.result, self.job, self.ip)

    def is_available(self):
        return self.available

    def assign_job(self, job):
        self.available = False
        self.job = job
        self._start = time.time()
        try:
            self._remote_dispatch(job)
        except Exception as e:
            print(e)
            print("Job dispatch failed.")
            return False
        return True

    def has_result(self):
        if time.time() - self._start > self.timeout:
            raise TimeoutException
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

    def get_current_job(self):
        assert self.job is not None
        return self.job

    def _remote_dispatch(self, job):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self._job_port))
        s.sendall(pickle.dumps(job))
        s.close()

    def _fetch_remote_result(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self._result_port))
        s.sendall(b"RDY?")
        response = s.recv(1024)
        if "BSY" in str(response):
            return None
        else:
            result = pickle.loads(response)
            assert(result.score is not None)
            return result


class LevyWorker(object):
    def __init__(self):
        self.available = True
        self.result = None

    def is_available(self):
        return self.available

    def assign_job(self, job):
        self.available = False
        xm = job.individual.genotype
        x = (xm[0] - 3, xm[1] - 7, xm[2] - 13, xm[3] - 20)
        w = []
        for i in range(len(x)):
            w.append(1 + (x[i] - 1) / 4)
        middle_term = 0
        for i in range(len(x) - 1):
            middle_term += (w[i]-1)**2*(1 + 10 * sin(pi*w[i] + 1) * sin(pi*w[i] + 1))
        result = sin(pi*w[0])*sin(pi*w[0]) + middle_term + (w[-1] - 1)**2 * (1 + sin(2*pi*w[-1])*sin(2*pi*w[-1]))
        job.individual.loss = result
        job.individual.score = 1000 - result
        self.result = job.individual
        return True

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
        self.results = []

    def __add_workers(self):
        hosts_pool = []
        with open("workers","r") as f:
            for line in f:
                hosts_pool.append(line.strip())
        for host in hosts_pool:
            if not RemoteWorker(host) in self.workers:
                if host_available(host):
                    print("Adding new worker: %s" % host)
                    self.workers.append(RemoteWorker(host))

    def evaluate(self, jobs):
        '''

        :param jobs: list of jobs with scores to be computed
        :return: list of Individuals with scores computed
        '''
        self.results = []
        expected_results = len(jobs)
        while len(self.results) < expected_results:
            self.__add_workers()  # makes adding new workers while the script is running possible
            for worker in self.workers[:]:
                if worker.is_available() and jobs:
                    job = jobs.pop()
                    print("Worker available. Assigning job ({}/{}): {}".format(expected_results - len(jobs), expected_results, job))
                    success = worker.assign_job(job)
                    if not success:
                        print("Worker %s broken in assigning job, removing from pool and reasigning job" % worker.ip)
                        jobs.append(worker.get_current_job())
                        self.workers.remove(worker)
            for worker in self.workers[:]:
                try:
                    if not worker.is_available():
                        if worker.has_result():
                            result = worker.get_result()
                            self.results.append(result)
                            worker.free_worker()
                except Exception as e:
                    print(e)
                    print("Worker %s broken in result collection, removing from pool and reasigning job" % worker.ip)
                    jobs.append(worker.get_current_job())
                    self.workers.remove(worker)
            time.sleep(1)
        return self.results
