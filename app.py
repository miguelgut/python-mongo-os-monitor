import tkinter as tk               
from tkinter import font as tkfont 
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
import sys
from datetime import datetime

global t
class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        _mgraficos = tk.Menu(self, tearoff=False)
        _mgraficos.add_command(label="Individual", command=lambda: parent.show_frame("PageOne"))
        _mgraficos.add_command(label="Conjunto", command=lambda: parent.show_frame("PageTwo"))

        _mtabela =  tk.Menu(self, tearoff=False)
        _mtabela.add_command(label="Individual", command=lambda: parent.show_frame("PageOne"))
        _mtabela.add_command(label="Conjunto", command=lambda: parent.show_frame("PageTwo"))

        _marquivo =  tk.Menu(self, tearoff=False)
        _marquivo.add_command(label="Individual", command=lambda: parent.show_frame("PageOne"))
        _marquivo.add_command(label="Conjunto", command=lambda: parent.show_frame("PageTwo"))

        self.add_cascade(label="Gráficos", menu=_mgraficos)
        self.add_cascade(label="Tabela", menu=_mtabela)
        self.add_cascade(label="Arquivo", menu=_marquivo)
        self.add_command(label="Sair", underline=1, command=lambda: sys.exit(0))

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        menubar = MenuBar(self)
        self.config(menu=menubar)
        self.title_font = tkfont.Font(family='Arial', size=18, weight="bold", slant="italic")
        self.button_font = tkfont.Font(family='Arial', size=16)
        self.datepicker_font = tkfont.Font(family='Arial', size=10)
        self.option_font = tkfont.Font(family='Arial', size=12)
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        n = datetime.now()
        t = n.timetuple()
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Monitoramento de Sistema Operacional", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        button2.pack()


class PageOne(tk.Frame):    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.title = tk.Label(self, text="Gráfico individual", font=controller.title_font)
        self.title.grid(column=0, row=0, columnspan=2)
        options = [
            "",
            "Uso de bateria",
            "CPU",
            "Bateria restante"
        ] #etc

        self.graphOptions = tk.StringVar(self)
        self.graphOptions.set(options[0]) # default value
        
        self.optionMenu = tk.OptionMenu(self, self.graphOptions, *options)
        self.optionMenu.config(font=controller.option_font)
        self.optionMenu.grid(column=0, row=1,columnspan=2)

        self.dateStart = Calendar(self,
                font=controller.datepicker_font, selectmode='day',
                cursor="hand1",
                # year=y, month=m, day=d
                )
    
        self.dateStart.grid(column=0, row=2,  sticky='E')

        self.dateEnd = Calendar(self,
                font=controller.datepicker_font, selectmode='day',
                cursor="hand1",
                 #year=y, month=m, day=d
                 )
        self.dateEnd.grid(column=2, row=2, sticky='W')

        def showQuery(*args):
            tk.messagebox.showinfo(title=None, message="The selected item is {}".format(self.graphOptions.get()))

        self.queryButton = tk.Button(self, text="Realizar busca",  font=controller.button_font,command=showQuery)
        self.queryButton.grid(column=0, row=10,columnspan=2, pady=10)
        
        for x in range(10):
            tk.Grid.columnconfigure(self, x, weight=1)

        for y in range(10):
            tk.Grid.rowconfigure(self, y, weight=1)

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = App()
    app.geometry("850x550+300+300")
    app.mainloop()