#!/usr/bin/env python3

code = input("No funny business: ")
if any(c in code for c in "qwertyuiopasdfghjklzxcvbnm1234567890"):
    print("Nope")
    exit(1)
else:
    eval(code)