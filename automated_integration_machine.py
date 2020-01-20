import sys
import ADTool_parser
import OpenFTA_parser
from Node import Node

attackmerger_id = 0

def parse_attack_tree(attackTreeFiles, integration_config):
    """
    Parse attack trees, and integrate trees that has same target.
    :param attackTreeFiles: List of the attack tree files
    :param integration_config: Configuration file that includes the information of attack tree and a target
    :return: Dictionary that has key as the target fault, and value as the attack tree.
    """
    configs = {}
    config = open(integration_config, 'r')
    config_lines = config.readlines()
    config.close()

    for line in config_lines:
        line = line.split('\t')
        configs[line[0]] = line[1].rstrip()

    parsedAttackTrees = {}
    for tree in attackTreeFiles:
        attackTree = ADTool_parser.parse_file(tree)
        targetFault = configs[tree]
        if targetFault not in parsedAttackTrees:
            parsedAttackTrees[targetFault] = []
        parsedAttackTrees[targetFault].append(attackTree)

    return parsedAttackTrees


def attack_integration(parsedAttackTrees):
    """
    Integrate trees that has same target
    :param parsedAttackTrees: Dictionary that has key as the target fault, and value as the attack trees.
    :return: Dictionary that has key as the target fault, and value as the single attack tree.
    """
    for key in parsedAttackTrees:
        if len(parsedAttackTrees[key]) > 1:
            global attackmerger_id
            ans = Node('<<ATTACK>> Attack targeting ' + key, 'O', 'ATTACKMERGER' + str(attackmerger_id))
            attackmerger_id += 1
            for tree in parsedAttackTrees[key]:
                ans.add_child(tree[0])
                tree[0].set_mother = ans
            parsedAttackTrees[key] = ans
        else:
            parsedAttackTrees[key] = parsedAttackTrees[key][0]

    return parsedAttackTrees


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
        :return: If the node is find, return the node, otherwise return -1
        """
        if start.get_name() == target:
            return start
        else:
            for child in start.get_children():
                ans = search_node(child, target)
                if ans != -1:
                    return ans
        return -1

    merge_id = 0
    for key in parsedAttackTrees:
        target_node = search_node(parsedFaultTree, key)
        target_attack_tree = parsedAttackTrees[key]

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

    return parsedFaultTree


if __name__ == '__main__':
    faultTreeFile_fta = sys.argv[1]
    faultTreeFile_dirs = sys.argv[1].split('/')[:-1]
    faultTreeFile_dir = ''
    for dirs in faultTreeFile_dirs:
        faultTreeFile_dir += dirs + '/'
    integration_config = sys.argv[2]
    attackTreeFiles = sys.argv[3:]

    parsedFaultTree = OpenFTA_parser.parse_file(faultTreeFile_fta)
    parsedAttackTrees = parse_attack_tree(attackTreeFiles, integration_config)
    parsedAttackTrees = attack_integration(parsedAttackTrees)
    integrated_tree = integrate_tree(parsedFaultTree, parsedAttackTrees)
    OpenFTA_parser.create_fta(integrated_tree, faultTreeFile_fta)
