import string


def reading_level(text):
    words = 1
    letters = 0
    sentences = 0
    length = len(text)
    for i in range(0, length, 1):
        if text[i].isspace():
            words += 1
        elif text[i] in string.punctuation:
            if (text[i] in ['.', '?', '!']):
                sentences += 1
        elif text[i].isalpha():
            letters += 1
    L = (100.0 / words * letters)
    S = (100.0 / words * sentences)
    level = 0.0588 * L - 0.296 * S - 15.8
    if (level > 16.0):
        print("Grade 16+")
    elif (level < 1.0):
        print("Before Grade 1")
    else:
        print(f"Grade {round(level)}")


text = input("Text: ")
reading_level(text)
