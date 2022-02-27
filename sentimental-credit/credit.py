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

elif length == 13 or length == 16:
    if str(number)[0] == str(4):
        print("VISA")

elif length == 16:
    print(str(number)[0] + str(number)[1])
    if str(number)[0] + str(number)[1] == str(51) or str(52) or str(53) or str(54) or str(55):
        print("MASTERCARD")


