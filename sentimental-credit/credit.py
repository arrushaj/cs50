from cs50 import get_int

number = get_int("Number: ")

for i in range(len(number)):
    j = 1
    digit = number % (10^j)
    double = digit * 2
    total = total + double
    j = j + 2
    i = i + 2

for 