from utils import get_logger
from crawler.frontier import Frontier
from crawler.worker import Worker
from crawler.report import Report

class Crawler(object):
    def __init__(self, config, restart, frontier_factory=Frontier, worker_factory=Worker):
        # Standard init, but I don't currently know what get_logger does. I think most likely to log info that we can view but not sure
        self.config = config
        self.logger = get_logger("CRAWLER")
        self.frontier = frontier_factory(config, restart)
        self.report = Report()
        self.workers = list()
        self.worker_factory = worker_factory

    def start_async(self):
        # Workers are initialized with everything the same except for ids, which depends on the number of threads in config.ini
        self.workers = [
            self.worker_factory(worker_id, self.config, self.frontier, self.report)
            for worker_id in range(self.config.threads_count)]
        # Each worker runs .start(), which is presumably a mathod in the Thread class which worker inherits from
        # .start(): "It arranges for the object’s run() method to be invoked in a separate thread of control."
        for worker in self.workers:
            worker.start()

    def start(self):
        # launch.py runs this
        self.start_async()
        self.join()

    def join(self):
        # Each worker runs .join(), which is presumably a method in the Thread class which Worker inherits from 
        # .join(): "Wait until the thread terminates. This blocks the calling thread until the thread whose join() method is called terminates"
        for worker in self.workers:
            worker.join()
