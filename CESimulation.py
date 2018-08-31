"""Simulation of the C. Elegans nervous system."""

import csv
import sys


class Connection:
    """Class representing an outgoing connection to another neuron from a neuron.

    Attributes:
        receivingNeuronName (str): The name of the neuron at the receiving end of this connection.
        Type (str): The type of this connection, with options "NMJ" (neuromuscular junction), "EJ" (electrical junction),
            or "R" (receiving, representing a chemical junction).
        nbr (int): The number of synapses between the sending and receiving neuron.
        weight (float): The strength of the connection.
    """

    def __init__(self, receivingNeuronName, Type, nbr, weight=1):
        """The constructor for the Connection class.

        Args:
            receivingNeuronName (str): The name of the neuron at the receiving end of this connection.
            Type (str): The type of this connection, with options "NMJ" (neuromuscular junction), "EJ" (electrical junction),
                or "R" (receiving, representing a chemical junction).
            nbr (int): The number of synapses between the sending and receiving neuron.
            weight (int): The strength of the connection.
        """
        self.receivingNeuronName = receivingNeuronName
        self.Type = Type
        self.number = nbr
        self.weight = weight


class Muscle:
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
        self.alreadyActivated = False
        self.justActivated = False

    def activate(self):
        """Activate the muscle, increasing the global count of the number of muscle activations and making note that the muscle was just activated."""
        self.alreadyActivated = True
        self.justActivated = True
        global numberOfMuscleActivations
        numberOfMuscleActivations += 1


class Neuron:
    """Class representing a muscle.

    Attributes:
        name (str): The name of the neuron.
        outgoingConnections (list of Connection): List of Connection objects to neurons and muscles this neuron has outgoing connections to.
        neuronsNotConnectedTo (list of Neuron): List of Neuron objects this Neuron is not connected to.
        alreadyFired (bool): Has the neuron ever fired.
        justFired (bool): Did the neuron just fire in the last round of neuron fires.
        signalReceivedStrength (float): The strength of the signal this neuron received in the last round of neuron fires, 0 if no signal was received.
        signalToSendStrength (float): The strength of the signal this neuron will send to the neurons at the end of its
            outgoing connections during the current round of neuron fires.
        totalNumberOfFires (int): How many times this neuron has fired.
    """

    def __init__(self, name):
        """The constructor for the Neuron class.

        Args:
            name (str): The name of the neuron.
        """
        self.name = name
        self.outgoingConnections = []
        self.alreadyFired = False
        self.addConnectedMuscles()
        self.signalReceivedStrength = 0
        self.signalToSendStrength = 0
        self.justFired = False
        self.totalNumberOfFires = 0
        self.neuronsNotConnectedTo = []

    def addConnection(self, receivingNeuronName, Type, nbr):
        """Add a Connection to this neurons outgoingConnections list.

        Args:
            receivingNeuronName (str): The name of the neuron at the receiving end of this connection.
            Type (str): The type of the Connection to add, with options "NMJ" (neuromuscular junction), "EJ" (electrical junction), or "R" (receiving, representing a chemical junction).
            nbr (int): The number of synapses of the Connection to add.
        """
        if(Type == "NMJ"):
            return
        self.outgoingConnections.append(
            Connection(receivingNeuronName, Type, nbr))

    def addConnectedMuscles(self):
        """Add all Connections of type NMJ from this Neuron to its outgoingConnections list by parsing the CSV file "NeuronFixedPoints.csv"."""
        with open('NeuronFixedPoints.csv') as csvDataFile:
            csvReader = csv.reader(csvDataFile)

            skippedFirstRow = False
            for row in csvReader:
                if(not skippedFirstRow):
                    skippedFirstRow = True
                    continue
                NeuronName = row[0]
                if(NeuronName == self.name):
                    Landmark = row[1]
                    if(Landmark != "Sensory" and Landmark != "SensoryNB"):
                        weight = float(row[3])
                        self.addConnectedMuscle(Landmark, weight)

    def addConnectedMuscle(self, muscleName, muscleWeight):
        """Add a Connection of type NMJ to this Neurons's outgoingConnections list.

        Args:
            muscleName (str): The name of the muscle at the receiving end of this connection.
            muscleWeight (float): The weight of the Connection to add.
        """
        self.outgoingConnections.append(
            Connection(muscleName, "NMJ", 1, muscleWeight))

    def fireGP(self, strength):
        """Fire a GP (graded potential) from this Neuron to the Neurons at the end of this Neuron's outgoingConnections.

        Args:
            strength (float): The strength of the graded potential to be sent.
        """
        global numberOfNeuronFires
        numberOfNeuronFires += 1
        self.justFired = True
        self.alreadyFired = True
        self.totalNumberOfFires += 1
        for connection in self.outgoingConnections:
            receivingNeuron = getNeuron(
                connection.receivingNeuronName)
            if(connection.Type == "NMJ"):
                muscle = getMuscle(connection.receivingNeuronName)
                if(muscle.alreadyActivated and exploreConnectivity):
                    continue
                muscle.activate()
            elif(connection.Type != "EJ"):
                receivingNeuron.receiveSignal(
                    strength * chemicalSignalDecayRate)
            else:
                receivingNeuron.receiveSignal(
                    strength * electricalSignalDecayRate)

    def receiveSignal(self, strength):
        """Receive a GP (graded potential) signal from another Neuron, and get ready to fire a graded potential during the next round of neuron fires if the strength of the signal received surpassed the firing threshold set in the command line.

        Args:
            strength (float): The strength of the graded potential received.
        """
        if(exploreConnectivity):
            if(not self.alreadyFired):
                self.signalReceivedStrength = 1
                return
            else:
                self.signalReceivedStrength = 0
                return

        if(strength < firingThreshold):
            return
        if(strength > self.signalReceivedStrength):
            self.signalReceivedStrength = strength


