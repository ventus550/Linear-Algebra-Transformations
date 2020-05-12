from tkinter import *
from LIN import Vector
from math import sin, cos, radians
from settings import *

def sgn(x):
    if x == 0:
        return 1
    return x / abs(x)


class GenericButton(Button):
    def __init__(self, parent, x, y, txt, width, function, color=c[1]):
        Button.__init__(self, parent, text=txt, command=function, background=color,
                                  fg=c[0], bd=0, activebackground=c[0])
        self.place(x=x, y=y, width=width)

class GenericWindow(Frame):

    def __init__(self, parent, x, y, wh, ht):
        Frame.__init__(self, parent, width=wh, height=ht, bd=10,
                       background=c[2],
                       highlightbackground=c[1],
                       highlightcolor=c[0],
                       highlightthickness=1)
        self.place(x=x, y=y)
        self.entries = []
        self.bind('<Button-1>', self.set_focus)


    def addLabel(self, x, y, txt, size):
        l = Label(self, text=txt, fg=c[0], bg=c[2], font=("Helvetica", size))
        l.place(x=x, y=y)

    def addEntry(self, x, y, txt=""):
        v = StringVar()
        self.entries += [Entry(self, textvariable=v, width="3",background=c[1], fg=c[0], bd=0,
                               font=("Helvetica", 16), insertbackground=c[0])]

        self.entries[-1].place(x=x, y=y)
        v.set(txt)

    def addButton(self, x, y, txt, width, function):
        animation_button = GenericButton(self, x, y, txt, width, function)
        animation_button.bind('<Button-1>', self.set_focus)
    def __getitem__(self, i):
        return float(self.entries[i].get())

    def set_focus(self, event):
        self.focus_set()

class VectorConstructor(GenericWindow):
    def __init__(self, parent, x, y, wh, ht, function):
        GenericWindow.__init__(self, parent, x, y, wh, ht)

        self.ctx = VectorFactory(parent, 45, 350, 200, 200)

        def callback(event):
            l = self.slider_length.get()
            a = self.slider_direction.get()
            self.vector = Vector(cos(radians(a)) * l, sin(radians(a)) * l)
            self.ctx.drawVector(self.vector)

        self.slider_direction = Scale(parent, from_=360, to=0, length=200, orient=HORIZONTAL,
                                      bg=c[2], bd=0, fg=c[0], highlightbackground=c[2], troughcolor=c[0],
                                      command=callback)
        self.slider_direction.place(x=45, y=y+ht-117)
        self.slider_direction.set(90)
        self.slider_direction.bind('<Button-1>', self.set_focus)

        self.slider_length = Scale(parent, from_=0, to=100, length=200, orient=HORIZONTAL,
                              bg = c[2], bd=0, fg = c[0], highlightbackground=c[2], troughcolor=c[0],
                              command=callback)
        self.slider_length.place(x=45, y=y + ht - 80)
        self.slider_length.set(50)
        self.slider_length.bind('<Button-1>', self.set_focus)

        self.addButton(25, 337.5, "Append", 200, function)

class VectorFactory(Canvas):

    def __init__(self, parent, x, y, wh, ht):
        Canvas.__init__(self, parent, width=wh, height= ht, bg = c[2], highlightbackground=c[1])
        self.place(x=x, y=y)
        self.update()
        self.side = self.winfo_width()
        self.parent = parent

    def drawVector(self, v):
        mid = self.side / 2
        self.delete("all")
        self.create_line(mid, mid, mid + v[0], mid - v[1], fill = 'red', width=10,arrow=LAST,
                         arrowshape=(16, 20, 6))
        self.create_text(mid, 2*mid - 20, fill="red", font="Times 15 italic bold",
                         text="(" + "{:.1f}".format(v[0]) + ", " + "{:.1f}".format(v[1]) + ")")

class Ctx(Canvas):

    def __init__(self, parent, x, y, wh, ht):
        Canvas.__init__(self, parent, width=wh-25, height=ht-25, bd=10,
                        background=c[2], highlightbackground=c[1])
        self.place(x=x, y=y)
        self.update()
        self.side = self.winfo_width()
        self.parent = parent

    def drawLine(self, M, color, tag):
        mid = self.side / 2
        width = 2
        if M.isvector:
            color = 'red'
            self.create_text(mid + M[1][0], mid - M[1][1] - sgn(M[1][1])*10, fill="red", font="Times 15 italic bold",
                                    text="(" + "{:.1f}".format(M[1][0]) + ", " + "{:.1f}".format(M[1][1]) + ")", tag="fg")
            width = 5

        self.create_line(mid + M[0][0], mid - M[0][1], mid + M[1][0], mid - M[1][1], fill = color, width = width, arrow=LAST, tags=tag)

    def drawLin(self, L, color, tag):
        for M in L:
            self.drawLine(M, color, tag)