import time
import tkinter as tk

buff = []
keys = []

root = tk.Tk()
m = tk.Label(root, text="hello")
# m.pack()


def key_callback(event):
    keys.append(event.char)
    pressed = event.char
    buff.append(pressed)
    m['text'] = ''.join(buff)


frame = tk.Frame(root, width=300, height=300)
frame2 = tk.Frame(root, width=300, height=300)
frame['bg'] = "red"
frame2['bg'] = "blue"
frame.bind("<Key>", key_callback)
frame.grid(column=0)
frame2.grid(column=1)
frame.focus_set()
root.mainloop()

s = 'the fox jumped over the lazy frog'
print(f"enter the following text\n{s}")


def go():
    start_time = time.time()
    input("START\n")
    end_time = time.time()
    t = end_time - start_time
    print(t)
    print(len(s)/5)
    print((len(s)/5)/(t/60))
    # wpm formula is (letters / 5) / time(in minutes)
