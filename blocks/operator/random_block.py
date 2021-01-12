from blocks.operator_block import OperatorBlock
from block_children import *
from random import randint


class RandomBlock(OperatorBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y)

        self.children = [Text(self, 'random'),
                         Field(self, default='1'),
                         Text(self, 'to'),
                         Field(self, default='10')]

        super().children_config()

    def run(self, _=None):
        try:
            return randint(int(self.children[1].val), int(self.children[3].val))
        except TypeError:
            print(f'{type(self).__name__}: Input not valid')
