from msilib.schema import Icon
from operator import itemgetter
import tkinter as tk
from tkinter import PhotoImage, StringVar
from tkinter import ttk
from tkinter.simpledialog import askstring
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from funcoes import ControleDespesasFuncoes
#from bandeja import SystemTray


class ControleDespesasApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Orçamento")
        self.root.geometry("1000x600")

        funcoes = ControleDespesasFuncoes(root=root)
        funcoes.conexao_banco()
        funcoes.criar_tabela_despesas()

        # Menu
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # Opções do Menu
        opcoes_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Menu", menu=opcoes_menu)
        opcoes_menu.add_command(label="Cadastro", command=funcoes.abrir_tela_cadastro)
        opcoes_menu.add_command(label="Relatório", command=funcoes.abrir_tela_relatorio)
        opcoes_menu.add_command(label="Sobre o App", command=funcoes.abrir_tela_sobre_app)
        opcoes_menu.add_separator()
        opcoes_menu.add_command(label="Sair", command=funcoes.sair)
    

if __name__ == "__main__":
    root = tk.Tk()
    app = ControleDespesasApp(root)
    #window = ControleDespesasFuncoes.criar_bandeija_sistema()
    #ControleDespesasFuncoes.adicionar_bandeija(window)
    root.mainloop()

