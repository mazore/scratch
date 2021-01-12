from blocks.variable_block import VariableBlock
from block_children import *
from constants import BLOCK_BAR_WIDTH


class GetBlock(VariableBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y)

        self.var_name = None

    def set_var_name(self, var_name):
        self.children = [Text(self, var_name)]
        self.var_name = var_name

        super().children_config()

    def drag_start(self, event):
        super().drag_start(event)

        if self.x < BLOCK_BAR_WIDTH:  # add change new blocks var_name
            self.coding_area.blocks[-1].set_var_name(self.var_name)

    def run(self, _=None):
        try:
            return self.coding_area.root.vars[self.var_name]
        except KeyError:
            print(f'{type(self).__name__}: {self.var_name} not set yet')
            return 0

    def encode(self):
        return {
            'type': type(self).__name__,
            'x': self.x,
            'y': self.start_y,
            'children': [child.encode() for child in self.children],
            'below': None if self.below is None else self.below.encode(),
            'inside_block': self.inside_block.encode() if self.has_inside and self.inside_block is not None else None,
            'var_name': self.var_name
        }
