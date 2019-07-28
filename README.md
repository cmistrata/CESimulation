# C. Elegans Simulation

A scipt simulating the nervous system of the [C. Elegans worm](https://en.wikipedia.org/wiki/Caenorhabditis_elegans), which has an extremely simple and [completely mapped out](https://en.wikipedia.org/wiki/Connectome) nervous sytem, using [neuronal wiring data from worm atlas](https://wormatlas.org/neuronalwiring.html). Stimulate a C. Elegans neuron and watch the signal propagate across the nervous system. *Not very scientifically accurate :/*

## Usage
To call the CESimulation.py function run
```
python celegans_simulation.py [-h] -n NEURON [-s SIGNAL_STRENGTH]
```
where ```NEURON``` is the name of the neuron to stimulate  (see the 'Neuron 1' and 'Neuron 2' columns of [the neural connectivity csv](resources/NeuronConnect.csv) for neuron names) and ```SIGNAL_STRENGTH``` is the strength of the signal to stimulate the neuron with, by default 1.
