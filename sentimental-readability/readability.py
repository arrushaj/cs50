from cs50 import get_string

text = get_string("Text: ")

words = 0
sentences = 0
letters = 0

lower = text.lower

for i in range(len(text)):
    if ord(lower[i]) > ord('a') and ord(lower[i]) < ord('z'):
        letters += 1
    elif lower[i] == " ":
        words += 1
    elif lower[i] == "?" or "." or "!":
        sentences += 1



