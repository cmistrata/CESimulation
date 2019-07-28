from enum import Enum, auto


class NeuralJunction(Enum):
    CHEMICAL = auto()
    ELECTRICAL = auto()
    NEUROMUSCULAR = auto()

    @staticmethod
    def from_str(label):
        if label in ('S', 'Sp', 'R', 'Rp'):
            return NeuralJunction.CHEMICAL
        elif label == 'EJ':
            return NeuralJunction.ELECTRICAL
        elif label == 'NMJ':
            return NeuralJunction.NEUROMUSCULAR
        else:
            raise NotImplementedError(f"Neural junction type {label} not recognized.")
