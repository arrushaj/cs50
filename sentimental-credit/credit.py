from cs50 import get_int

number = get_int("Number: ")

length = len(str(number))

for i in range(length):
    j = 1
    digit = number % (10^j)
    double = digit * 2
    total = total + double
    j = j + 2
    i = i + 2

for k in range(length):
    j = 2
    digit = number % (10^j)
    checksum = checksum + total + digit
    j = j + 2
    i = i + 2

print(checksum)