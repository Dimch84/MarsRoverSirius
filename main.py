from tkinter import Tk

from map import Map


def main():
    root = Tk()
    test_map = Map()
    test_map.draw()
    root.mainloop()


if __name__ == '__main__':
    main()
