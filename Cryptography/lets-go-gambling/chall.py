#!/usr/bin/env python3

import random
import os

random.seed(os.urandom(32))
sym = ["7", "Cherry", "Gold", "Bar", "FLAG", "Lemon", "Money", "Bell", "Clover", "Watermelon"]
flagindex = 4
def pprint(symbols):
    emptysymbols = [" " * len(s) for s in symbols]
    print("-"*(6 + 10 + sum(len(s) for s in symbols)))
    # print("| ", end="")
    # for s in symbols:
    #     print(" "*len(s) + " | ", end="")
    print("| " + " | ".join(emptysymbols) + " |")
    print("| " + " | ".join(symbols) + " |")
    print("| " + " | ".join(emptysymbols) + " |")
    # print("| ", end="")
    # for s in symbols:
    #     print(" "*len(s) + " | ", end="")
    print(""+"-"*(6 + 10 + sum(len(s) for s in symbols)))

def gamble(amount=1):
    result = random.getrandbits(32)
    for _ in range(amount):
        symbols = []
        for i in range(5):
            symbols.append(sym[result % len(sym)])
            result //= len(sym)
        pprint(symbols)
        # good luck reaching this lmao
        if all(s == symbols[flagindex] for s in symbols):
            print("WOWWWOWOWOWOWOWOW!")
            print(open("flag.txt", "r").read()[:flagindex])
        elif len(set(symbols)) == 1:
            print("So Lucky!")
        else:
            print("Aww Dammit!")

def predict():
    print("Predict 10 times and win a prize!")
    for _ in range(10):
        result = random.getrandbits(32)
        prediction = input("Enter your prediction: ").split()
        symbols = []
        for i in range(5):
            symbols.append(sym[result % len(sym)])
            result //= len(sym)
        pprint(symbols)
        if symbols == prediction:
            print("AMAZING!")
        else:
            print("Aww Dammit!")
            return
    print(open("flag.txt", "r").read()[flagindex:])

attempt = 0
consent = "n"
while attempt < 1337:
    print("1. Gamble")
    print("2. Predict")
    print("3. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        if attempt < 10:
            gamble()
            attempt += 1
        elif attempt % 10 == 0 and consent != "y":
            print("Tired of clicking the button? Try out our state-of-the-art double spin! Spin twice with a single click!")
            consent = input("Do you want to try it? (y/n): ")
            if consent == "y":
                gamble(2)
                attempt += 2
            else:
                print("Okay, maybe next time!")
                gamble()
                attempt += 1
        else:
            if consent == "y":
                gamble(2)
                attempt += 2
            else:
                gamble()
                attempt += 1
    elif choice == "2":
        predict()
        # just once please
        attempt += 1337
    elif choice == "3":
        break
    else:
        print("Invalid choice, please try again.")