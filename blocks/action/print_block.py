from blocks.action_block import ActionBlock
from block_children import *


class PrintBlock(ActionBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y)

        self.children = [Text(self, 'print'),
                         Field(self, default='Hello!')]

        super().children_config()

    def run(self, run_number):
        if self.children[1].val is not None:
            print(self.children[1].val)
        if self.below is not None:
            self.below.run(run_number)
        self.after_run(run_number)
