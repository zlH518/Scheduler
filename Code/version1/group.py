from typing import Iterable
from node import BaseNode



class Package:
    def __init__(self, cards_per_package: int, node_index: int):
        self.cards = cards_per_package
        self.nodeId = node_index
        self.task = []

    def __len__(self):
        return self.cards


class Group:
    def __init__(self, cards_per_package: int, theta: float):
        self.cards_per_package = cards_per_package
        self.package = []
        self.theta = theta
        self.completed_task = []

    def getEmptyPackage(self):
        if next((p for p in self.package if len(p.task) == 0), None) is not None:
            index = next((index for index, p in enumerate(self.package) if len(p.task)), None)
            return index
        else:
            return None





