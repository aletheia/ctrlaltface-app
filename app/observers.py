
import logging


class Observable:
    def __init__(self):
        self.observers = []

    def register(self, observer):
        logging.info("Registering observer {}".format(
            observer.__class__.__name__))
        self.observers.append(observer)

    def unregister(self, observer):
        self.observers.remove(observer)

    def notify(self, data):
        for observer in self.observers:
            observer.update(data)


class Observer:
    def update(self, frame):
        pass
