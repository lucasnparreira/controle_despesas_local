import tkinter as tk
from tkinter import PhotoImage, StringVar
from tkinter import ttk
from tkinter.simpledialog import askstring
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from funcoes import ControleDespesasFuncoes

class ControleDespesasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Orçamento")
        self.root.geometry("1000x600")

        caminho_imagem = "/Users/lucasparreira/Documents/Projects/controle_despesas/old-vintage-pc-clipart-design-illustration-free-png.png"
        imagem_original = Image.open(caminho_imagem)
        largura_desejada = 400  
        altura_desejada = 300  
        imagem_redimensionada = imagem_original.resize((largura_desejada, altura_desejada), Image.ANTIALIAS)
        self.imagem = ImageTk.PhotoImage(imagem_redimensionada)

        label_imagem = tk.Label(self.root, image=self.imagem)
        label_imagem.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
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
        opcoes_menu.add_separator()
        opcoes_menu.add_command(label="Sair", command=funcoes.sair)

        # Carregar um ícone de lixeira para exclusão
        self.icon_path = "/Users/lucasparreira/Documents/Projects/controle_despesas/trash.png"
        self.trash_icon = Image.open(self.icon_path)
        self.trash_icon = self.trash_icon.resize((20, 20), Image.ANTIALIAS)
        self.trash_icon = ImageTk.PhotoImage(self.trash_icon)


         # Widgets para o cadastro
        self.entry_descricao = tk.Entry(self.root)
        self.valor_var = StringVar()
        self.entry_valor = tk.Entry(self.root,textvariable=self.valor_var)
        self.tipos_despesa = ["Mensal", "Quinzenal", "Semanal"]
        self.combo_tipo = tk.StringVar()
        self.combo_tipo.set(self.tipos_despesa[0])
        self.dropdown_tipo = tk.OptionMenu(self.root, self.combo_tipo, *self.tipos_despesa)
        self.cal_data = DateEntry(self.root, width=12, background='darkblue', foreground='white', borderwidth=2)


if __name__ == "__main__":
    root = tk.Tk()
    app = ControleDespesasApp(root)
    root.mainloop()

