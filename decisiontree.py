from treelib import Tree
from treelib import Node

import pprint

import game_state as ct

class GameTree(Tree):

    def __init__(self, current_turn: ct.CurrentTurn):
        self.game_tree: Tree = Tree()
        self.create_root_node(current_turn)
        

    def create_root_node(self, current_turn: ct.CurrentTurn) -> None:
        
        display_data: str = pprint.pformat(current_turn.__dict__)

        self.game_tree.create_node(
            tag=display_data, identifier="root"
        )

    def add_turn_node(self, current_turn: ct.CurrentTurn) -> None:

        display_data: str = pprint.pformat(current_turn.__dict__)

        node_data: dict[str:str] = current_turn.__dict__

        parent_node_identifier:str = current_turn.previous_node_identifier

        identifier:str = current_turn.current_node_identifier

        self.game_tree.create_node(
            tag=display_data, parent=parent_node_identifier, identifier=identifier, data=node_data
        )

    def show_node(self, nodeID:str) -> Node:
        return self.game_tree[nodeID]

    def show_tree(self):
        
        self.game_tree.to_graphviz("tree.dot")


