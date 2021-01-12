from blocks.variable_block import VariableBlock
from block_children import *
from constants import STAGE_X, STAGE_Y


class MouseXBlock(VariableBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y)

        self.children = [Text(self, 'mouse x')]

        super().children_config()

    def run(self, _=None):
        root = self.coding_area.root
        return root.winfo_pointerx() - root.winfo_rootx() - STAGE_X


class MouseYBlock(VariableBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y)

        self.children = [Text(self, 'mouse y')]

        super().children_config()

    def run(self, _=None):
        root = self.coding_area.root
        return root.winfo_pointery() - root.winfo_rooty() - STAGE_Y
