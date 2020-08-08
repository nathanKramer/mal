import traceback
import sys
import reader
import printer


def EVAL(str):
    return str


def read_evaluate_print(str):
    return printer.pr_str(
        EVAL(
            reader.read_str(str)
        )
    )


def main():
    while True:
        try:
            user_input = input("user> ")
            print(read_evaluate_print(user_input))
        except reader.MalReaderError:
            print("".join(traceback.format_exception(*sys.exc_info())))
        except EOFError:
            print("EOF Received, exiting.")
            exit()


if __name__ == "__main__":
    main()
