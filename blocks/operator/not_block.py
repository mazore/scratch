from blocks.operator_block import OperatorBlock
from block_children import *


class NotBlock(OperatorBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y)

        self.children = [Text(self, 'not'),
                         Field(self, default='')]

        super().children_config()

    def run(self, _=None):
        return not self.children[1].val
