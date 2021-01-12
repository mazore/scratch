from blocks.variable_block import VariableBlock
from block_children import *


class SetBlock(VariableBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y, is_action=True)

        self.children = [Text(self, 'set', padding=(0, 5)),
                         Field(self, default='score'),
                         Text(self, 'to'),
                         Field(self, default='0')]

        super().children_config()

    def drag_start(self, event):
        super().drag_start(event)

        self.coding_area.refresh_var_blocks()

    def run(self, run_number):
        var_name = self.children[1].val
        val = self.children[3].val
        self.coding_area.root.vars[var_name] = val
        stage = self.coding_area.root.sprite_manager.stage
        # stage.itemconfig(self.coding_area.shown_var_ids[var_name], text=f'{var_name}: {val}')
        if self.below is not None:
            self.below.run(run_number)
        self.after_run(run_number)
