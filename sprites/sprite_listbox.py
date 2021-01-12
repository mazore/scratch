import tkinter as tk


class SpriteListbox(tk.Listbox):
    def __init__(self, sprite_manager):
        self.sprite_manager = sprite_manager

        self.var = tk.Variable(value=[])
        super().__init__(activestyle='none',     # remove underline from selected item
                         export=False,           # don't deselect when some other widget selects
                         highlightthickness=0,   # don't highlight border
                         relief='solid',         # have solid outline
                         selectmode='extended',  # allow shift and ctrl for selecting
                         listvariable=self.var)  # for retrieving the list of items
        self.place(x=690, y=320, width=95, height=170)
        self.bind('<MouseWheel>', self.scroll)

        self.popup_menu = tk.Menu(self, tearoff=False)
        self.popup_menu.add_command(label='Add', command=self.sprite_manager.add_sprite)
        self.popup_menu.add_command(label='Delete', command=self.sprite_manager.delete_selected_sprites)
        self.popup_menu.add_command(label='Deselect', command=self.sprite_manager.deselect_all)
        self.bind('<ButtonRelease-3>', self.popup)

        self.bind('<<ListboxSelect>>', self.selection_changed)
        self.bind('<Delete>', lambda _: self.sprite_manager.delete_selected_sprites())

    def clicked(self, event):
        num_sprites = len(self.sprite_manager.sprites)
        top_index = self.yview()[0] * num_sprites
        bottom_item_y = (num_sprites - top_index) * 16
        if event.y > bottom_item_y:
            self.sprite_manager.deselect_all()

    def scroll(self, event):
        self.yview_scroll(-1 * (event.delta//120), 'units')
        return 'break'

    def popup(self, event):
        width = self.popup_menu.winfo_reqwidth()
        self.popup_menu.tk_popup(event.x_root + int(width / 2), event.y_root + 10, 0)

    def selection_changed(self, _):
        self.sprite_manager.refresh_selected_sprites()
