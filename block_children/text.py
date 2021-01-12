from helpers import constrain


class Text:
    def __init__(self, parent_block, text, padding=(0, 0), y_offset=0):
        self.parent_block = parent_block

        self.is_draggable = True
        self.held_block = None

        self.padding = padding
        self.x_offset = None
        self.y_offset = y_offset

        self.text = text
        self.width = None
        self.id = None

    def setup(self):
        self.id = self.parent_block.coding_area.create_text(self.left, self.top, text=self.text,
                                                            fill='white', anchor='w'),

    def update_width(self):
        id_ = self.parent_block.coding_area.create_text(0, 0, text=self.text, anchor='w')
        x1, _, x2, _ = self.parent_block.coding_area.bbox(id_)
        self.parent_block.coding_area.delete(id_)
        self.width = constrain(float(x2) - float(x1) + 3, min_val=13)

    @property
    def left(self):
        return self.parent_block.x + self.x_offset

    @property
    def top(self):
        return self.parent_block.y + self.parent_block.height / 2 - self.y_offset

    def update_pos(self):
        self.parent_block.coding_area.coords(self.id, self.left, self.top)

    @staticmethod
    def encode():
        return {}
