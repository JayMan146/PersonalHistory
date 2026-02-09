import tkinter

primary_window: tkinter.Tk = tkinter.Tk(className=" Journal System") # why is there a space? well because the first character is forced to be lowercase, of course.

def main():
    primary_window.mainloop()

if __name__ == "__main__":
    main()