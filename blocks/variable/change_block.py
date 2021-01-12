from blocks.variable_block import VariableBlock
from block_children import *


class ChangeBlock(VariableBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y, is_action=True)

        self.children = [Text(self, 'change'),
                         Field(self, default='score'),
                         Text(self, 'by'),
                         Field(self, default='1')]

        super().children_config()

    def run(self, run_number):
        vars_ = self.coding_area.root.vars
        try:
            vars_[self.children[1].val] = float(vars_[self.children[1].val]) + float(self.children[3].val)
        except KeyError:
            print(f'{type(self).__name__}: {self.children[1].val} not set yet')
        except ValueError:
            print(f'{type(self).__name__}: Input not valid')
        if self.below is not None:
            self.below.run(run_number)
        self.after_run(run_number)
