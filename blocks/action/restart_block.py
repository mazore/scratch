from blocks.action_block import ActionBlock
from block_children import *


class RestartBlock(ActionBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y, flat_bottom=True)

        self.children = [Text(self, 'restart script')]

        super().children_config()

    def run(self, _=None):
        self.coding_area.root.run()
