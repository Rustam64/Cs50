def main():
    while True:
        height = input("Height: ")
        if (height.isnumeric() and int(height) > 0 and int(height) < 9):
            break
    height = int(height)
    ends = "\n"
    for x in range(1, height + 1, 1):
        indent(height-x)
        block(x, "")
        print("  ", end="")
        block(x, ends)
        x += 1


def block(x, ends):
    print("#"*x, end=ends)


def indent(x):
    print(" "*x, end="")


main()
