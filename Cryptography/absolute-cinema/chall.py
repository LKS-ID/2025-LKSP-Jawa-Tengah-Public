#!/usr/bin/env python3

from gmpy2 import iroot
print("I'll judge your number")
try:
    num = int(input("Enter a number: "))
except:
    print("That's not a number")
    exit(1)

creativity = round(min(5, num/20000), 1)
balance = min(abs(len(set(str(num))) - 10), len(set(str(num))))
harmony = max(0, 5 - (num - int(iroot(num, 2)[0])**2))

print(f"creativity: {creativity}/5")
print(f"balance: {balance}/5")
print(f"harmony: {harmony}/5")

if creativity == 5 and balance == 5 and harmony == 5:
    print("ABSOLUTE CINEMA")
    print(open("flag.txt", "r").read())

else:
    print("Not absolute cinema :(")