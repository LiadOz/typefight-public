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
        for k, v in game_data.items():
            self.render.render_frame(k, v)

    def render_change(self, changes):
        for k, v in changes.items():
            self.render.render_changes(k, v)

    def _set_defaults(self):
        self.title('Typefight')
        self.focus_set()

    def _set_keybindings(self):
        send = self.presenter
        # keybinding for each english letter
        for x in range(ord('a'), ord('z') + 1):
            letter = chr(x)
            self.bind(letter, send.send_letter)
            self.bind(letter.upper(), send.send_letter)

        self.bind("<BackSpace>", send.remove_letter)
        self.bind("<space>", send.publish_current_word)
        self.bind("<Return>", send.switch_user)
        self.bind("<Tab>", send.switch_typing_mode)

    def run(self):
        self.mainloop()


class GameFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._set_defaults()
        self._create_splits()

    def set_player_message(self, message):
        self.player.set_message(message)

    def render_frame(self, user, payload):
        frame = None
        if user == 'PLAYER':
            frame = self.player
        elif user == 'RIVAL':
            frame = self.rival
        frame.clear_frame()
        if 'CURRENT' in payload:
            frame.set_message(payload['CURRENT'])
        if 'ATTACK' in payload:
            for word in payload['ATTACK']:
                frame.add_word(WordType.ATTACK, word)
        if 'DEFEND' in payload:
            for word in payload['DEFEND']:
                frame.add_word(WordType.DEFEND, word)

    def render_changes(self, player, changes):
        user = None
        if player == 'PLAYER':
            user = self.player
        elif player == 'RIVAL':
            user = self.rival
        for c_type, data in changes:
            if c_type == 'ADD_LETTER':
                message = user.get_message()
                user.set_message(message + data)
            elif c_type == 'REMOVE_LETTER':
                message = user.get_message()
                user.set_message(message[:-1])
            elif c_type == 'CLEAR_WORD':
                user.set_message('')
            elif c_type == 'ADD_ATTACK':
                user.add_word(WordType.ATTACK, data)
            elif c_type == 'ADD_DEFEND':
                user.add_word(WordType.DEFEND, data)
            elif c_type == 'REMOVE_ATTACK':
                user.remove_word(WordType.ATTACK, data)
            elif c_type == 'REMOVE_DEFEND':
                user.remove_word(WordType.DEFEND, data)

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
        self.player = UserGridFrame(left_pane, text='Player')
        self.rival = UserGridFrame(right_pane, text='Rival')

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

    def get_message(self):
        return self.input_message['text']

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
        attack = self.attack.items()
        defense = self.defense.items()
        for k, v in attack:
            v.grid_forget()
        for k, v in defense:
            v.grid_forget()
        self.attack = {}
        self.defense = {}

    def _set_defaults(self):
        self['width'] = 450
        self['height'] = 700
        self.place(relx=.5, rely=.5, anchor="center")
        self.pack_propagate(False)
        self.grid_propagate(False)


class UserGridFrame(UserFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.defend_frame = GridDefendFrame(self)
        self.attack_frame = tk.LabelFrame(self, text='ATTACK')
        self.defend_frame.pack()
        self.attack_frame.pack()

    def remove_word(self, w_type, word):
        if w_type == WordType.ATTACK:
            self.attack[word].pack_forget()
            self.attack.pop(word)
        else:
            self.defend_frame.remove_word(word)

    def add_word(self, w_type, word):
        if w_type == WordType.ATTACK:
            label = tk.Label(self.attack_frame, text=word)
            label.pack(side='left')
            self.attack[word] = label
        else:
            self.defend_frame.add_words(word)


class GridDefendFrame(tk.LabelFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, text='DEFEND', *args, **kwargs)
        self.words = {}

    def add_words(self, word):
        word = word.replace('#', ' ')
        label = tk.Label(self, text=word, font=('Courier', 13))
        label.pack()
        for w in word.split(' '):
            if not w:
                continue
            self.words[w] = label

    def remove_word(self, word):
        label = self.words.pop(word)
        text = label['text'].split(word)
        label['text'] = text[0] + ' ' * len(word) + text[1]
        if label['text'].strip() == '':
            label.pack_forget()
