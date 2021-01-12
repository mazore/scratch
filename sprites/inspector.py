import tkinter as tk


class Inspector(tk.Frame):
    def __init__(self, sprite_manager):
        self.sprite_manager = sprite_manager

        super().__init__(bd=1, bg='white', relief='solid')
        self.place(x=795, y=320, width=95, height=170)

        self.selected_sprite = None

        self.name_var = tk.StringVar()
        self.x_var = tk.IntVar()
        self.y_var = tk.IntVar()
        self.w_var = tk.IntVar()
        self.h_var = tk.IntVar()

        self.name_var.trace('w', self.update_sprite_properties)
        self.x_var.trace('w', self.update_sprite_properties)
        self.y_var.trace('w', self.update_sprite_properties)
        self.w_var.trace('w', self.update_sprite_properties)
        self.h_var.trace('w', self.update_sprite_properties)

        self.frame_x = tk.Frame(self)
        self.frame_y = tk.Frame(self)
        self.frame_w = tk.Frame(self)
        self.frame_h = tk.Frame(self)

        tk.Label(self.frame_x, text='x =', bg='white').pack(side='left')
        tk.Label(self.frame_y, text='y =', bg='white').pack(side='left')
        tk.Label(self.frame_w, text='w =', bg='white').pack(side='left')
        tk.Label(self.frame_h, text='h =', bg='white').pack(side='left')
        self.name_field = tk.Entry(self, relief='solid', textvariable=self.name_var, insertwidth=1)
        self.name_field.bind('<FocusIn>', lambda _: self.name_field.select_range(0, 'end'))
        tk.Spinbox(self.frame_x, relief='solid', repeatinterval=10, textvariable=self.x_var, from_=0, to=300,
                   insertwidth=1).pack(padx=2, side='left')
        tk.Spinbox(self.frame_y, relief='solid', repeatinterval=10, textvariable=self.y_var, from_=0, to=300,
                   insertwidth=1).pack(padx=2, side='left')
        tk.Spinbox(self.frame_w, relief='solid', repeatinterval=20, increment=1, textvariable=self.w_var,
                   from_=0, to=1000, insertwidth=1).pack(padx=2, side='left')
        tk.Spinbox(self.frame_h, relief='solid', repeatinterval=20, increment=1, textvariable=self.h_var,
                   from_=0, to=1000, insertwidth=1).pack(padx=2, side='left')

    def inspect_sprites(self, sprites):
        if len(sprites) != 1:  # hide
            self.name_field.pack_forget()
            self.frame_x.pack_forget()
            self.frame_y.pack_forget()
            self.frame_w.pack_forget()
            self.frame_h.pack_forget()
            return
        # show
        self.name_field.pack(padx=2, pady=2, side='top')
        self.frame_x.pack(side='top')
        self.frame_y.pack(side='top')
        self.frame_w.pack(side='top')
        self.frame_h.pack(side='top')

        self.selected_sprite = sprite = sprites[0]
        x, y, w, h = sprite.x, sprite.y, sprite.w, sprite.h
        self.name_var.set(sprite.name)
        self.x_var.set(x)
        self.y_var.set(y)
        self.w_var.set(w)
        self.h_var.set(h)

    def update_sprite_properties(self, *_):
        if self.selected_sprite is None:
            return
        if self.selected_sprite.name != self.name_var.get():
            self.selected_sprite.rename(self.name_var.get())
        try:
            x, y, w, h = self.x_var.get(), self.y_var.get(), self.w_var.get(), self.h_var.get()
        except tk.TclError:  # if input not valid
            return
        self.sprite_manager.move_sprite_to(self.selected_sprite, x, y, w, h)
