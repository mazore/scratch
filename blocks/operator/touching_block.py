from blocks.operator_block import OperatorBlock
from block_children import *


class TouchingBlock(OperatorBlock):
    def __init__(self, coding_area, x, y):
        super().__init__(coding_area, x, y)

        self.children = [Field(self, default='Sprite1'),
                         Text(self, 'touching'),
                         Field(self, default='Sprite2')]

        super().children_config()

    def run(self, _=None):
        name1, name2 = self.children[0].val, self.children[2].val
        sprite1 = self.coding_area.root.sprite_manager.get_sprite(name1, 'name')
        sprite2 = self.coding_area.root.sprite_manager.get_sprite(name2, 'name')
        if sprite1 is None or sprite2 is None:
            print(f'{type(self).__name__}: Input not valid')
            return
        x1, y1, w1, h1 = sprite1.x, sprite1.y, sprite1.w, sprite1.h
        x2, y2, w2, h2 = sprite2.x, sprite2.y, sprite2.w, sprite2.h
        horizontal_touching = x1 + w1 > x2 > x1 - w2
        vertical_touching = y1 + h1 > y2 > y1 - h2
        return horizontal_touching and vertical_touching
