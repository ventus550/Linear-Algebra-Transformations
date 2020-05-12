from tkinter import *
from LIN import *
from Sections import *
from settings import *
import time

class Root(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.attributes('-alpha', 0.0)
        self.title("Linear Algebra Transformations")
        self.window = Window(self,700)
        self.bind('<FocusIn>', self.on_show)
        self.config(bg=c[2])
        self.iconbitmap(r"icon.ico")

    def on_show(self, event):
        self.window.deiconify()
        self.window.focus_set()


class Window(Toplevel):

    def __init__(self, parent, size):
        Toplevel.__init__(self, parent)
        self.overrideredirect(True)  # turns off title bar, geometry
        self.geometry(str(size+300) + 'x' + str(size) + '+400+100')  # set new geometry
        self.config(background=c[1])
        self.protocol("WM_DELETE_WINDOW", self.window_exit)


        def get_pos(event):
            xwin = self.winfo_x()
            ywin = self.winfo_y()
            startx = event.x_root
            starty = event.y_root

            ywin = ywin - starty
            xwin = xwin - startx

            def move_window(event):
                self.geometry(str(size+300) + 'x' + str(size) + '+{0}+{1}'.format(event.x_root + xwin, event.y_root + ywin))
            self.title_bar.bind('<B1-Motion>', move_window)

        self.ctx = Ctx(self, 300, 0, size-10, size-10)
        self.LinSpace = Lin(s[0], s[1])
        self.ctx.drawLin(self.LinSpace, "#363c3d", "bg")
        self.ctx.drawLin(self.LinSpace, c[0], "fg")
        self.animating = False
        self.fresh = True

        self.title_bar = Frame(self, bg=c[1], width=size+300, height=30, bd=2)
        self.title_bar.place(x=0, y=0)
        self.title_bar.bind('<Button-1>', get_pos)
        GenericButton(self.title_bar, 975, 0, "X", 20, self.window_exit, color=c[2])
        GenericButton(self.title_bar, 950, 0, "_", 20, self.window_hide, color=c[2])

        self.title_text = Label(self.title_bar, text="   Linear Algebra Transformations", bg=c[1], fg=c[0])
        self.title_text.place(x=0, y=0)

        self.input_window = GenericWindow(self, 10, 30, 280, 260)
        self.input_window.addLabel(50, 0, "Transformation Matrix", 12)
        self.input_window.addLabel(30, 20, "[   ]", 100)
        self.input_window.addEntry(70, 70, txt="1")
        self.input_window.addEntry(70, 120, txt="0")
        self.input_window.addEntry(140, 70, txt="0")
        self.input_window.addEntry(140, 120, txt="1")

        def animate_callback():
            if self.animating:
                return
            self.fresh = False
            self.LinSpace.transform(Matrix(
                Vector(self.input_window[0],self.input_window[1]),
                Vector(self.input_window[2], self.input_window[3])))
            self.animate(self.LinSpace)

        def reset_callback():
            if self.animating:
                return
            self.fresh = True
            self.ctx.delete("fg")
            self.LinSpace = Lin(s[0], s[1])
            self.ctx.drawLin(self.LinSpace, c[0], "fg")

        self.input_window.addButton(25, 180, "Animate!", 200, animate_callback)
        self.input_window.addButton(25, 210, "Reset", 200, reset_callback)

        def append_callback():
            if self.animating or not self.fresh:
                return
            self.LinSpace.add(self.vconstr.vector)
            self.ctx.delete("fg")
            self.ctx.drawLin(self.LinSpace, c[0], "fg")

        self.vconstr = VectorConstructor(self, 10, 300, 280, 387.5, append_callback)
        self.vconstr.addLabel(50, 0, "Vector Constructor", 12)


    def flipAnimationStatus(self):
        self.animating = not self.animating

    def animate(self, L):
        def frame():
            L.nextFrame()
            self.ctx.delete("fg")
            self.ctx.drawLin(L, c[0], "fg")


        def animation():
            self.flipAnimationStatus()
            for i in range(100):
                self.after(20*i, frame)
            self.after(2000, self.flipAnimationStatus)

        animation()

    def window_hide(self):
        self.master.iconify()
        self.withdraw()
    def window_exit(self):
        self.master.destroy()


root = Root()
root.mainloop()
