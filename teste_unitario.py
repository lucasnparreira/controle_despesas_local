import sqlite3
from tkinter import messagebox
import unittest
import tkinter as tk
from main import ControleDespesasApp
from funcoes import ControleDespesasFuncoes

class TestControleDespesas(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = ControleDespesasApp(self.root)
        self.funcoes = ControleDespesasFuncoes(self.root)

    def tearDown(self):
            try:
                self.root.destroy()
            except tk.TclError:
                # Ignorar o erro caso a aplicação já tenha sido destruída
                pass

    def test_criar_tabela_despesas(self):
        self.funcoes.criar_tabela_despesas()
        # Adicionando uma asserção para verificar se a tabela foi criada corretamente
        self.assertTrue(self.funcoes.verificar_tabela_despesas())

    def test_abrir_tela_cadastro(self):
        # Simulando a abertura da tela de cadastro
        self.funcoes.abrir_tela_cadastro()
        # Adicionando uma asserção para verificar se a tela de cadastro foi aberta corretamente
        self.assertTrue(self.funcoes.tela_cadastro_aberta)

    def test_abrir_tela_relatorio(self):
        # Simulando a abertura da tela de relatório
        self.funcoes.abrir_tela_relatorio()
        # Adicionando uma asserção para verificar se a tela de relatório foi aberta corretamente
        self.assertTrue(self.funcoes.tela_relatorio_aberta)


    # def test_excluir_despesa(self):
    #     self.conexao_bd = sqlite3.connect('controle_despesas.db')
    #     # Simule a entrada de dados para a despesa a ser excluída
    #     self.funcoes.classificacao = "Despesa"
    #     self.funcoes.descricao = "Despesa a Excluir"
    #     self.funcoes.valor_str = "150.0"
    #     self.funcoes.tipo = "Quinzenal"
    #     self.funcoes.data = "2023-12-08"  # Substitua pelo formato de data real que você está usando

    #     # Salve uma despesa para garantir que exista algo para excluir
    #     self.funcoes.salvar_despesa()

    #     # Obtenha as despesas do relatório antes da simulação de exclusão
    #     despesas_antes_excluir = self.funcoes.obter_despesas_do_relatorio()

    #     # Chame a função excluir_despesa com os dados simulados
    #     self.funcoes.excluir_despesa(self.funcoes.descricao)

    #     # Obtenha as despesas do relatório após a simulação de exclusão
    #     despesas_apos_excluir = self.funcoes.obter_despesas_do_relatorio()

    #     # Adicione asserções para verificar se a despesa foi excluída corretamente
    #     self.assertEqual(len(despesas_apos_excluir), len(despesas_antes_excluir) - 1)

    # def test_sair(self):
    #     self.assertTrue(self.root.winfo_exists())

    #     # Simulando a chamada da função sair
    #     self.funcoes.sair()


if __name__ == '__main__':
    unittest.main()



#python -m unittest teste_unitario.py