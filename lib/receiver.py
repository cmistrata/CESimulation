from abc import ABC, abstractmethod


class Receiver(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def receive_graded_potential(self, graded_potential_strength):
        pass
