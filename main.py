from tkinter import Tk

from field import Field
from ui import UI


def main():
    root = Tk()
    root.geometry("{0}x{1}+0+0".format(
        root.winfo_screenwidth(), root.winfo_screenheight()))
    # root.wm_attributes('-fullscreen', 1)
    test_map = Field()
    UI(root, test_map)
    root.mainloop()


if __name__ == '__main__':
    main()
