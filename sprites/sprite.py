from constants import COLORS
from helpers import rgb_to_hex
from random import choice, randint


class Sprite:
    def __init__(self, sprite_manager, name=None,
                 x=None, y=None, w=50, h=50, color=None):
        self.sprite_manager = sprite_manager

        num = 1
        while f'Sprite{num}' in [sprite.name for sprite in self.sprite_manager.sprites]:
            num += 1
        self.name = f'Sprite{num}' if name is None else name

        self.x = randint(0, 250) if x is None else x
        self.y = randint(0, 250) if y is None else y
        self.w, self.h = w, h
        self.color = choice(COLORS) if color is None else color

        self.listbox_index = self.sprite_manager.sprite_listbox.size()
        self.sprite_manager.sprite_listbox.insert('end', self.name)
        self.id = self.sprite_manager.stage.create_rectangle(self.x, self.y, self.x+self.w, self.y+self.h,
                                                             fill=rgb_to_hex(*self.color), outline='black')

    def delete(self):
        self.sprite_manager.sprite_listbox.delete(self.listbox_index)
        self.sprite_manager.stage.delete(self.id)

    def rename(self, name):
        selected = self.listbox_index in self.sprite_manager.sprite_listbox.curselection()
        self.name = name
        self.sprite_manager.sprite_listbox.delete(self.listbox_index)
        self.sprite_manager.sprite_listbox.insert(self.listbox_index, name)
        if selected:
            self.sprite_manager.sprite_listbox.selection_set(self.listbox_index)

    def encode(self):
        return {
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'w': self.w,
            'h': self.h,
            'color': self.color
        }
