from tkinter import Tk

from field import Field


def main():
    root = Tk()
    root.geometry('1000x800')
    test_map = Field()
    test_map.load('input.txt')
    test_map.draw()
    root.mainloop()
    test_map.save('output.txt')


if __name__ == '__main__':
    main()
