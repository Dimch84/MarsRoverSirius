from tkinter import Tk

from map import Map


def main():
    root = Tk()
    root.geometry('1000x800')
    test_map = Map()
    test_map.load('input.txt')
    test_map.draw()
    root.mainloop()
    test_map.save('output.txt')


if __name__ == '__main__':
    main()
