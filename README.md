## BRIEF DESCRIPTION

This description is abbreviated, see the project report (minus the conclusions section) for more information.
The attached script and files are the final project for a class I took on bioinformatics. It mimics the nervous system of the C Elegans worm, an animal with an extremely
small and simple nervous system that has been completely mapped out. The C Elegans nervous system works by having neurons send signals to each other which decay rapidly over time
and space. When these signals reach a muscle with enough strength, they cause it to fire. Additionally, two different types of synapses (connections between neurons)
exist: a two way electrical synapse, or a one way chemical synapse. Properties of neurons which were not specified in the attached csv's are left to the user as
command line parameters. The program allows you to simulate firing different nerves of the animal, and will print out info about what neurons fired, how often, what
muscles fired, etc (see the USAGE section below).

## USAGE
To call the CESimulation.py function run
    python CESimulation.py <Firing Neuron Name> <Explore Connectivity> <Firing Threshold> <Chemical Signal Decay Rate> <Electrical Signal Decay Rate> <Firing Strength>
where all the arguments are optional and will be replaced by default values if not specified.

Firing neuron name: The name of the neuron you want to fire, with names from NeuroConnect.csv. Set to ALL to fire all neurons sequentially and print some interesting statistics.

Explore Connectivity: If "True", each neuron will fire only once, but signals will not decay (remaining parameters meaningless). Combine "True" with "ALL" as the firing neuron name to see which neurons are reachable from other neurons.

Firing threshold: The signal strength that a neuron must receive to fire.

Chemical Signal Decay Rate: How much a signal decays when sent through a chemical synapse. (Strength of signal received = strength of sent signal * chemical decay rate)

Electrical Signal Decay Rate: How much a signal decays when sent through an electrical synapse (Strength of signal received = strength of sent signal * electrical decay rate)

Firing Strength: The signal strength with which the the neuron of the name <Firing Neuron Name> will fire. This signal is sent to all its outgoing connections.
