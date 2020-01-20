import xml.etree.ElementTree as ET
from Node import Node

attack_id = 0


class NotConOrDisError(Exception):
    def __init__(self):
        super().__init__('Gate must be conjuctive or disjunctive')


def parse_file(file):
    """
    Parse the xml file that created from ADTool
    :param file: The xml file that created from ADTool
    :return: The list of nodes that included in the given tool
    """
    doc = ET.parse(file)
    root = doc.getroot()
    root = root.find("node")
    nodes = []

    def parse_node(node, mother=None):
        """
        Parse the xml element Node to the class Node
        :param node: Target XML element
        :param mother: Mother node of target node
        :return: The node that was targeted.
        """
        if 'switchRole' in node.attrib and node.attrib['switchRole'] == 'yes':
            return -1
        name = node.find('label').text
        gate = node.attrib['refinement']
        if gate == 'disjunctive':
            gate = 'O'
        elif gate == 'conjunctive':
            gate = 'A'
        else:
            raise NotConOrDisError()

        global attack_id
        target = Node('<<ATTACK>>' + name.rstrip(), gate, 'ATTACK' + str(attack_id), mother)
        attack_id += 1
        nodes.append(target)

        for child in node.findall('node'):
            child_node = parse_node(child, target)
            if child_node != -1:
                target.add_child(child_node)

        if target.get_numChild() == 0:
            probability = node.find('comment').text
            target.set_prob(probability)

        return target

    return parse_node(root)
