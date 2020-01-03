from Node import Node


gate_id = {'O': 0, 'A': 0, 'P': 0, 'X': 0}


class OpenFTATypeError(Exception):
    def __init__(self):
        super().__init__('It is not a fault tree conducted only using M, B, and U')


def parse_file(file):
    """
    Parse the ftp file to make class Node
    :param file: Given ftp file to parse
    :return: The list of nodes that included in the given tool
    """
    faultTree_fta = open(file, "r")
    faultTreeFile_ped = faultTree_fta.readline().rstrip()
    faultTree_fta.readline()
    faultTree_fta.readline()

    def parse_node(mother=None):
        """
        Parse the ftp file line to the class Node
        :param mother: Mother node of target node
        :return: The node that was targeted.
        """
        line = faultTree_fta.readline().split(' ')

        if line[0] == 'M':
            line2 = faultTree_fta.readline().split(' ')

            desc = ''
            for des in line2[1:]:
                desc += des + ' '
            desc = desc[:-1].rstrip()

            if int(line[2]) == 0:
                target = Node(desc, 'A', line[1], mother)
            else:
                line3 = faultTree_fta.readline().split(' ')
                target = Node(desc, line3[0], line[1], mother)
                for i in range(int(line3[2])):
                    child = parse_node(target)
                    target.add_child(child)
        elif line[0] == 'B' or line[0] == 'U':
            target = Node(id=line[1], mother=mother)
        else:
            raise OpenFTATypeError()

        return target

    target_tree = parse_node()
    faultTree_fta.close()
    return target_tree, faultTreeFile_ped


def create_fta(integrated_tree, ped_line, origin_fta, origin_ped):
    """
    Create new fta file based on treeList
    :param integrated_tree: Integrated tree
    :param ped_line: Additional ped lines from attack tree
    :param origin_fta: Original file of fta to get original file name
    :param origin_ped: Original file of ped to get file name and lines
    :return:
    """
    new_fta_name = origin_fta.split('.')[0] + '_integrated.fta'
    new_ped_name = origin_ped.split('.')[0] + '_integrated.ped'

    new_fta_file = open(new_fta_name, 'w')
    new_fta_file.write(new_ped_name + '\n')
    new_fta_file.write('S NULL 0\n')
    new_fta_file.write('0\n')

    def write_node(node):
        global gate_id
        if node.get_numChild() > 0:
            new_fta_file.write('M ' + node.get_id() + ' 1\n')
            new_fta_file.write(str(len(node.get_name())) + ' ' + node.get_name() + '\n')
            new_fta_file.write(node.get_gate() + ' ' + node.get_gate() + str(gate_id[node.get_gate()]) + ' ' + str(node.get_numChild()) + '\n')
            gate_id[node.get_gate()] += 1

            node_children = node.get_children()
            for i in range(len(node_children)):
                write_node(node_children[i])
        else:
            new_fta_file.write('B ' + node.get_id() + ' 0\n')

    write_node(integrated_tree)
    new_fta_file.close()

    new_ped_file = open(new_ped_name, 'w')

    with open(origin_ped, 'r') as origin_file:
        for line in origin_file:
            new_ped_file.write(line)

    for line in ped_line:
        new_ped_file.write(line + '\n')

    new_ped_file.close()
