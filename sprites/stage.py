from constants import STAGE_X, STAGE_Y
import tkinter as tk


class Stage(tk.Canvas):
    def __init__(self, sprite_manager):
        self.sprite_manager = sprite_manager

        super().__init__(bd=1, bg='white', relief='solid')
        self.place(x=STAGE_X, y=STAGE_Y, width=300, height=300)

        self.drag = None

        self.bind('<ButtonPress-1>', self.mouse_down)
        self.bind('<Button1-Motion>', self.mouse_motion)
        self.bind('<ButtonRelease-1>', self.mouse_up)

    def mouse_down(self, event):
        closest = self.find_closest(event.x, event.y)
        if len(closest) == 0:
            return
        sprite_id = closest[0]
        sprite = self.sprite_manager.get_sprite(sprite_id, 'id')
        x, y, w, h = sprite.x, sprite.y, sprite.w, sprite.h
        if (not self.sprite_manager.root.running) and x < event.x < x+w and y < event.y < y+h:
            self.tag_raise(sprite_id)
            self.sprite_manager.select_sprite(sprite)
            self.drag = {
                'sprite': sprite,
                'sprite_start': (x, y),
                'screen_start': (event.x, event.y)
            }
        else:
            self.sprite_manager.root.event_manager.run_event('clicked')

    def mouse_motion(self, event):
        if self.drag is not None:
            keys = ['sprite', 'sprite_start', 'screen_start']
            sprite, sprite_start, screen_start = [self.drag[key] for key in keys]

            dx, dy = event.x - screen_start[0], event.y - screen_start[1]
            x, y = sprite_start[0] + dx, sprite_start[1] + dy
            w, h = sprite.w, sprite.h
            self.sprite_manager.move_sprite_to(sprite, x, y, w, h)
            self.sprite_manager.inspector.inspect_sprites([sprite])

    def mouse_up(self, _):
        if self.drag is None:
            self.sprite_manager.sprite_listbox.selection_clear(0, 'end')
            self.sprite_manager.refresh_selected_sprites()
            return
        self.sprite_manager.select_sprite(self.drag['sprite'])
        self.drag = None

    def show_selection(self, sprites):
        for i in self.find_all():
            if i in [sprite.id for sprite in sprites]:
                self.itemconfig(i, width=3, outline='orange')
            else:
                self.itemconfig(i, width=1, outline='black')
