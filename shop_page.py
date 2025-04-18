from PIL import Image, ImageTk
from helpers import clean_screen
from json import load, dump, loads # load - from json into string
import json
from canvas import frame, root
from tkinter import Button, Label, Scrollbar

def display_products():
    clean_screen()
    display_stock()
    calculate_total(ordered_products)
    frame.create_text(345, 16, text ="Today's Picks", font=('Arial Rounded MT', 14))




def display_stock():
    with open('db/products.json', 'r') as stock:
        info = load(stock)

    x,y = 150, 50

    for item_name, item_info in info.items():
        img = Image.open(item_info['image'])
        resized_img = img.resize((120, 120))
        item_image = ImageTk.PhotoImage(resized_img)
        price = item_info['price']

        images.append(item_image) #keeping the reference to the image so that tkinter does not delete it after the function ends
        frame.create_text(x, y, text=item_name, font=('Arial', 13), fill='black')
        frame.create_text(x,y + 20, text=f'Price:{price} €', font=('Arial', 10), fill='black')
        frame.create_image(x, y+100, image=item_image)

        if item_info['quantity'] > 0:
            color = 'green'
            text = f'In stock: {item_info["quantity"]}'

            item_button = Button(
                root,
                text='Buy',
                bg='green',
                fg='white',
                font=('Comic Sans MS', 8),
                width=5,
                command= lambda x=item_name, y=info : buy_product(x, y)
            #command= lambda: buy_product(item_name, info) this is not correct -> because it would reduce the quantity of the last product that was worked with
            # because of the loop the last product's info would be saved, so when we click the 'buy' button we would reduce its quantity
            )

            frame.create_window(x,y + 210, window=item_button)
        else:
            color = 'red'
            text = f'Out of stock.'

        frame.create_text(x, y + 180, text=text, fill=color)

        x += 200

        if x >= 650:
            y+= 270
            x=150

def paid_order():
    clean_screen()
    if total_amount > 0:
        frame.create_text(350, 200, text='Thank you for your oder!', font=('Book Antiqua',25), fill='black')

def reduce_quantity(product_name, ordered_products):
    ordered_products[product_name]['quantity'] -= 1
    if ordered_products[product_name]['quantity'] == 0:
        del ordered_products[product_name]

    display_checkout(ordered_products)

def display_checkout(ordered_products):
    clean_screen()

    frame.create_text(120, 30, text='Review Your Order', font=('Book Antiqua', 14), fill='black')

    if not ordered_products:
        frame.create_text(140, 70, text= 'Your shopping cart is empty', font=('Book Antiqua', 12), fill='black')

        back_link = Label(root, text="Go back to SHOP", fg="black", cursor="hand2",
                          font=("Book Antiqua", 12, "underline"))
        frame.create_window(100, 270, window=back_link)
        back_link.bind("<Button-1>", lambda e: display_products())

    else:

        x,y = 160, 70
        for product, product_info in ordered_products.items():
            frame.create_text(x, y, text=f'{product}    Price: {product_info["price"]} €    Quantity: {product_info["quantity"]}', font=('Book Antiqua', 12), fill='black')

            reduce_btn = Button(root, text="Reduce quantity", fg="black", cursor="hand2",
                                command=lambda p=product: reduce_quantity(p, ordered_products))
            frame.create_window(x+250, y, window=reduce_btn)
            y += 40

        frame.create_text(x+220, y, text=f"Your Total: {total_amount} €", font=('Book Antiqua', 12), fill='black')
        back_link = Label(root, text="Shop More", fg="black", cursor="hand2",
                          font=("Book Antiqua", 12, "underline"))
        frame.create_window(90, y + 40, window=back_link)
        back_link.bind("<Button-1>", lambda e: display_products())

        pay_button = Button(root, text="Pay", fg="black",bg='green', width=10, cursor="hand2",command=paid_order)
        frame.create_window(x+270, y+40, window=pay_button)




def calculate_total(ordered_products):
    global total_amount
    total_amount = 0

    for product_info in ordered_products.values():
        total_amount += product_info["price"] * product_info["quantity"]


    total_link = Label(root, text=f"Total amount: {total_amount:.2f}€", fg="black", cursor="hand2",
                       font=("Arial Rounded MT", 12, "underline"))
    frame.create_window(100, 570, window=total_link)
    total_link.bind("<Button-1>", lambda e: display_checkout(ordered_products))
    pay_button = Button(root, text="Pay", fg="white", bg='orange', width=10, cursor="hand2", command=paid_order)
    frame.create_window(570, 565, window=pay_button)

def buy_product(product_name, info):
    price = info[product_name]["price"]
    quantity = 1
    info[product_name]["quantity"] -= 1

    if product_name not in ordered_products:
        ordered_products[product_name] = {"price": price, "quantity": quantity}
    else:
        ordered_products[product_name]["price"] = price
        ordered_products[product_name]["quantity"] += quantity


    with open('db/products.json', 'w') as stock:
        dump(info, stock, indent=4)

    clean_screen()
    display_stock()
    calculate_total(ordered_products)


images = []
ordered_products = {}
total_amount = 0
