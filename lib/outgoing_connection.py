class OutgoingConnection:
    """Class representing an outgoing connection to another neuron from a neuron."""

    def __init__(self, receiver, junction_type, number_of_synapses, weight=1):
        self.receiver = receiver
        self.junction_type = junction_type
        self.number_of_synapses = number_of_synapses
        self.weight = weight
