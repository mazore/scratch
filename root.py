from constants import WIDTH, HEIGHT
from coding_area import CodingArea
import datetime
from event_manager import EventManager
import json
import os
from sprites import SpriteManager
import tkinter as tk
from tkinter import filedialog, messagebox


class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry(f'{WIDTH}x{HEIGHT}+100+100')
        self.title('Scratch')

        self.running = False
        self.run_number = 0
        self.chunks_finished = 0
        self.filename = None
        self.d = None

        self.blocks = []
        self.vars = {}
        self.event_manager = EventManager(self)
        self.coding_area = CodingArea(self)
        self.sprite_manager = SpriteManager(self)

        kwargs = dict(bg='white', relief='solid', bd=1)
        self.run_button = tk.Button(text='run', command=self.run, **kwargs)
        self.run_button.place(x=0, y=0)
        tk.Button(text='stop', command=self.stop, **kwargs) \
            .place(x=0, y=25)
        tk.Button(text='save', command=self.save, **kwargs) \
            .place(x=0, y=50)
        tk.Button(text='open', command=self.load, **kwargs) \
            .place(x=0, y=75)

        self.initial_d = self.encode()

        self.bind('<Button-1>', self.clicked)
        self.protocol('WM_DELETE_WINDOW', self.on_quit)

        self.mainloop()

    def clicked(self, event):
        if event.widget is self.sprite_manager.sprite_listbox:
            self.sprite_manager.sprite_listbox.clicked(event)

    def on_quit(self):
        # don't ask to save if no changes made
        def key1(block):  # sort sprites
            return block['name'] + str(block['x']) + str(block['y'])

        def key2(block):  # sort blocks
            return block['type'] + str(block['x']) + str(block['y'])

        def sort(d):
            return (sorted(d['sprite_manager']['sprites'], key=key1),
                    sorted(d['coding_area']['blocks'], key=key2))

        current = sort(self.encode())
        if self.d is not None:
            original = sort(self.d)
        else:
            original = sort(self.initial_d)

        if current == original:
            self.destroy()
            return
        result = messagebox.askyesnocancel("Save", "Would you like to save?")
        if result is None:  # cancel
            return
        if result:
            self.save()
        self.destroy()

    @property
    def session(self):
        return None if not self.running else self.run_number

    def run(self, _=None):
        self.run_button.configure(bg='gray75')
        self.running = True
        self.run_number += 1
        self.chunks_finished = 0
        self.event_manager.run_event('run')

    def chunk_finished(self):
        self.chunks_finished += 1
        if self.chunks_finished == len(self.event_manager.subscriptions['run']) - 1:
            self.stop()

    def stop(self):
        self.run_button.configure(bg='SystemButtonFace')
        self.running = False

    def save(self):
        initial_file = os.path.dirname(__file__) + '/saves' if self.filename is None else self.filename
        filename = filedialog.asksaveasfilename(initialfile=initial_file)
        if filename == '':  # cancel
            return
        if os.path.exists(filename):
            with open(filename, 'r') as overwritten:
                dt = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
                with open(f'saves/overwritten/{dt}.json', 'w') as write:
                    write.write(overwritten.read())
        with open(filename, 'w') as file:
            json.dump(self.encode(), file, indent=4)

    def encode(self):
        return {
            'sprite_manager': self.sprite_manager.encode(),
            'coding_area': self.coding_area.encode()
        }

    def load(self):
        file = filedialog.askopenfile(initialdir=os.path.dirname(__file__) + '/saves')
        if file is None:  # cancel
            return
        self.filename = file.name

        self.d = json.load(file)
        self.sprite_manager.load(self.d['sprite_manager'])
        self.coding_area.load(self.d['coding_area'])
