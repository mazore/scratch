from blocks.action_block import ActionBlock
from block_children import *


class MoveBlock(ActionBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y)

        self.children = [Text(self, 'move'),
                         Field(self, default='Sprite1'),
                         Text(self, 'to'),
                         Field(self, default='0'),
                         Text(self, ',', padding=(0, -5)),
                         Field(self, default='0')]

        super().children_config()

    def run(self, run_number):
        sprite_manager = self.coding_area.root.sprite_manager

        sprite_name = self.children[1].val
        x, y = self.children[3].val, self.children[5].val
        try:
            sprite = sprite_manager.get_sprite(sprite_name, 'name')
            if sprite is not None:
                sprite_manager.move_sprite_to(sprite, int(x), int(y), sprite.w, sprite.h)
            else:
                print(f'{type(self).__name__}: Sprite {sprite_name} does not exist')
        except ValueError:
            print(f'{type(self).__name__}: Input not valid')

        if self.below is not None:
            self.below.run(run_number)
        self.after_run(run_number)
