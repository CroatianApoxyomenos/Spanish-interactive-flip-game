from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}


# ---------------------------- FUNCTIONS ---------------------------- #
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(new_data)
    canvas.itemconfig(title, text="Spanish", fill="black")
    canvas.itemconfig(guess_word, text=current_card["Spanish"], fill="black")
    canvas.itemconfig(bg_image, image=card_front)
    flip_timer = window.after(3000, card_flip)


def card_flip():
    global current_card
    canvas.itemconfig(bg_image, image=card_back)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(guess_word, text=current_card["English"], fill="white")


def remove_card():
    global current_card
    new_data.remove(current_card)
    next_card()
    to_learn_dict = pandas.DataFrame(new_data)
    to_learn_dict.to_csv("./data/to_learn_spanish.csv", index=False)


# ---------------------------- GUI ---------------------------- #
window = Tk()
window.title("My flash card game")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, card_flip)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
bg_image = canvas.create_image(402, 263, image=card_front)

wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=remove_card)
right_button.grid(column=1, row=1)

title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
guess_word = canvas.create_text(400, 313, text="word", font=("Ariel", 50, "bold"))

# ---------------------------- DATAFRAMES ---------------------------- #
try:
    data = pandas.read_csv("data/to_learn_spanish.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/spanish_words.csv")
finally:
    new_data = data.to_dict(orient="records")
    print(len(data))

next_card()
window.mainloop()

