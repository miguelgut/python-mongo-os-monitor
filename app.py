## Código principal
# Importação de bibliotecas
import tkinter as tk               
from tkinter import font as tkfont 
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
import sys
from datetime import datetime
from database import Mongo
from plots import Graphs

# Classe do frame principal, que implementa o esquema de todas as telas sobrepostas e controla a navegação
class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Inicialização do menu
        menubar = MenuBar(self)
        self.config(menu=menubar)
        
        # Inicializando o componente de gráficos e da base de dados
        self.database = Mongo()
        self.graphs = Graphs()
        
        # Configurando as fontes para centralizar o tamanho ao longo de todo o código
        self.title_font = tkfont.Font(family='Arial', size=18, weight="bold", slant="italic")
        self.button_font = tkfont.Font(family='Arial', size=16)
        self.datepicker_font = tkfont.Font(family='Arial', size=10)
        self.label_font = tkfont.Font(family='Arial', size=10)
        self.option_font = tkfont.Font(family='Arial', size=12)

        # Container principal, configurações do grid
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # Aqui cada tela é iniciada a partir da classe com o respectivo nome
        self.frames = {}
        for F in (StartPage, IndividualGraph, GroupTable):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
    
    # Mostra o frame de acordo com o nome
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

# Tela inicial do sistema
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Monitoramento de Sistema Operacional", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        tk.Label(self, text="Utilize a barra superior para navegar", font=controller.label_font).pack()
        tk.Label(self, text="Versão 0.1", font=controller.label_font).pack(side="bottom")

# Tela dos gráficos individuais
class IndividualGraph(tk.Frame):

    def __init__(self, parent, controller):
        # Inicializando o frame e colocando os dados de titulo
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.title = tk.Label(self, text="Gráfico individual", font=controller.title_font)
        self.title.grid(column=0, row=0, columnspan=2)
       
       # Dropdown de opções
        options = [
            "",
            "Uso de disco",
            "CPU",
        ]
        
        self.graphLabel = tk.Label(self, text='Selecione uma métrica para visualizar', font=controller.label_font)
        self.graphOptions = tk.StringVar(self)
        self.graphOptions.set(options[0]) # default value
        
        self.optionMenu = tk.OptionMenu(self, self.graphOptions, *options)
        self.optionMenu.config(font=controller.option_font)
        
        # Datepicker e label dos mesmos
        self.startLabel = tk.Label(self, text='Data de início', font=controller.label_font)
        self.endLabel = tk.Label(self, text='Data final', font=controller.label_font)
        self.dateStart = Calendar(self,
                font=controller.datepicker_font, selectmode='day',
                cursor="hand1",
                )
    
        self.dateEnd = Calendar(self,
                font=controller.datepicker_font, selectmode='day',
                cursor="hand1",
                 )

        # Colocando os elementos no grid
        self.graphLabel.grid(column=0, row=1)
        self.optionMenu.grid(column=0, row=2,columnspan=2)
        self.startLabel.grid(column=0, row=3,sticky='E')
        self.endLabel.grid(column=5, row=3, sticky='W')
        self.dateEnd.grid(column=5, row=4, sticky='W')
        self.dateStart.grid(column=0, row=4,  sticky='E')

        # Função que faz a consulta
        def showQuery(*args):
            
            dStart = datetime.combine(self.dateStart.selection_get(), datetime.min.time())
            dEnd = datetime.combine(self.dateEnd.selection_get(), datetime.max.time())

            if self.graphOptions.get() == 'Uso de disco':
                _graphData = self.controller.database.findDiskUsage(dStart,dEnd)

            elif self.graphOptions.get() == 'CPU':
                _graphData = self.controller.database.findCpuUsage(dStart,dEnd)

            self.controller.graphs.generatePlot(_graphData)


        self.queryButton = tk.Button(self, text="Realizar busca",  font=controller.button_font,command=showQuery)
        self.queryButton.grid(column=10, row=10,columnspan=2, pady=10)
        
        for x in range(10):
            tk.Grid.columnconfigure(self, x, weight=1)

        for y in range(10):
            tk.Grid.rowconfigure(self, y, weight=1)

