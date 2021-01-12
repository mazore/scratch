from blocks.action_block import ActionBlock
from block_children import *


class WaitBlock(ActionBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y)

        self.children = [Text(self, 'wait'),
                         Field(self, default='2'),
                         Text(self, 'seconds')]

        super().children_config()

    def run(self, run_number):
        time = float(self.children[1].val)
        try:
            self.coding_area.root.after(int(time*1000), lambda: self.after_wait(run_number))
        except ValueError:
            print(f'{type(self).__name__}: Input not valid')

    def after_wait(self, run_number):
        if self.coding_area.root.session == run_number:
            if self.below is not None:
                self.below.run(run_number)
            else:
                self.after_run(run_number)
