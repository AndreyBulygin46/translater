from tkinter import *
from tkinter import messagebox as mb
from googletrans import Translator
import string
import re
import pyperclip as pc
import keyboard as kb
import pystray
from PIL import Image
import threading

# Создаем иконку
image = Image.open("icon.png")  # Подготовьте свою иконку в формате PNG


def show_window():
    win.deiconify()
    win.lift()


def quit_app():
    icon.stop()
    win.destroy()


# Создаем значок в трее
icon = pystray.Icon(
    "name",
    image,
    "Моё приложение",
    menu=pystray.Menu(
        pystray.MenuItem("Показать", show_window), pystray.MenuItem("Выход", quit_app)
    ),
)

translator = Translator()
win = Tk()
win.title("Переводчик")
win.geometry("500x500+2000+300")
win.iconbitmap(default="icon.ico")
win.resizable(False, False)


def translate(text):
    # pattern = re.findall('[a-zA-Zа-яА-Я]', text)
    if variable.get() == "en-ru":
        translated = translator.translate(text, src="en", dest="ru")
    else:
        translated = translator.translate(text, src="ru", dest="en")
    return translated.text


options = ["en-ru", "ru-en"]
variable = StringVar(win)
variable.set(options[0])
option_menu = OptionMenu(win, variable, *options)
option_menu.place(x=400, y=370)

text_input = Text(win, width=60, height=10)
text_input.place(x=10, y=10)

text_output = Text(win, width=60, height=10)
text_output.place(x=10, y=200)

bt_translate = Button(
    win,
    text="Перевести",
    width=25,
    height=2,
    command=lambda: (
        text_output.delete("1.0", END),
        text_output.insert(END, translate(text_input.get("1.0", END))),
    ),
)
bt_translate.place(x=10, y=370)

bt_copy = Button(
    win,
    text="Скопировать",
    width=25,
    height=2,
    command=lambda: pc.copy(text_output.get("1.0", END)),
)
bt_copy.place(x=200, y=370)

lb_1 = Label(win, text="alt+x - вставить из буфера в поле ввода и перевести")
lb_1.place(x=10, y=420)

lb_3 = Label(win, text="alt+3 - скопировать в буфер")
lb_3.place(x=10, y=460)

kb.add_hotkey(
    "alt+x",
    lambda: (
        show_window(),
        text_input.delete("1.0", END),
        text_input.insert(END, pc.paste()),
        text_output.delete("1.0", END),
        text_output.insert(END, translate(text_input.get("1.0", END))),
    ),
)

kb.add_hotkey(
    "alt+3", lambda: text_output.insert(END, translate(text_input.get("1.0", END)))
)
kb.add_hotkey("esc", lambda: (win.withdraw()))

def run_icon():
    icon.run()


threading.Thread(target=run_icon, daemon=True).start()  # <- НОВЫЙ ПОТОК

win.mainloop()
