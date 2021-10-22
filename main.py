from tkinter import *
from tkinter.ttk import *
import random

wpm = 0
count = 60
random_words = []
first_word = ""
first_word_length = 0


def timer():
    global count

    wpm_entry.configure(state="normal")

    # Redraw counter
    time_entry.delete(0, "end")
    time_entry.insert(0, count)

    # Check timeout
    if count == 0:
        # Redraw wpm
        wpm_entry.delete(0, "end")
        wpm_entry.insert(0, wpm)
    else:
        # Register new timer
        count = count - 1
        window.after(1000, timer)

    wpm_entry.configure(state="disabled")


def draw_words():
    global first_word
    global first_word_length

    words_text.configure(state="normal")

    # Redraw all words
    words_text.delete("1.0", "end")
    for word in random_words:
        words_text.insert(CURRENT, word + "\n")

    # Remove all tags
    for tag in words_text.tag_names():
        words_text.tag_delete(tag)

    first_word = random_words[0]
    first_word_length = len(first_word)

    # Highlight the first word
    words_text.tag_add("here", "1.0", "1." + str(first_word_length))
    words_text.tag_config("here", background="yellow", foreground="black")

    # Make tags for character coloring
    for i in range(first_word_length):
        words_text.tag_add(str(i), "1." + str(i), "1." + str(i + 1))

    words_text.configure(state="disabled")


def start():
    global wpm
    global count
    global random_words

    # Initialize variables
    wpm = 0
    count = 60
    random_words = []

    # Make list with 100 random words
    for _ in range(100):
        random_word = random.choice(all_words)
        random_words.append(random_word)

    draw_words()

    word_entry.delete(0, "end")
    word_entry.focus()

    # Start timer
    timer()


def click_enter(key):
    global wpm

    typed = word_entry.get()
    word = random_words.pop(0)

    draw_words()
    word_entry.delete(0, "end")

    if typed == word:
        wpm = wpm + 1


def validate(d, s, P, S):
    # print(f"d={d}, s={s}, P={P}, S={S}")

    words_text.configure(state="normal")

    # Backspace
    if d == "0":
        char_pos = len(P)
        words_text.tag_config(str(char_pos), background="yellow", foreground="black")
        return True
    else:
        if S.isalpha():
            if len(P) > first_word_length:
                return False

            char_pos = len(s)
            if first_word[char_pos] == S:
                words_text.tag_config(str(char_pos), background="yellow", foreground="green")
            else:
                words_text.tag_config(str(char_pos), background="yellow", foreground="red")
            return True

    words_text.configure(state="disabled")
    return False


with open("engmix.txt", "r", encoding="utf-8", errors="ignore") as file:
    lines = file.readlines()
    all_words = [line.rstrip() for line in lines]

window = Tk()
window.title("Typing Speed")
window.minsize(width=400, height=260)
window.config(padx=20, pady=10)

wpm_label = Label(text="WPM: ")
wpm_label.grid(row=0, column=0, pady=5)
wpm_entry = Entry(width=10)
wpm_entry.grid(row=0, column=1, pady=5)

time_label = Label(text="Time left: ")
time_label.grid(row=0, column=2, padx=(10, 0), pady=5)
time_entry = Entry(width=10)
time_entry.grid(row=0, column=3, pady=5)

start_button = Button(text="Start", command=start, width=10)
start_button.grid(row=0, column=4, padx=(20, 0), pady=5)

words_text = Text(window, width=24, height=5, font=("Abadi", 20, "bold"), wrap=WORD)
words_text.configure(state="disabled")
words_text.grid(row=1, column=0, columnspan=5, sticky="W")

validate_command = (window.register(validate), '%d', '%s', '%P', '%S')
word_entry = Entry(window, width=24, font=("Abadi", 20, "bold"), justify="center",
                   validate="key", validatecommand=validate_command)
word_entry.grid(row=2, column=0, columnspan=5, sticky="W")
word_entry.bind('<Return>', click_enter)

window.mainloop()
