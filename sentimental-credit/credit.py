from cs50 import get_int

number = get_int("Number: ")

length = len(str(number))

total = 0
checksum = 0
for i in range(1, length, 2):
    digit = int(str(number)[length-i-1])
    digit = digit * 2
    if digit > 9:
        digit = int(str(digit)[0]) + int(str(digit)[1])
    total = total + digit

checksum = checksum + total
for i in range(0, length, 2):
    digit = int(str(number)[length-i-1])
    checksum = checksum + digit

length_checksum = len(str(checksum))
if str(checksum)[length_checksum-1] != str(0):
    print("INVALID")

if length == 15:
        if str(number)[0] + str(number)[1] == str(34) or str(37):
            print("AMEX")
