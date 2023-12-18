import tkinter as tk
from tkinter import StringVar, ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import sqlite3

class ControleDespesasFuncoes:
    def __init__(self, root):
        self.root = root
        self.inicializar_interface()
        self.conexao_banco()

    def criar_tabela_despesas(self):
        # Criar tabela de despesas se não existir
        cursor = self.conexao_bd.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS despesas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                classificacao TEXT NOT NULL,
                tipo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                data TEXT NOT NULL
            )
        """)
        self.conexao_bd.commit()
        cursor.close()

    def inicializar_interface(self):
        caminho_imagem = "/Users/lucasparreira/Documents/Projects/controle_despesas/old-vintage-pc-clipart-design-illustration-free-png.png"
        imagem_original = Image.open(caminho_imagem)
        largura_desejada = 400  
        altura_desejada = 300  
        imagem_redimensionada = imagem_original.resize((largura_desejada, altura_desejada), Image.ANTIALIAS)
        self.imagem = ImageTk.PhotoImage(imagem_redimensionada)

        label_imagem = tk.Label(self.root, image=self.imagem)
        label_imagem.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    def conexao_banco(self):
        self.conexao_bd = sqlite3.connect('controle_despesas.db')

    def abrir_tela_cadastro(self):
        nova_janela = tk.Toplevel(self.root)
        nova_janela.title("Cadastro de Despesa")
        nova_janela.transient(self.root)

        frame_cadastro = tk.Frame(nova_janela)
        frame_cadastro.pack(padx=20, pady=20)

        # Widgets para o cadastro
        lbl_classificacao = tk.Label(frame_cadastro, text="Classificação:")
        lbl_classificacao.grid(row=0, column=0, padx=10, pady=10)
        tipos_classificacao = ["Despesa", "Recebido"]
        self.combo_classificacao= tk.StringVar()
        self.combo_classificacao.set(tipos_classificacao[0])
        dropdown_classificacao = tk.OptionMenu(frame_cadastro, self.combo_classificacao, *tipos_classificacao)
        dropdown_classificacao.grid(row=0, column=1, padx=10, pady=10)

        lbl_descricao = tk.Label(frame_cadastro, text="Descrição:")
        lbl_descricao.grid(row=1, column=0, padx=10, pady=10)
        self.entry_descricao = tk.Entry(frame_cadastro)
        self.entry_descricao.grid(row=1, column=1, padx=10, pady=10)

        lbl_valor = tk.Label(frame_cadastro, text="Valor:")
        lbl_valor.grid(row=2, column=0, padx=10, pady=10)
        self.entry_valor = tk.Entry(frame_cadastro)
        self.entry_valor.grid(row=2, column=1, padx=10, pady=10)

        lbl_tipo = tk.Label(frame_cadastro, text="Tipo:")
        lbl_tipo.grid(row=3, column=0, padx=10, pady=10)
        tipos_despesa = ["Mensal", "Quinzenal", "Semanal"]
        self.combo_tipo = tk.StringVar()
        self.combo_tipo.set(tipos_despesa[0])
        dropdown_tipo = tk.OptionMenu(frame_cadastro, self.combo_tipo, *tipos_despesa)
        dropdown_tipo.grid(row=3, column=1, padx=10, pady=10)

        lbl_data = tk.Label(frame_cadastro, text="Data:")
        lbl_data.grid(row=4, column=0, padx=10, pady=10)
        self.cal_data = DateEntry(frame_cadastro, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.cal_data.grid(row=4, column=1, padx=10, pady=10)

        btn_salvar = tk.Button(frame_cadastro, text="Salvar", command=self.salvar_despesa)
        btn_salvar.grid(row=5, column=0, columnspan=2, pady=10)

    def salvar_despesa(self):
        classificacao = self.combo_classificacao.get()
        descricao = self.entry_descricao.get()
        valor_str = self.entry_valor.get()
        tipo = self.combo_tipo.get()
        data = self.cal_data.get_date()

        try:
            # Verificar se o campo de valor não está vazio
            if not valor_str:
                messagebox.showerror("Erro", "O campo de valor não pode ficar vazio.")
                return

            # Converter o valor para um tipo numérico (float) antes de inserir no banco de dados
            valor = float(valor_str)

            cursor = self.conexao_bd.cursor()
            cursor.execute("""
                INSERT INTO despesas (classificacao, descricao, valor, tipo, data) 
                VALUES (?, ?, ?, ?, ?)
            """, (classificacao, descricao, valor, tipo, str(data)))
            self.conexao_bd.commit()
            cursor.close()
            messagebox.showinfo("Sucesso", "Despesa cadastrada com sucesso!")

            # Limpar os campos após o cadastro
            self.entry_descricao.delete(0, tk.END)
            self.entry_valor.delete(0, tk.END)
            self.combo_tipo.set(self.tipos_despesa[0])
            self.cal_data.set_date(None)

        except ValueError:
            messagebox.showerror("Erro", "O valor deve ser numérico.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar despesa: {str(e)}")

    def abrir_tela_relatorio(self):
        nova_janela = tk.Toplevel(self.root)
        nova_janela.title("Relatório de Despesas")
        nova_janela.transient(self.root)

        frame_relatorio = tk.Frame(nova_janela)
        frame_relatorio.pack(padx=20, pady=20)

        # Criação de uma treeview para exibir os relatórios
        self.tree = ttk.Treeview(frame_relatorio, columns=("ID","Classificação","Tipo","Descrição", "Valor", "Data"))
        self.tree.heading("#0", text="ID", anchor=tk.W)
        self.tree.heading("#1", text="Classificação", anchor=tk.W)
        self.tree.heading("#2", text="Tipo", anchor=tk.W)
        self.tree.heading("#3", text="Descrição", anchor=tk.W)
        self.tree.heading("#4", text="Valor", anchor=tk.W)
        self.tree.heading("#5", text="Data", anchor=tk.W)

        # for col in tree["columns"]:
        #     tree.column(col, width=tk.BU, minwidth=100, anchor=tk.W)

        self.tree.pack(expand=True, fill=tk.BOTH)

        # Preenche a treeview com os dados do banco de dados
        cursor = self.conexao_bd.cursor()
        cursor.execute("SELECT * FROM despesas")
        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=row)
        cursor.close()

        self.tree.bind("<Double-1>", lambda event: self.editar_despesa(self.tree))
        self.tree.bind("<KeyPress-d>", self.excluir_despesa)

    def editar_despesa(self, janela_pai):
        # Obtém o item selecionado na treeview
        self.item_selecionado = self.tree.selection()
        
        if not self.item_selecionado:
            messagebox.showinfo("Aviso", "Selecione uma despesa para editar.")
            return

        # Obtém os detalhes da despesa selecionada
        id_despesa = self.tree.item(self.item_selecionado, "values")[0]
        classificacao = self.tree.item(self.item_selecionado, "values")[1]
        tipo = self.tree.item(self.item_selecionado, "values")[2]
        descricao = self.tree.item(self.item_selecionado, "values")[3]
        valor = self.tree.item(self.item_selecionado, "values")[4]
        data = self.tree.item(self.item_selecionado, "values")[5]

        # Cria uma nova janela para edição
        janela_edicao = tk.Toplevel(self.root)
        janela_edicao.title("Editar Despesa")

        frame_edicao = tk.Frame(janela_edicao)
        frame_edicao.pack(padx=20, pady=20)

        # Widgets para a edição
        lbl_classificacao = tk.Label(frame_edicao, text="Nova Classificação:")
        lbl_classificacao.grid(row=0, column=0, padx=10, pady=10)
        entry_classificacao = tk.Entry(frame_edicao)
        entry_classificacao.grid(row=0, column=1, padx=10, pady=10)
        entry_classificacao.insert(0, classificacao)

        entry_classificacao.bind("<KeyPress-Return>", lambda event: self.salvar_edicao(self.tree, id_despesa, entry_classificacao.get(), entry_descricao.get(), entry_valor.get(), entry_tipo.get(), cal_data.get_date(), janela_pai))

        lbl_tipo = tk.Label(frame_edicao, text="Novo Tipo:")
        lbl_tipo.grid(row=1, column=0, padx=10, pady=10)
        entry_tipo = tk.Entry(frame_edicao)
        entry_tipo.grid(row=1, column=1, padx=10, pady=10)
        entry_tipo.insert(0, tipo)

        entry_tipo.bind("<KeyPress-Return>", lambda event: self.salvar_edicao(self.tree, id_despesa, entry_classificacao.get(), entry_descricao.get(), entry_valor.get(), entry_tipo.get(), cal_data.get_date(), janela_pai))

        lbl_descricao = tk.Label(frame_edicao, text="Nova Descrição:")
        lbl_descricao.grid(row=2, column=0, padx=10, pady=10)
        entry_descricao = tk.Entry(frame_edicao)
        entry_descricao.grid(row=2, column=1, padx=10, pady=10)
        entry_descricao.insert(0, descricao)

        entry_descricao.bind("<KeyPress-Return>", lambda event: self.salvar_edicao(self.tree, id_despesa,entry_classificacao.get(), entry_descricao.get(), entry_valor.get(), entry_tipo.get(), cal_data.get_date(), janela_pai))

        
        lbl_valor = tk.Label(frame_edicao, text="Novo Valor:")
        lbl_valor.grid(row=3, column=0, padx=10, pady=10)
        entry_valor = tk.Entry(frame_edicao)
        entry_valor.grid(row=3, column=1, padx=10, pady=10)
        entry_valor.insert(0, valor)

        entry_valor.bind("<KeyPress-Return>", lambda event: self.salvar_edicao(self.tree, id_despesa, entry_classificacao.get(), entry_descricao.get(), entry_valor.get(), entry_tipo.get(), cal_data.get_date(), janela_pai))

    
        lbl_data = tk.Label(frame_edicao, text="Nova Data:")
        lbl_data.grid(row=4, column=0, padx=10, pady=10)
        cal_data = DateEntry(frame_edicao, width=12, background='darkblue', foreground='white', borderwidth=2)
        cal_data.grid(row=4, column=1, padx=10, pady=10)
        cal_data.set_date(data)

        cal_data.bind("<KeyPress-Return>", lambda event: self.salvar_edicao(self.tree, id_despesa, entry_classificacao.get(), entry_descricao.get(), entry_valor.get(), entry_tipo.get(), cal_data.get_date(), janela_pai))

    def carregar_relatorio(self):
        # Limpa os dados existentes na treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Preenche a treeview com os dados do banco de dados
        cursor = self.conexao_bd.cursor()
        cursor.execute("SELECT * FROM despesas")
        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=row)
        cursor.close()

    def salvar_edicao(self, tree, id_despesa, classificacao, descricao, valor, tipo, data, janela_pai):
        try:
            cursor = self.conexao_bd.cursor()
            cursor.execute("""
                UPDATE despesas 
                SET classificacao = ?, descricao = ?, valor = ?, tipo = ?, data = ? 
                WHERE id = ?
            """, (classificacao, descricao, valor, tipo, data, id_despesa))
            self.conexao_bd.commit()
            cursor.close()

            messagebox.showinfo("Sucesso", "Despesa editada com sucesso!")

            # Atualizar a treeview com os dados atualizados
            tree.item(self.item_selecionado, values=(id_despesa, classificacao, descricao, valor, tipo, data))

            # Recarregar os dados do relatório após a edição
            self.carregar_relatorio()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao editar despesa: {str(e)}")

    def excluir_despesa(self, event):
        # Obter o item selecionado na treeview
        item_selecionado = self.tree.selection()

        if not item_selecionado:
            return

        # Exibir uma caixa de diálogo de confirmação
        resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir esta despesa?")
        
        if resposta:
            try:
                # Obter o ID da despesa selecionada
                id_despesa = self.tree.item(item_selecionado, "values")[0]

                # Executar a exclusão no banco de dados
                cursor = self.conexao_bd.cursor()
                cursor.execute("DELETE FROM despesas WHERE id = %s", (id_despesa,))
                self.conexao_bd.commit()
                cursor.close()

                messagebox.showinfo("Sucesso", "Despesa excluída com sucesso!")

                # Recarregar os dados do relatório após a exclusão
                self.carregar_relatorio()

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir despesa: {str(e)}")


    def sair(self):
        self.conexao_bd.close()
        self.root.destroy()