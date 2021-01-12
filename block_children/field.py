from helpers import constrain
from snap_point import SnapPoint
import tkinter as tk


class Field:
    def __init__(self, parent_block, default='', padding=(0, 3), y_offset=0):
        self.parent_block = parent_block

        self.is_draggable = False

        self.padding = padding
        self.x_offset = None
        self.width = None
        self.height = 18
        self.y_offset = y_offset

        self.var = tk.StringVar(parent_block.coding_area.root, default)
        self.var.trace('w', self.var_changed)
        self.held_block = None

        self.id = self.text_id = self.entry_id = None

    def setup(self):
        coding_area = self.parent_block.coding_area
        self.id = coding_area.create_rectangle(self.left, self.top, self.right, self.bottom, fill='white')
        self.text_id = coding_area.create_text(self.left + 2, self.mid_y, text=self.var.get(), anchor='w')

        self.parent_block.coding_area.tag_bind(self.id, '<Button-1>', self.add_entry)
        self.parent_block.coding_area.tag_bind(self.text_id, '<Button-1>', self.add_entry)

    def update_pos(self):
        self.parent_block.coding_area.coords(self.id, self.left, self.top,
                                             self.right, self.bottom)

        self.parent_block.coding_area.coords(self.text_id, self.left+2, self.mid_y)
        self.parent_block.coding_area.tag_raise(self.text_id)

        if self.held_block is not None:
            self.held_block.x = self.left
            self.held_block.y = self.mid_y - self.held_block.height/2
            self.held_block.update_pos()

    def update_width(self):
        id_ = self.parent_block.coding_area.create_text(0, 0, text=self.var.get(), anchor='w')
        x1, _, x2, _ = self.parent_block.coding_area.bbox(id_)
        self.parent_block.coding_area.delete(id_)
        self.width = constrain(float(x2) - float(x1) + 3, min_val=13)

    @property
    def val(self):
        if self.held_block is not None:
            return self.held_block.run()
        return self.var.get()

    @property
    def left(self):
        return self.parent_block.x + self.x_offset

    @property
    def right(self):
        return self.left + self.width

    @property
    def top(self):
        return self.parent_block.y + self.parent_block.height / 2 - self.height / 2 - self.y_offset

    @property
    def bottom(self):
        return self.top + self.height

    @property
    def mid_y(self):
        return (self.bottom + self.top) / 2

    def tab(self, _):
        children = self.parent_block.children
        i = children.index(self)
        while True:
            i += 1
            i %= len(children)
            if hasattr(children[i], 'add_entry'):
                break
        self.remove_entry()
        children[i].add_entry()

    def add_entry(self, _=None):
        entry = tk.Entry(textvariable=self.var, insertwidth=1, relief='solid', export=False)
        self.entry_id = self.parent_block.coding_area.create_window(self.left, self.mid_y, window=entry,
                                                                    width=self.width + 1, anchor='w')
        for event_name in ['<Return>', '<Escape>']:
            entry.bind(event_name, lambda _: self.remove_entry(event_name))
        entry.bind('<Tab>', self.tab)
        entry.focus()
        entry.select_range(0, 'end')
        entry.icursor('end')

    def remove_entry(self, _=None):
        if self.entry_id is not None:
            self.parent_block.coding_area.delete(self.entry_id)
        self.entry_id = None

    def var_changed(self, *_):
        self.parent_block.coding_area.itemconfig(self.text_id, text=self.var.get())
        self.update_entry_width()
        self.parent_block.coding_area.refresh_var_blocks()

    def update_entry_width(self):
        self.update_width()
        self.parent_block.coding_area.itemconfig(self.entry_id, width=self.width + 1)
        self.parent_block.update_dimensions()

    def get_held_blocks(self):
        if self.held_block is None:
            return []
        result = []
        for child in self.held_block.children:
            if hasattr(child, 'get_held_blocks'):
                result.extend(child.get_held_blocks())
        return [self.held_block] + result

    def get_snap_points(self, other):
        if not other.is_returning or self.held_block is not None:
            return []
        held_blocks = []
        for child in other.children:
            if hasattr(child, 'get_held_blocks'):
                held_blocks.extend(child.get_held_blocks())
        if self.parent_block in held_blocks:  # don't snap onto a held block's field
            return []
        return [SnapPoint(self.left, self.top, self.on_snapped_to, on_detach=self.on_detached_from)]

    def on_snapped_to(self, snap_point, other):
        other.x, other.y = snap_point.pos
        other.held_by_field = self
        self.held_block = other
        self.parent_block.update_dimensions()
        self.parent_block.coding_area.tag_raise(self.id)
        self.parent_block.get_top_block().update_pos()

    def on_detached_from(self, _, other):
        self.held_block.held_by_field = None
        self.held_block = None
        self.parent_block.update_dimensions()
        other.update_pos()
        self.parent_block.get_top_block().update_pos()

    def encode(self):
        return {
            'val': self.var.get(),
            'held_block': None if self.held_block is None else self.held_block.encode()
        }
