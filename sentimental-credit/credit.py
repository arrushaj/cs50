from cs50 import get_int

number = get_int("Number: ")

length = len(str(number))

total = 0
checksum = 0
for i in range(0, length, 2):
    digit = int(str(number)[i])
    print(digit)
    digit = digit * 2
    total = total + digit

print(total)

break

for i in range(1, length, 2):
    digit = int(str(number)[i])
    checksum = checksum + total + digit

print(checksum)

length_checksum = len(str(checksum))
if str(checksum)[length_checksum-1] != 0:
    print("INVALID")

if length == 15:
        if str(number)[0] + str(number)[1] == str(34) or str(37):
            print("AMEX")
