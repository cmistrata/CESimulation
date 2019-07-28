from lib.receiver import Receiver


class Muscle(Receiver):
    """Class representing a muscle.

    Attributes:
        name (str): The name of the muscle.
        alreadyActivated (bool): Has the muscle ever been activated.
        just
        Activated (bool): Was the muscle just activated in the last round of neuron fires.
    """

    def __init__(self, name):
        """The constructor for the Muscle class.

        Args:
            name (str): The name of the muscle.
        """
        self.name = name

    def receive_graded_potential(self, graded_potential_strength):
        self.activate()

    def activate(self):
        """Activate the muscle."""
        print(f"Muscle {self.name} fired!")

    def get_name(self):
        return self.name