def resetReceivedSignals():
    """Set the signalReceivedStrength attribute of all the Neuron objects in the global Neurons list to 0."""
    for neuron in Neurons:
        neuron.signalReceivedStrength = 0


def resetToSendSignals():
    """Set the signalToSendStrength attribute of all the Neuron objects in the global Neurons list to 0."""
    for neuron in Neurons:
        neuron.signalToSendStrength = 0


def resetJustFiredBools():
    """Set the justFired attribute of all the Neuron objects in the global Neurons list and the justActivated attribute of all the Muscle objects in the global Muscles list to False."""
    for neuron in Neurons:
        neuron.justFired = False
    for muscle in Muscles:
        muscle.justActivated = False


def resetAlreadyFiredBools():
    """Set the alreadyFired attribute of all the Neuron objects in the global Neurons list and the alreadyActivated attribute of all the Muscle objects in the global Muscles list to False."""
    for neuron in Neurons:
        neuron.alreadyFired = False
    for muscle in Muscles:
        muscle.alreadyActivated = False


def printInfoAboutNeuronsThatJustFired():
    """Print a list of the neurons that fired and a list of the muscles that were activated during the last round of neuron fires."""
    str = "Neurons that fired: "
    for neuron in Neurons:
        if(neuron.justFired):
            str += neuron.name + " "
    print(str)

    str = "Muscles that activated: "
    for muscle in Muscles:
        if(muscle.justActivated):
            str += muscle.name + " "
    print(str)


def updateNeuronsNotConnectedTo(firingNeuron):
    """Set a Neuron's neuronsNotConnectedTo list to Neurons that, viewing the neural network as a graph, are unreachable from the Neuron.

    Args:
        firingNeuron (Neuron): The Neuron whose neuronsNotConnectedTo list will be set.
    """
    for neuron in Neurons:
        if(not neuron.alreadyFired):
            firingNeuron.neuronsNotConnectedTo.append(neuron)


