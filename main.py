from tkinter import Tk

from field import Field
from ui import UI


def main():
    root = Tk()
    root.geometry("{0}x{1}+0+0".format(
        root.winfo_screenwidth(), root.winfo_screenheight()))
    # root.wm_attributes('-fullscreen', 1)
    # ui = UI()
    test_map = Field()
    test_map.load('input.txt')
    # test_map.generate_random()
    root.mainloop()
    test_map.save('output.txt')


if __name__ == '__main__':
    main()
