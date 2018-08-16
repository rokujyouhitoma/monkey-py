import getpass
from repl import Start

def main():
    user = getpass.getuser()
    print("Hello {}! This is the Monkey programming language!\n".format(user), end='')
    print("Feel free to type in commands\n", end='')
    Start()


if __name__ == '__main__':
    main()