def printNeuralConnectivityInfo(neuron):
    """Print the names of the Neurons in a Neuron's neuronsNotConnectedToList.

    Args:
        neuron (Neuron): The Neuron whose neuronsNotConnectedTo list will be printed.
    """
    str = neuron.name + " cannot reach the following neurons: "
    for i, unconnectedNeuron in enumerate(neuron.neuronsNotConnectedTo):
        str += unconnectedNeuron.name
        if(i < len(neuron.neuronsNotConnectedTo)):
            str += ", "
    print(str)
    print("")


def printNeuronNonConnectivites():
    """Print the names of the Neurons in every Neuron's neuronsNotConnectedToList."""
    for neuron in Neurons:
        printNeuralConnectivityInfo(neuron)


def fireReadyNeuronsAndResetAndReturnIfAnyNeuronsFired():
    """Perform a round of neuron fires."""
    resetJustFiredBools()
    anyNeuronsFired = False

    # Mark neurons with received signals as ready to fire, and change the
    # received signal as an about to send signal
    for neuron in Neurons:
        if(neuron.signalReceivedStrength > 0):
            neuron.signalToSendStrength = neuron.signalReceivedStrength

    # Reset the received signals, and let neurons with outgoing signals fire
    resetReceivedSignals()

    # Fire ready neurons
    for neuron in Neurons:
        if(neuron.signalToSendStrength > 0):
            anyNeuronsFired = True
            neuron.fireGP(neuron.signalToSendStrength)

    # Get rid of the ready to send signals, as they were just sent
    resetToSendSignals()
    return anyNeuronsFired


def printRoundNumber(roundNumber):
    """Print "ROUND (roundNumber)".

    Args:
        roundNumber (int)
    """
    stri = "ROUND " + str(roundNumber)
    print(stri)


def fireOriginalNeuron(
        originalNeuronName, originalSignalStrength, doPrintStatements):
    """Fire the neuron with name originalNeuronName.

    Fire the neuron with name originalNeuronName, or all the neurons sequentially if originalNeuronName is "ALL", with signal strength originalSignalStrength. Continue to
    fire neurons in rounds until all signals have decayed below the globally set firingThreshold. Alternatively, if the global bool exploreConnectivities is true,
    will fire all neurons that, viewing the neural network as a graph, are reachable from the original neuron.

    Args:
        originalNeuronName (str): The name of the Neuron to fire in the first round of Neuron fires. If "ALL", all the Neurons will be fired sequentially.
        originalSignalStrength (float): The strength with which the first Neuron will fire.
        doPrintStatements (bool): Should info be printed during the program.
    """
    if(originalNeuronName.upper() == "ALL"):
        for neuron in Neurons:
            resetAlreadyFiredBools()
            fireOriginalNeuron(neuron.name, originalSignalStrength, False)
            resetReceivedSignals()
        return
    firingNeuron = getNeuron(originalNeuronName)
    if(firingNeuron == ""):
        print("Invalid neuron name")
        exit(0)
    firingNeuron.fireGP(originalSignalStrength)
    roundNumber = 1
    if(doPrintStatements):
        printRoundNumber(roundNumber)
        printInfoAboutNeuronsThatJustFired()
        print("")

    # Continue firing neurons until all the signals decay
    while(True):
        anyNeuronsFired = fireReadyNeuronsAndResetAndReturnIfAnyNeuronsFired()
        roundNumber += 1
        if(doPrintStatements):
            printRoundNumber(roundNumber)
            printInfoAboutNeuronsThatJustFired()
            print("")
        if(not anyNeuronsFired):
            updateNeuronsNotConnectedTo(getNeuron(originalNeuronName))
            return


def getNeuronWithMostFires():
    """Return the Neuron with the most fires."""
    mostFires = 0
    NeuronWithMostFires = Neurons[0]
    for neuron in Neurons:
        if(neuron.totalNumberOfFires > mostFires):
            mostFires = neuron.totalNumberOfFires
            NeuronWithMostFires = neuron
    return NeuronWithMostFires


