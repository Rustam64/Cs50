import re


def validate_input():
    user_input = input("Number: ")
    length = len(user_input)
    if not re.fullmatch(r"\d{13,16}", user_input):
        print("INVALID")
        return
    total_sum = 0
    double = False
    for i in range(length - 1, -1, -1):  # Start from the last digit
        digit = int(user_input[i])
        if double:
            digit *= 2
            if digit > 9:
                digit -= 9
        total_sum += digit
        double = not double

    # Checksum Validation
    if total_sum % 10 != 0:
        print("INVALID")
        return
    if length == 15 and (user_input.startswith("34") or user_input.startswith("37")):
        print("AMEX")
    elif (length == 16 or length == 13) and user_input.startswith("4"):
        print("VISA")
    elif length == 16 and (51 <= int(user_input[:2]) <= 55):
        print("MASTERCARD")
    else:
        print("INVALID")


validate_input()
