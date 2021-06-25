from blocks import *
from constants import BLOCK_BAR_WIDTH, CODING_AREA_WIDTH, CODING_AREA_HEIGHT
from helpers import constrain
from snap_point import SnapPoint
import tkinter as tk


class CodingArea(tk.Canvas):
    def __init__(self, root):
        self.root = root

        super().__init__(root, bd=1, bg='white', relief='solid')
        self.place(x=40, y=10, width=CODING_AREA_WIDTH, height=CODING_AREA_HEIGHT)

        # Separator
        f = tk.Frame(width=CODING_AREA_WIDTH, highlightbackground='black', highlightthickness=1)
        self.create_window(BLOCK_BAR_WIDTH, CODING_AREA_HEIGHT / 2, window=f,
                           width=1, height=CODING_AREA_HEIGHT - 6)
        self.bind('<MouseWheel>', self.scrolled)
        self.scroll_y = 0

        self.check_ids = []
        self.check_start_ys = []
        self.shown_vars = []
        self.shown_var_ids = {}

        self.bind('<Button-1>', self.clicked)

        self.blocks = []
        y = 10
        for block_type in block_types:
            if block_type.__name__ == 'GetBlock':
                continue
            self.blocks.append(block_type(self, 10, y))
            block = self.blocks[-1]
            if block.top_notch_height != 0:
                y += block.top_notch_height
                block.y = block.start_y = y
                block.update_pos()
            y += block.height + block.bottom_notch_height + 5
        self.refresh_var_blocks()

    def scrolled(self, event):
        if event.x < BLOCK_BAR_WIDTH:
            self.remove_all_entries()

            height = 0
            for block in self.blocks:
                height += block.height + block.bottom_notch_height + block.top_notch_height + 5
            height -= 300
            self.scroll_y = constrain(self.scroll_y + event.delta/3, min_val=-height, max_val=0)

            for block in self.blocks:
                if block.x < BLOCK_BAR_WIDTH:
                    block.y = block.start_y + self.scroll_y
                    block.update_pos()
            for check_id, check_start_y in zip(self.check_ids, self.check_start_ys):
                self.coords(check_id, 20, check_start_y + self.scroll_y)

    def refresh_var_blocks(self):
        for check_id in self.check_ids:
            self.delete(check_id)
        self.check_ids = []
        self.check_start_ys = []

        var_names = set()
        for block in self.blocks[::-1]:
            if isinstance(block, SetBlock):
                var_names.add(block.children[1].val)
            if isinstance(block, GetBlock) and block.held_by_field is None:
                block.remove()
        y = 875
        for var_name in sorted(var_names):
            y += 33
            block = GetBlock(self, 30, y)
            block.y += self.scroll_y
            block.update_pos()
            block.set_var_name(var_name)
            self.blocks.append(block)

            window = tk.Checkbutton(bg='white', command=lambda *_, x=var_name: self.check_changed(x))
            if var_name in self.shown_vars:
                window.select()
            self.check_ids.append(self.create_window(20, y+12+self.scroll_y, window=window, width=15, height=15))
            self.check_start_ys.append(y+12)

    def check_changed(self, var_name):
        if var_name in self.shown_vars:  # hide var
            self.shown_vars.remove(var_name)
            self.root.sprite_manager.stage.delete(self.shown_var_ids[var_name])
            del self.shown_var_ids[var_name]
        else:  # show var
            self.shown_vars.append(var_name)
            stage = self.root.sprite_manager.stage
            y = len(self.shown_var_ids) * 30 + 5
            text = f'{var_name}: 0'
            self.shown_var_ids[var_name] = stage.create_text(10, y, text=text, anchor='nw')

    def clicked(self, event):
        if len(self.find_overlapping(event.x, event.y, event.x + 1, event.y + 1)) == 0:
            self.remove_all_entries()

    def remove_all_entries(self):
        for block in self.blocks:
            for child in block.children:
                if hasattr(child, 'remove_entry'):
                    child.remove_entry()

    def get_top_blocks(self):
        top_blocks = set()
        for block in self.blocks:
            top_blocks.add(block.get_top_block())
        return list(top_blocks)

    def encode(self):
        return {
            'blocks': [top_block.encode() for top_block in self.get_top_blocks()]
        }

    def load(self, d):
        self.scroll_y = 0
        for block in self.get_top_blocks():
            block.remove()

        for block in d['blocks']:
            self.load_block(block)

        for block in self.get_top_blocks():
            for _ in range(5):
                block.update_pos()

        self.refresh_var_blocks()

    def load_block(self, d):
        keys = ['type', 'x', 'y', 'children', 'below', 'inside_block']
        t = (d[key] for key in keys)
        type_, x, y, children, below, inside_block = t
        block = eval(f'{type_}(self, {x}, {y})')

        if 'var_name' in d:
            block.set_var_name(d['var_name'])

        if below is not None:
            block.below = self.load_block(below)
            block.below.above = block
        if inside_block is not None:
            block.inside_block = self.load_block(inside_block)
            block.inside_block.above = block

        for child_dict, child in zip(children, block.children):
            if hasattr(child, 'var') and 'val' in child_dict:
                child.var = tk.StringVar(value=child_dict['val'])
                child.var.trace('w', child.var_changed)
                child.var_changed()
            if hasattr(child, 'held_block') and 'held_block' in child_dict and child_dict['held_block'] is not None:
                held_block = self.load_block(child_dict['held_block'])
                child.held_block = held_block
                held_block.held_by_field = child
                held_block.snap_point = SnapPoint(child.left, child.top, child.on_snapped_to,
                                                  on_detach=child.on_detached_from)
        block.update_dimensions()

        self.blocks.append(block)
        return block
