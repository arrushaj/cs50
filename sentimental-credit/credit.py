from cs50 import get_int

number = get_int("Number: ")

length = len(str(number))

total = 0
checksum = 0
for i in range(0, length, 2):
    digit = int(str(number)[i])
    digit = digit * 2
    total = total + digit

for i in range(1, length, 2):
    digit = int(str(number)[i])
    checksum = checksum + total + digit

if checksum % 10 != 0:
    print("INVALID")

if length == 15:
        if str(number)[0] + str(number)(1) == 34 or 37:
            print("AMEX")
