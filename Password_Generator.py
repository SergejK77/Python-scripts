import string
import secrets

DIGITS = string.digits
LOWERS = string.ascii_lowercase
UPPERS = string.ascii_uppercase
PUNC = string.punctuation
ALL_CHARS = DIGITS + LOWERS + UPPERS + PUNC
USE_INPUT = False


def create_PW(length=32):
    if int(length) < 4:
        raise ValueError("Password length must be at least 4 characters")
    password = [
        secrets.choice(DIGITS),
        secrets.choice(LOWERS),
        secrets.choice(UPPERS),
        secrets.choice(PUNC)
    ]

    password += [secrets.choice(ALL_CHARS) for _ in range(int(length) - 4)]

    secrets.SystemRandom().shuffle(password)
    return "".join(password)


if __name__ == "__main__":
    if USE_INPUT:
        print("Para is optional. Press Enter to continue")
        min_length = input("Please give the min. password length: ")
        if min_length.isdigit() and int(min_length) >= 4:
            pw = create_PW(int(min_length))
    else:
        pw = create_PW()
    print(pw)