def getNeuronWithLeastFires():
    """Return the Neuron with the least fires."""
    leastFires = 9999999999
    NeuronWithLeastFires = Neurons[0]
    for neuron in Neurons:
        if(neuron.totalNumberOfFires < leastFires):
            leastFires = neuron.totalNumberOfFires
            NeuronWithLeastFires = neuron
    return NeuronWithLeastFires


def addConnectionToNeurons(sendingNeuronName, receivingNeuronName, Type, nbr):
    """Add a connection to Neuron in Neurons list with name sendingNeuronName.

    Args:
        sendingNeuronName (str): The name of the Neuron from which the Connection to add is outgoing.
        receivingNeuronName (str): The name of the Neuron at the receiving end of the Connection to add.
        Type (str): The type of the Connection to add.
        nbr (int): The number of synapses of the Connection to add.
    """
    for neuron in Neurons:
        if neuron.name == sendingNeuronName:
            neuron.addConnection(receivingNeuronName, Type, nbr)
            return
    Neurons.append(Neuron(sendingNeuronName))


def getNeuron(neuronName):
    """Get the Neuron with name neuronName from the Neurons list.

    Args:
        neuronName (str): The name of the Neuron to get.
    """
    for neuron in Neurons:
        if neuron.name == neuronName:
            return neuron
    return ""


def getMuscle(muscleName):
    """Get the Muscle with name muscleName from the Muscles list.

    Args:
        neuronName (str): The name of the Muscle to get.
    """
    for muscle in Muscles:
        if muscle.name == muscleName:
            return muscle
    return ""


