from block_children.field import Field
import tkinter as tk


class Dropdown(Field):
    def add_entry(self, _=None):
        root = self.parent_block.coding_area.root
        options = root.vars.keys() if len(root.vars) != 0 else ['x']
        menu = tk.OptionMenu(root, self.var, *options)
        self.entry_id = self.parent_block.coding_area.create_window(self.left, self.mid_y, window=menu,
                                                                    width=self.width + 1, height=20, anchor='w')
        for event_name in ['<Return>', '<Escape>']:
            menu.bind(event_name, lambda _: self.remove_entry(event_name))
        menu.bind('<Tab>', self.tab)
        menu.focus()
