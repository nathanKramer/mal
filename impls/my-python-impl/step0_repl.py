def mal_read(str):
    return str


def mal_eval(str):
    return str


def mal_print(str):
    return str


def read_evaluate_print(str):
    val = mal_read(str)
    val = mal_eval(val)
    val = mal_print(val)
    return val


def main():
    while True:
        try:
            user_input = input("user> ")
            print(read_evaluate_print(user_input))
        except EOFError:
            print("EOF Received, exiting.")
            exit()


if __name__ == "__main__":
    main()
