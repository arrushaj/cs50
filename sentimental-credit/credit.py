from cs50 import get_int

number = get_int("Number: ")

length = len(str(number))

total = 0
checksum = 0
j = 1
for i in range(length):
    place = 10^j
    digit = number % (place)
    print(digit)
    double = digit * 2
    total = total + double
    j += 2
    i += 2

j = 2
for k in range(length):
    digit = number % (10^j)
    checksum = checksum + total + digit
    j = j + 2
    k = k + 2

print(checksum)