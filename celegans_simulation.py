"""Simulation of the C. Elegans nervous system."""

import argparse
import pandas as pd
import os
from lib.neuron import Neuron
from lib.muscle import Muscle
from lib.enums.neural_junction import NeuralJunction


def get_neurons_by_name(neuron_connect_csv, neuron_fixed_points_csv):
    connections = pd.read_csv(neuron_connect_csv)
    sender_name_col = 0
    receiver_name_col = 1
    junction_type_col = 2
    number_of_synapses_col = 3

    fixed_points = pd.read_csv(neuron_fixed_points_csv)
    weight_col = 3

    muscles_by_name = {}
    fixed_points_muscle_rows = [
        row for row in fixed_points.values if row[receiver_name_col].startswith('M')]
    for muscle_name in set([row[1] for row in fixed_points.values]):
        muscles_by_name[muscle_name] = Muscle(muscle_name)

    neurons_by_name = {}
    outgoing_connections_rows = [
        row for row in connections.values if row[junction_type_col] not in ["R", "Rp"]]
    for outgoing_connection_row in outgoing_connections_rows:
        neuron_name = outgoing_connection_row[sender_name_col]
        if neuron_name in neurons_by_name:
            neuron = neurons_by_name[neuron_name]
        else:
            neuron = Neuron(neuron_name)
            neurons_by_name[neuron_name] = neuron

        junction_type = NeuralJunction.from_str(
            outgoing_connection_row[junction_type_col])
        receiver_name = outgoing_connection_row[receiver_name_col]
        number_of_synapses = outgoing_connection_row[number_of_synapses_col]

        receiver_is_muscle = junction_type == NeuralJunction.NEUROMUSCULAR
        if receiver_is_muscle:
            fixed_points_muscle_row = (
                row for row in fixed_points_muscle_rows if row[sender_name_col] == neuron_name)
            for receiving_muscle_fixed_points_row in fixed_points_muscle_row:
                receiving_muscle_name = receiving_muscle_fixed_points_row[receiver_name_col]
                weight = receiving_muscle_fixed_points_row[weight_col]
                receiver = muscles_by_name[receiving_muscle_name]
        else:
            if receiver_name in neurons_by_name:
                receiving_neuron = neurons_by_name[receiver_name]
            else:
                receiving_neuron = Neuron(receiver_name)
                neurons_by_name[receiver_name] = receiving_neuron
            receiver = receiving_neuron
            weight = 1

        neuron.add_outgoing_connection(
            receiver, junction_type, number_of_synapses, weight)

    return neurons_by_name


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='A script simulating the nervous system of C. Elegans. Stimulate a neuron and '
                    'watch the signal propagate across the nervous system.')
    parser.add_argument('-n', '--neuron', type=str,
                        required=True,
                        help='the neuron to stimulate')
    parser.add_argument('-s', '--signal-strength', type=float,
                        default=1,
                        help='the strength of the signal to send to the neuron')

    args = parser.parse_args()
    neuron_connect_csv = os.path.join("resources", "NeuronConnect.csv")
    neuron_fixed_points_csv = os.path.join("resources", "NeuronFixedPoints.csv")
    neurons_by_name = get_neurons_by_name(
        neuron_connect_csv, neuron_fixed_points_csv)
    if args.neuron not in neurons_by_name:
        print(f"Error: neuron {args.neuron} wasn't found! Exiting.")
        exit(1)
        
    first_neuron = neurons_by_name[args.neuron]
    first_neuron.receive_graded_potential(args.signal_strength)

    neurons = neurons_by_name.values()
    firing_round = 1
    print(f"Round {firing_round}")
    while any([neuron.try_to_fire() for neuron in neurons]):
        [neuron.exit_refractory_period() for neuron in neurons]
        firing_round += 1
        print(f"\nRound {firing_round}")
