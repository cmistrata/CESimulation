from lib.enums.neural_junction import NeuralJunction
from lib.outgoing_connection import OutgoingConnection
from lib.receiver import Receiver
import lib.constants as constants


class Neuron(Receiver):
    """Class representing a neuron."""

    def __init__(self, name):
        """The constructor for the Neuron class.

        Args:
            name (str): The name of the neuron.
        """
        self.name = name
        self.outgoing_connections = []
        self.in_refractory_period = False
        self.graded_potential_strength = 0
        self.totalNumberOfFires = 0

    def add_outgoing_connection(self, receiver, junction_type, number_of_synapses, weight=1):
        """Add a Connection to this neurons outgoingConnections list."""
        self.outgoing_connections.append(OutgoingConnection(
            receiver, junction_type, number_of_synapses, weight))

    def try_to_fire(self):
        if self.graded_potential_strength > 0 and not self.in_refractory_period:
            print(f"{self.name}: Fire!")
            for outgoing_connection in self.outgoing_connections:
                receiver = outgoing_connection.receiver
                junction_type = outgoing_connection.junction_type
                signal_strength = self.graded_potential_strength
                if junction_type == NeuralJunction.ELECTRICAL:
                    signal_strength *= constants.ELECTRICAL_SIGNAL_DECAY_RATE
                else:
                    signal_strength *= constants.CHEMICAL_SIGNAL_DECAY_RATE
                receiver.receive_graded_potential(signal_strength)

            self.enter_refractory_period()
            return True
        return False

    def enter_refractory_period(self):
        self.graded_potential_strength = 0
        self.in_refractory_period = True

    def exit_refractory_period(self):
        self.in_refractory_period = False

    def receive_graded_potential(self, graded_potential_strength):
        if (not self.in_refractory_period
            and graded_potential_strength > constants.FIRING_THRESHOLD
                and graded_potential_strength > self.graded_potential_strength):
            self.graded_potential_strength = graded_potential_strength

    def get_name(self):
        return self.name
