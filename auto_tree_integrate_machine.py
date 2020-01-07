import sys
import ADTool_parser
import OpenFTA_parser
from Node import Node


def parse_attack_tree(integration_config):
    """
    Parse attack tree, and integrate trees that has same target.
    :param integration_config: Configuration file that includes the information of attack tree and a target
    :return: Dictionary that has key as the target fault, and value as the attack tree.
    """
    config = open(integration_config, 'r')
    config_lines = config.readlines()
    config.close()

    integrate_target = {}
    for line in config_lines:
        line = line.split('\t')

        if line[1].rstrip() in integrate_target:
            integrate_target[line[1].rstrip()].append(ADTool_parser.parse_file(line[0]))
        else:
            integrate_target[line[1].rstrip()] = [ADTool_parser.parse_file(line[0])]

    for key in integrate_target:
        if len(integrate_target[key]) > 1:
            integrate_target[key] = ADTool_parser.merge_attack_tree(integrate_target[key], '<<ATTACK>> Attack targeting ' + key)
        else:
            integrate_target[key] = integrate_target[key][0]

    return integrate_target


def integrate_tree(parsedFaultTree, parsedAttackTrees):
    """
    Integrate attack tree and fault tree
    :param parsedFaultTree: The top node of parsed OpenFTA fault tree.
    :param parsedAttackTrees: Dictionary that has key as the target fault, and value as the attack tree.
    :return:
    """

    def search_node(start, target):
        """
        Search node that has name target
        :param start: Start node to find.
        :param target: The target name to find.
        :return:
        """
        if start.get_name() == target:
            return start
        else:
            for child in start.get_children():
                ans = search_node(child, target)
                if ans != -1:
                    return ans
        return -1

    ped_lines = []
    merge_id = 0
    for key in parsedAttackTrees:
        target_node = search_node(parsedFaultTree, key)
        target_attack_tree = parsedAttackTrees[key][0]
        additional_ped_line = parsedAttackTrees[key][1]

        if target_node.get_numChild() > 0:
            merged_node = Node(target_node.get_name() + '_merged', 'O', 'MERGE' + str(merge_id))

            merged_node.add_child(target_node)
            if target_node.get_mother() is not None:
                target_node.get_mother().remove_child(target_node)
                merged_node.set_mother(target_node.get_mother())
            target_node.set_mother(merged_node)

            merged_node.add_child(target_attack_tree)
            target_attack_tree.set_mother(merged_node)

        else:
            target_node.set_gate(target_attack_tree.get_gate())
            for child in target_attack_tree.get_children():
                target_node.add_child(child)
                child.set_mother = target_node

        ped_lines.extend(additional_ped_line)

    return parsedFaultTree, ped_lines


if __name__ == '__main__':
    faultTreeFile_fta = sys.argv[1]
    faultTreeFile_dirs = sys.argv[1].split('/')[:-1]
    faultTreeFile_dir = ''
    for dirs in faultTreeFile_dirs:
        faultTreeFile_dir += dirs + '/'
    integration_config = sys.argv[2]

    parsedAttackTrees = parse_attack_tree(integration_config)
    parsedFaultTree, faultTreeFile_ped = OpenFTA_parser.parse_file(faultTreeFile_fta)

    integrated_tree, integrated_ped = integrate_tree(parsedFaultTree, parsedAttackTrees)

    OpenFTA_parser.create_fta(integrated_tree, integrated_ped, faultTreeFile_fta, faultTreeFile_dir + faultTreeFile_ped)
