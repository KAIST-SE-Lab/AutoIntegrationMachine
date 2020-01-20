class Node:
    def __init__(self, name=None, gate=None, id=None, mother=None, prob=None):
        """
        Constructor function of class Node
        :param name: The name(description) of the node
        :param gate: The type of the gate that linked with child nodes
        :param id: The id of the node
        :param mother: mother node
        :param prob: The probability of the node
        """
        self.name = name
        self.gate = gate
        self.id = id
        self.child = []
        self.mother = mother
        self.prob = prob

    def set_name(self, name):
        """
        Set the name(description) of the node by given parameter
        :param name: The name(description) that user want to give
        :return: None
        """
        self.name = name

    def get_name(self):
        """
        Return the name(description) of the node
        :return: The name(description) of the node
        """
        return self.name

    def set_gate(self, gate):
        """
        Set the gate of the node by given parameter
        :param gate: The gate that user want to give
        :return: None
        """
        self.gate = gate

    def get_gate(self):
        """
        Return the gate of the node
        :return: The gate of the node
        """
        return self.gate

    def set_mother(self, mother):
        """
        Set the mother of the node by given parameter
        :param mother: The gate that user want to give
        :return: None
        """
        self.mother = mother

    def get_mother(self):
        """
        Return the mother of the node
        :return: The mother of the node
        """
        return self.mother

    def get_id(self):
        """
        Return the id of the node
        :return: The id of the node
        """
        return self.id

    def get_numChild(self):
        """
        Return the number of child
        :return: The number of child
        """
        return len(self.child)

    def get_children(self):
        """
        Return the list of child
        :return: The list of child
        """
        return self.child

    def check_type(self, gate):
        """
        Check wheter gate type is the same with the given parameter
        :param gate: The parameter that want to check
        :return: Boolean value based on parameter
        """
        return self.gate == gate

    def add_child(self, child):
        """
        Add child node to the node
        :param child: The child node
        :return: None
        """
        self.child.append(child)

    def remove_child(self, child):
        """
        Remove given child node from the node
        :param child: Given node that want to remove from the parameter
        :return: None
        """
        self.child.remove(child)

    def find_child(self, child):
        """
        Return the boolean value whether it has given child or not
        :param child: Given child
        :return: The boolean value about the child
        """
        for my_child in self.child:
            if my_child == child:
                return True
        return False

    def set_prob(self, prob):
        """
        Set the probability of the node by given parameter
        :param prob: The gate that user want to give
        :return: None
        """
        self.prob = prob

    def get_prob(self):
        """
        Return the probability of the node
        :return: The probability of the node
        """
        return self.prob