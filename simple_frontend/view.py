import tkinter as tk
import tkinter.font as tk_font
from common.utility import WordType


class View(tk.Tk):
    def __init__(self, pres, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.presenter = pres
        self._set_defaults()
        self._set_keybindings()
        self.render = GameFrame(self)

    def render_game(self, game_data):
        pass

    def _set_defaults(self):
        self.title('Typefight')
        self.focus_set()

    def _set_keybindings(self):
        send = self.presenter
        # keybinding for each english letter
        for x in range(ord('a'), ord('z')+1):
            letter = chr(x)
            self.bind(letter, send.send_letter)
            self.bind(letter.upper(), send.send_letter)

        self.bind("<BackSpace>", send.remove_letter)
        self.bind("<space>", send.publish_current_word)
        self.bind("<Return>", send.switch_user)
        # self.bind("<Tab>", self._switch_typing_mode)

    def run(self):
        self.mainloop()


class GameFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._set_defaults()
        self._create_splits()

    def set_player_message(self, message):
        self.player.set_message(message)

    def add_word(self, w_type, word):
        if w_type == WordType.RIVAL:
            self.rival.add_word(WordType.DEFEND, word)
        else:
            self.player.add_word(w_type, word)

    def remove_word(self, w_type, word):
        if w_type == WordType.RIVAL:
            self.rival.remove_word(WordType.DEFEND, word)
        else:
            self.player.remove_word(w_type, word)

    def clear_game(self):
        self.player.clear_frame()
        self.rival.clear_frame()

    def _create_splits(self):
        left_pane = tk.Frame(self, width=500, height=800)
        right_pane = tk.Frame(self, width=500, height=800)
        left_pane.grid(row=0, column=0)
        right_pane.grid(row=0, column=1)
        self.player = UserFrame(left_pane, text='Player')
        self.rival = UserFrame(right_pane, text='Rival')

    def _set_defaults(self):
        self['width'] = 1000
        self['height'] = 800
        self.pack()


class UserFrame(tk.LabelFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._set_defaults()
        self.font = tk_font.Font(family="Lucida Grande", size=26)
        self.input_message = tk.Label(self, font=self.font)
        self.input_message.pack()
        self.defense = {}
        self.attack = {}

    def set_message(self, message):
        self.input_message['text'] = message

    def remove_word(self, w_type, word):
        if w_type == WordType.ATTACK:
            self.attack[word].grid_forget()
            self.attack.pop(word)
        else:
            self.defense[word].grid_forget()
            self.defense.pop(word)

    def add_word(self, w_type, word):
        label = tk.Label(self, text=word)
        if w_type == WordType.ATTACK:
            label.grid(column=2)
            self.attack[word] = label
        else:
            label.grid(column=1)
            self.defense[word] = label

    def clear_frame(self):
        self.set_message('')
        for k, v in self.attack.items():
            v.grid_forget()
        for k, v in self.defense.items():
            v.grid_forget()
        self.attack = {}
        self.defense = {}

    def _set_defaults(self):
        self['width'] = 450
        self['height'] = 700
        self.place(relx=.5, rely=.5, anchor="center")
        self.pack_propagate(False)
        self.grid_propagate(False)
