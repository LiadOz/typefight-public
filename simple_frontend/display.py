import tkinter as tk
import tkinter.font as tk_font
from user import User, WordType, UserManager
import re
import sys
sys.path.append('../backend')

from generate import get_attack, get_defend, get_rival


# notice that there is a method here called get_current_user
# this is diffrent to self.user_manager.current_user one is for the gui
# the latter for handling user data
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.current_user = 0
        self._create_windows()
        self._set_defaults()
        self._sample_game()
        self._render_game()

    def _sample_game(self):
        self.user_manager = UserManager(User(), User())
        um = self.user_manager
        um.user_1.update_words(WordType.ATTACK, list(get_attack()))
        um.user_1.update_words(WordType.DEFEND, list(get_defend()))
        um.user_1.update_words(WordType.RIVAL, list(get_rival()))
        um.switch_user()
        um.user_2.update_words(WordType.ATTACK, list(get_attack()))
        um.user_2.update_words(WordType.DEFEND, list(get_defend()))
        um.user_2.update_words(WordType.RIVAL, list(get_rival()))
        um.switch_user()

    def _set_defaults(self):
        self.master.title('Typefight')
        self.master.geometry('1000x800')
        self.bind("<Key>", self._key_callback)
        self.bind("<BackSpace>", self._back)
        self.bind("<space>", self._space)
        self.bind("<Return>", self._switch_user)
        self.bind("<Tab>", self._switch_typing_mode)
        self.focus_set()
        self.pack()

    # this method is for convience for switching between users
    # a user should not have this ability
    def _switch_user(self, event=None):
        if self.current_user:
            self.current_user = 0
        else:
            self.current_user = 1
        self.user_manager.switch_user()
        self._render_game()
        self._tag_frames()

    def _switch_typing_mode(self, event):
        self.user_manager.toggle_mode()

    # this is used primarily because of the need to change users
    def _render_game(self):
        current = self._get_current_user()
        other = self._get_rival_user()
        current.clear_frame()
        other.clear_frame()
        for x in self.user_manager.get_words(WordType.ATTACK).queue:
            current.add_attack_word(x)
        for x in self.user_manager.get_words(WordType.DEFEND).queue:
            current.add_defense_word(x)
        for x in self.user_manager.get_words(WordType.RIVAL).queue:
            other.add_defense_word(x)

    def _get_current_user(self):
        if self.current_user:
            return self.first_user
        return self.second_user

    def _get_rival_user(self):
        if self.current_user:
            return self.second_user
        return self.first_user

    def _tag_frames(self):
        if self.current_user:
            self.first_user['text'] = 'User'
            self.second_user['text'] = 'Rival'
        else:
            self.first_user['text'] = 'Rival'
            self.second_user['text'] = 'User'

    def _create_windows(self):
        left_pane = tk.Frame(self, width=500, height=800)
        right_pane = tk.Frame(self, width=500, height=800)
        left_pane.grid(row=0, column=0)
        right_pane.grid(row=0, column=1)
        self.first_user = UserFrame(left_pane)
        self.second_user = UserFrame(right_pane)
        self._tag_frames()

    def _update_current_word(self):
        self._get_current_user().set_message(
            self.user_manager.get_current_word())

    def _back(self, event):
        self.user_manager.remove_previous()
        self._update_current_word()

    def _key_callback(self, event):
        if re.match("\\w", event.char):
            self.user_manager.type_key(event.char)
            self._update_current_word()

    def _space(self, event):
        if self.user_manager.publish_word():
            self._render_game()
            self._get_current_user().set_message('')
        self._update_current_word()


# currently the entire frame is rendered after every published word
class UserFrame(tk.LabelFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self._set_defaults()
        self.font = tk_font.Font(family="Lucida Grande", size=26)
        self.input_message = tk.Label(self, font=self.font)
        self.input_message.pack()
        self.defense = []
        self.attack = []
        self.rival = []

    def set_message(self, message):
        self.input_message['text'] = message

    def add_defense_word(self, word):
        label = tk.Label(self, text=word)
        label.grid(column=1)
        self.defense.append(label)

    def add_attack_word(self, word):
        label = tk.Label(self, text=word)
        label.grid(column=2)
        self.attack.append(label)

    def add_rival_word(self, word):
        label = tk.Label(self, text=word)
        label.grid(column=1)
        self.rival.append(label)

    def clear_frame(self):
        self.set_message('')
        for w in self.defense + self.attack + self.rival:
            w.grid_forget()
        self.defense = []
        self.attack = []
        self.rival = []

    def _set_defaults(self):
        self['width'] = 450
        self['height'] = 700
        self.place(relx=.5, rely=.5, anchor="center")
        self.pack_propagate(False)
        self.grid_propagate(False)

    def _create_windows(self):
        pass


root = tk.Tk()
app = Application(root)
app.mainloop()
