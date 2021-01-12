from sprites.inspector import Inspector
from sprites.sprite import Sprite
from sprites.sprite_listbox import SpriteListbox
from sprites.stage import Stage


class SpriteManager:
    def __init__(self, root):
        self.root = root

        self.inspector = Inspector(self)
        self.stage = Stage(self)
        self.sprite_listbox = SpriteListbox(self)

        self.sprites = []
        self.sprites.append(Sprite(self))

        self.deselect_all()

    @property
    def sprite_names(self):
        tags = []
        for i in self.stage.find_all():
            tags.append(self.stage.gettags(i)[0])
        return tags

    def add_sprite(self):
        sprite = Sprite(self)
        self.sprites.append(sprite)
        self.select_sprite(sprite)
        self.refresh_selected_sprites()

    def delete_sprite(self, sprite):
        sprite.delete()
        self.sprites.remove(sprite)

    def delete_selected_sprites(self):
        for i in self.sprite_listbox.curselection()[::-1]:
            self.delete_sprite(self.get_sprite(i, 'listbox_index'))
        self.refresh_selected_sprites()

    def get_sprite(self, attr, attr_name):
        for sprite in self.sprites:
            if getattr(sprite, attr_name) == attr:
                return sprite

    def refresh_selected_sprites(self):
        sprites = [self.get_sprite(i, 'listbox_index') for i in self.sprite_listbox.curselection()]
        self.stage.show_selection(sprites)
        self.inspector.inspect_sprites(sprites)

    def deselect_all(self):
        self.sprite_listbox.selection_clear(0, 'end')
        self.refresh_selected_sprites()

    def select_sprite(self, sprite):
        self.sprite_listbox.selection_clear(0, 'end')
        self.sprite_listbox.selection_set(sprite.listbox_index)
        self.refresh_selected_sprites()

    def move_sprite_to(self, sprite, x, y, w, h):
        sprite.x, sprite.y, sprite.w, sprite.h = x, y, w, h
        self.stage.coords(sprite.id, x, y, x+w, y+h)

    def encode(self):
        return {
            'sprites': [sprite.encode() for sprite in self.sprites]
        }

    def load(self, d):
        [self.delete_sprite(sprite) for sprite in list(self.sprites)[::-1]]
        for sprite in d['sprites']:
            self.sprites.append(Sprite(self, **sprite))
        self.refresh_selected_sprites()
