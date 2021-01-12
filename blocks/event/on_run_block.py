from blocks.event_block import EventBlock
from block_children import *


class OnRunBlock(EventBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y, 'run', min_width=100)

        self.children = [Text(self, 'On Run', padding=(5, 0), y_offset=5)]

        super().children_config()

    def run(self, run_number):
        if self.below is not None:
            self.below.run(run_number)
