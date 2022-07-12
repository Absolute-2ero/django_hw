import os


def build():
    os.system("python generator.py -s 15 -n 50 -lb 0 -rb 114 -r")


if __name__ == "__main__":
    build()