## Página das telas conjuntas
class GroupTable(tk.Frame):
    def __init__(self, parent, controller):
        # Função de busca
        def showQuery(*args):
                
                dStart = datetime.combine(self.dateStart.selection_get(), datetime.min.time())
                dEnd = datetime.combine(self.dateEnd.selection_get(), datetime.max.time())
                # Faz a busca no banco de dados
                _graphData = self.controller.database.findAll(dStart,dEnd)     
                
                # Cria uma nova janela pra tabela
                newWindow = tk.Toplevel(parent) 
                newWindow.title("Resultados") 
                # Cria um canvas 
                self.canvas = tk.Canvas(newWindow)
                self.canvas.grid(row=0, column=0, sticky="news")
                self.vsb = tk.Scrollbar(newWindow, orient="vertical", command=self.canvas.yview)
                self.vsb.grid(row=0, column=1, sticky='ns')
                Table(self.canvas,_graphData)
                self.canvas.configure(yscrollcommand=self.vsb.set,scrollregion=self.canvas.bbox("all"))

        # Inicializando o frame
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.title = tk.Label(self, text="Tabela em conjunto", font=controller.title_font)
        self.title.grid(column=0, row=0, columnspan=2)

        # Configurando os datepickers
        self.startLabel = tk.Label(self, text='Data de início', font=controller.label_font)
        self.endLabel = tk.Label(self, text='Data final', font=controller.label_font)
        self.dateStart = Calendar(self,
                font=controller.datepicker_font, selectmode='day',
                cursor="hand1",
                # year=y, month=m, day=d
                )
    
        self.dateEnd = Calendar(self,
                font=controller.datepicker_font, selectmode='day',
                cursor="hand1",
                 #year=y, month=m, day=d
                 )
        
        # Posiciona os elementos no frame
        self.startLabel.grid(column=0, row=3,sticky='E')
        self.endLabel.grid(column=5, row=3, sticky='W')
        self.dateEnd.grid(column=5, row=4, sticky='W')
        self.dateStart.grid(column=0, row=4,  sticky='E')
        self.queryButton = tk.Button(self, text="Realizar busca",  font=controller.button_font,command=showQuery)
        self.queryButton.grid(column=10, row=10,columnspan=2, pady=10)
        
        for x in range(10):
            tk.Grid.columnconfigure(self, x, weight=1)

        for y in range(10):
            tk.Grid.rowconfigure(self, y, weight=1)

## Classe do menu
class MenuBar(tk.Menu):

    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        _mgraficos = tk.Menu(self, tearoff=False)
        _mgraficos.add_command(label="Individual", command=lambda: parent.show_frame("IndividualGraph"))

        _mtabela =  tk.Menu(self, tearoff=False)
        _mtabela.add_command(label="Conjunto", command=lambda: parent.show_frame("GroupTable"))

        self.add_cascade(label="Gráficos", menu=_mgraficos)
        self.add_cascade(label="Tabela", menu=_mtabela)
        self.add_command(label="Sair", underline=1, command=lambda: sys.exit(0))

## Classe da tabela
class Table: 
    def __init__(self, parent, _list): 
        total_rows = len(_list) 
        total_columns = len(_list[0])

        _fields = ["ID", "CPU", "Data (timestamp)", "Uso de disco"]
        pos = 0
       
        # Cria uma linha de coluna
        for x in range(len(_fields)):
            self.e = tk.Entry(parent, font=('Arial',12)) 
            self.e.grid(row=0, column=pos) 
            self.e.insert(tk.END, _fields[x])
            pos += 1 

        # Percorre todas as linhas e colunas
        for i in range(1, total_rows): 
            for j in range(total_columns):           
                self.e = tk.Entry(parent, font=('Arial',12)) 
                self.e.grid(row=i, column=j) 
                self.e.insert(tk.END, str(_list[i][j]))

# Instancia o projeto e define o tamanho
if __name__ == "__main__":
    app = App()
    app.geometry("850x550+300+300")
    app.mainloop()