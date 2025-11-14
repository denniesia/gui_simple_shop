from json import loads, dump
from tkinter import Button, Entry, IntVar, Checkbutton
from shop_page import display_products
from canvas import root, frame, exit_program
from helpers import clean_screen, get_password_hash, get_users_data


def render_entry():
    clean_screen()
    frame.create_text(330, 240, text='Welcome to my Online Shop - Mestie', font=('Bell MT', 14))
    register_btn = Button(
        root,
        text="Register",
        bg="green",  # background color
        fg="white",  # font color
        borderwidth=0,
        width=12,
        height=1,
        command=register,
    )

    login_btn = Button(
        root,
        text="Login",
        bg="blue",
        fg="white",
        borderwidth=0,
        width=12,
        height=1,
        command=login,
    )
    frame.create_window(280, 270, window=register_btn)
    frame.create_window(380, 270, window=login_btn)
    frame.create_window(330, 295, window=exit_btn)

def show_password():
    if checkbox.get():
        password_box.config(show='')
    else:
        password_box.config(show='*')


def login():
    clean_screen()
    font=('Bell MT', 12)

    username_box.delete(0, 'end')
    password_box.delete(0, 'end')

    logging_btn["state"] = "disabled"  # options: active, normal, disabled
    root.bind('<KeyRelease>', check_if_login_is_fulfilled)

    frame.create_text(300, 150, text='Please log in to continue', font=('Bell MT', 14))

    frame.create_text(200, 200, text="Username:", font=font)
    frame.create_text(200, 230, text="Password:", font=font)

    frame.create_window(340, 200, window=username_box)
    frame.create_window(340, 230, window=password_box)

    check_btn = Checkbutton(root, text='Show password?', variable=checkbox,offvalue=False, font=('Bell MT', 10), command=show_password)
    frame.create_window(350, 255, window=check_btn)

    frame.create_window(380, 280, window=logging_btn)
    frame.create_window(225, 280, window=back_btn)

def logging():
    if check_if_login_is_fulfilled:
        if check_logging():
            display_products()
        else:
            frame.create_text(340, 310, text="Invalid username or password!", fill="red")


def check_logging():
    info_data = get_users_data()

    user_username = username_box.get()
    user_password = get_password_hash(password_box.get())

    for i in range(len(info_data)):
        username = info_data[i]["Username"]
        password = info_data[i]["Password"]

        if username == user_username and password == user_password:
            return True

    return False


def register():
    clean_screen()

    first_name_box.delete(0, 'end')
    last_name_box.delete(0, 'end')
    username_box.delete(0, 'end')
    password_box.delete(0, 'end')

    registration_btn["state"] = "disabled"
    root.bind('<KeyRelease>', check_if_registration_is_fulfilled)

    frame.create_text(310, 150, text='Please register to continue', font=('Bell MT', 14))

    frame.create_text(250, 180, text="First name:")
    frame.create_text(250, 210, text="Last name:")
    frame.create_text(250, 240, text="Username:")
    frame.create_text(250, 270, text="Password:")

    frame.create_window(380, 180, window=first_name_box)
    frame.create_window(380, 210, window=last_name_box)
    frame.create_window(380, 240, window=username_box)
    frame.create_window(380, 270, window=password_box)


    check_btn = Checkbutton(root, text='Show password?', variable=checkbox,offvalue=False, font=('Bell MT', 10), command=show_password)
    frame.create_window(360, 295, window=check_btn)

    frame.create_window(390, 320, window=registration_btn)
    frame.create_window(250, 320, window=back_btn)


def registration():
    info_dict = {
        "First_name": first_name_box.get(),
        "Last_name": last_name_box.get(),
        "Username": username_box.get(),
        "Password": get_password_hash(password_box.get()),
    }

    if check_registration(info_dict) and check_if_registration_is_fulfilled:
        with open("db/users_information.txt", "a") as users_file:
            dump(info_dict, users_file)
            users_file.write('\n')
            display_products()


def check_registration(info):
    info_data = get_users_data()

    for record in info_data:
        if record["Username"] == info["Username"]:
            frame.create_text(
                330,
                350,
                text="User with this username already exists!",
                fill="red",
                tag="error",
            )
            return False

    frame.delete("error")

    return True


def check_if_login_is_fulfilled(event):
    info = {
        "Username": username_box.get(),
        "Password": password_box.get(),
    }

    for el in info.values():
        if not el.strip():
            logging_btn["state"] = "disabled"
            break
            return False
    else:
        logging_btn["state"] = "normal"
    return True

def check_if_registration_is_fulfilled(event):
    info = {
        'First_name': first_name_box.get(),
        'Last_name': last_name_box.get(),
        "Username": username_box.get(),
        "Password": password_box.get(),
    }

    for el in info.values():
        if not el.strip():
            registration_btn["state"] = "disabled"
            break
            return False
    else:
        registration_btn["state"] = "normal"
    return True


first_name_box = Entry(root, bd=0)
last_name_box = Entry(root, bd=0)
username_box = Entry(root, bd=0)
password_box = Entry(root, bd=0, show='*')
checkbox = IntVar()

logging_btn = Button(
    root,
    text="Login",
    bg="blue",
    fg="white",
    command=logging,
)

registration_btn = Button(
    root,
    text="Register",
    bg="green",
    fg="white",
    command=registration,
)
exit_btn = Button(
    root,
    text="Exit",
    bg="red",
    fg="white",
    borderwidth=0,
    width=12,
    height=1,
    command=exit_program,
)
back_btn = Button(
    root,
    text="Back",
    bg="gray",
    fg="white",
    width=6,
    height=1,
    command=render_entry,
)