def fillNeuronsWithNames():
    """Fill the global Neurons list with Neuron objects with only their name set."""
    with open('NeuronConnect.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)

        skippedFirstRow = False
        for row in csvReader:
            if(not skippedFirstRow):
                skippedFirstRow = True
                continue

            shouldAdd = True
            neuronName = row[0]
            for neuron in Neurons:
                if neuron.name == neuronName:
                    shouldAdd = False
                    break
            if shouldAdd:
                Neurons.append(Neuron(neuronName))


def fillNeurons():
    """Update the global Neurons list with appropriate info for each Neuron."""
    with open('NeuronConnect.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)

        skippedFirstRow = False
        for row in csvReader:
            if(not skippedFirstRow):
                skippedFirstRow = True
                continue
            Type = row[2]

            # Avoiding adding duplicate connections by only adding sending
            # connections
            if(Type == "Rp" or Type == "R"):
                continue
            addConnectionToNeurons(row[0], row[1], row[2], float(row[3]))


def fillMuscles():
    """Fill the global Muscles list with Muscle objects."""
    with open('NeuronFixedPoints.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)

        skippedFirstRow = False
        for row in csvReader:
            if(not skippedFirstRow):
                skippedFirstRow = True
                continue

            Landmark = row[1]
            if(Landmark == "Sensory" or Landmark == "SensoryNB"):
                continue

            shouldAdd = True
            muscleName = row[1]

            for muscle in Muscles:
                if muscle.name == muscleName:
                    shouldAdd = False
                    break
            if shouldAdd:
                Muscles.append(Muscle(muscleName))


if __name__ == "__main__":
    # Global variables that are set by the user with the command line.
    firingNeuronName = "ALL"
    firingThreshold = 1
    exploreConnectivity = False
    chemicalSignalDecayRate = .8
    electricalSignalDecayRate = .4
    firingStrength = 2

    # Global variables used to keep track of statistics over the course of the
    # program's run.
    numberOfMuscleActivations = 0
    numberOfNeuronFires = 0

    # A global list of Neuron and Muscle objects
    Neurons = []
    Muscles = []

    # Get command line arguments
    argc = len(sys.argv)
    if(argc > 1):
        # Print help info and exit
        if(sys.argv[1] == "-h"):
            print(
                "To call the CESimulation.py function run" +
                "\n\tpython CESimulation.py <Firing Neuron Name> <Explore Connectivity> <Firing Threshold> <Chemical Signal Decay Rate> <Electrical Signal Decay Rate> <Firing Strength>" +
                "\nwhere all the arguments are optional and will be replaced by default values if not specified." +
                "\n\nFiring neuron name: The name of the neuron you want to fire, with names from NeuroConnect.csv. Set to ALL to fire all neurons sequentially and print some interesting statistics." +
                "\nExplore Connectivity: If \"True\", each neuron will fire only once, but signals will not decay (remaining parameters meaningless). Combine \"True\" with \"ALL\" as the firing neuron\n\tname to see which neurons are reachable from other neurons." +
                "\nFiring threshold: The signal strength that a neuron must receive to fire." +
                "\nChemical Signal Decay Rate: How much a signal decays when sent through a chemical synapse. (Strength of signal received = strength of sent signal * chemical decay rate)" +
                "\nElectrical Signal Decay Rate: How much a signal decays when sent through an electrical synapse (Strength of signal received = strength of sent signal * electrical decay rate)" +
                "\nFiring Strength: The signal strength with which the the neuron of the name <Firing Neuron Name> will fire. This signal is sent to all its outgoing connections.")
            exit(0)

        else:
            firingNeuronName = sys.argv[1]
    if(argc > 2):
        exploreConnectivity = (sys.argv[2].upper() == "TRUE")
    if(argc > 3):
        firingThreshold = float(sys.argv[3])
        if(firingThreshold <= 0):
            print("Firing threshold must be greater than 0 (arg3)")
            exit(0)
    if(argc > 4):
        chemicalSignalDecayRate = float(sys.argv[4])
        if(chemicalSignalDecayRate >= 1):
            print("Chemical signal decay rate must be lower than one (arg 4)")
            exit(0)
        elif(chemicalSignalDecayRate < 0):
            print("Chemical signal decay rate must be positive (arg4)")
            exit(0)
    if(argc > 5):
        electricalSignalDecayRate = float(sys.argv[5])
        if(electricalSignalDecayRate >= 1):
            print("Electrical signal decay rate must be lower than one (arg 5)")
            exit(0)
        elif(electricalSignalDecayRate < 0):
            print("Electrical signal decay rate must be positive (arg5)")
            exit(0)
    if(argc > 6):
        firingStrength = float(sys.argv[6])
        if(firingStrength < 0):
            print("Firing strength must be positive (arg6)")
            exit(0)

    # Populate the Neurons and Muscles arrays
    fillNeuronsWithNames()
    fillNeurons()
    fillMuscles()

    # Fire the first firing Neuron
    fireOriginalNeuron(firingNeuronName, firingStrength, True)

    # Print interesting statistics
    if(not exploreConnectivity):
        stri = "Muscles activated " + \
            str(numberOfMuscleActivations) + " times!"
        print(stri)
        stri = "Neurons fired " + str(numberOfNeuronFires) + " times!"
        print(stri)

    if(firingNeuronName.upper() != "ALL" and not exploreConnectivity):
        print("Following muscles activated:")
        for muscle in Muscles:
            if (muscle.alreadyActivated):
                print("\t" + muscle.name)

    if(exploreConnectivity):
        if(firingNeuronName.upper() == "ALL"):
            printNeuronNonConnectivites()
        else:
            printNeuralConnectivityInfo(getNeuron(firingNeuronName))

    NeuronWithMostFires = getNeuronWithMostFires()
    NeuronWithLeastFires = getNeuronWithLeastFires()

    if(firingNeuronName.upper() == "ALL" and not exploreConnectivity):
        str = "Neuron with the most fires was " + NeuronWithMostFires.name
        print(str)
        str = "Neuron with the least fires was " + NeuronWithLeastFires.name
        print(str)
