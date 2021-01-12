from blocks.control_block import ControlBlock
from block_children import *


class ForeverBlock(ControlBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y, snappable_bottom=False, min_width=100)

        self.children = [Text(self, 'forever')]

        super().children_config()

    def run(self, run_number):
        if self.inside_block is not None:
            self.inside_block.run(run_number)

    def contents_done(self, run_number):
        if self.coding_area.root.session == run_number:
            self.coding_area.root.after(1000 // 60, lambda: self.inside_block.run(run_number))
