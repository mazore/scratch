from blocks.control_block import ControlBlock
from block_children import *


class IfBlock(ControlBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y, top_part_height=35, children_y_offset=-3, min_width=100)

        self.children = [Text(self, 'if'),
                         Field(self),
                         Text(self, 'then')]

        super().children_config()

    def run(self, run_number):
        try:
            if eval(str(self.children[1].val)):
                if self.inside_block is not None:
                    self.inside_block.run(run_number)
            else:
                if self.below is not None:
                    self.below.run(run_number)
                self.after_run(run_number)
        except (NameError, TypeError, ValueError):
            print(f'{type(self).__name__}: Input not valid')

    def contents_done(self, run_number):
        if self.below is not None:
            self.below.run(run_number)
        self.after_run(run_number)
