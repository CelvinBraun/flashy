from pandas import *
from tkinter import *
import random
import csv

BACKGROUND_COLOR = "#B1DDC6"
FILE_PATH = "data/french_words.csv"
LANG1 = "French"
LANG2 = "English"

# check if words_to_learn.csv is existing from last learn session.
try:
    data = read_csv("data/words_to_learn.csv")
    TO_LEARN = data.to_dict(orient="records")
except:
    data = read_csv(FILE_PATH)
    TO_LEARN = data.to_dict(orient="records")

CURRENT_CARD = {}
WORDS_TO_LEARN = []

def did_know():
    global TO_LEARN, CURRENT_CARD, flip_timer
    TO_LEARN.remove(CURRENT_CARD)

    # if no words in list existing, end learn session
    if len(TO_LEARN)==0:
        window.after_cancel(flip_timer)
        card.itemconfig(card_title, text="Congrats!", fill="blue")
        card.itemconfig(card_word, text="You covered for now all vocabs!", fill="blue", font=("Ariel", 30, "bold"))
    else:
        next_card()

# when user don´t know card -> card gets added to learn list.
def did_not_know():
    global CURRENT_CARD, WORDS_TO_LEARN
    WORDS_TO_LEARN.append(CURRENT_CARD)

    # WORDS_TO_LEARN to WORDS_TO_LEARN.csv
    keys = WORDS_TO_LEARN[0].keys()
    with open("data/words_to_learn.csv", "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(WORDS_TO_LEARN)

    next_card()

def next_card():
    global CURRENT_CARD, flip_timer
    window.after_cancel(flip_timer)
    card.itemconfig(card_side, image=CARD_FRONT)
    CURRENT_CARD = TO_LEARN[random.randint(0, len(TO_LEARN) - 1)]
    card.itemconfig(card_title, text=LANG1, fill="black")
    card.itemconfig(card_word, text=CURRENT_CARD[LANG1], fill="black")
    flip_timer= window.after(3000, flip_card)

def flip_card():
    global CURRENT_CARD
    card.itemconfig(card_side, image=CARD_BACK)
    card.itemconfig(card_title, text=LANG2, fill="white")
    card.itemconfig(card_word, text=CURRENT_CARD[LANG2], fill="white")

window = Tk()
window.title("Flashy")
window.config(padx=10, pady=10, background=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)
CARD_FRONT = PhotoImage(file="images/card_front.png")
CARD_BACK = PhotoImage(file="images/card_back.png")

# canvas
card = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_side = card.create_image(400, 263, image = CARD_FRONT)
card.grid(row=0, column=0, columnspan=2)
card_title = card.create_text(400, 150, text="Language", font=("Ariel", 40, "italic"))
card_word = card.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))

# buttons
wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, command=did_not_know)
wrong_button.config(bg=BACKGROUND_COLOR)
wrong_button.grid(row=1, column=0)
right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, command=did_know)
right_button.config(bg=BACKGROUND_COLOR)
right_button.grid(row=1, column=1)

next_card()

window.mainloop()