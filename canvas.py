from tkinter import Tk, Canvas
from tkinter import Menu
from json import dump


def create_root():
    root = Tk()
    root.title('GUI Shop')
    root.geometry('700x600')
    root.resizable(False, False)

    return root

def create_frame():
    frame = Canvas(root, width=700, height=700)
    frame.grid(row=0, column=0)  #attaching the frame to the app window

    return frame

def exit_program():
    root.quit()


def create_menu():
    menu = Menu(root)
    file_menu = Menu(menu, tearoff=0, font=('Times New Roman', 10))
    file_menu.add_command(label="Exit", command=exit_program)
    menu.add_cascade(label="Menu", menu=file_menu)

    root.config(menu=menu)


root = create_root()
menu = create_menu()
frame = create_frame()

