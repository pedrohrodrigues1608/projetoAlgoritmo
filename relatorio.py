
"""Camada de aplicação: menu e integração das classes."""

import main as entrada
import relatorio

from padaria import Padaria


class Aplicacao:
    """Controla o fluxo do sistema sem duplicar as regras de negócio."""

    def __init__(self):
        self.padaria = Padaria("Padaria Pão Quente")
        entrada.carregar_dados_iniciais(self.padaria)

    def executar(self):
        acoes = {
            1: self.cadastrar_produto,
            2: lambda: relatorio.imprimir_estoque(self.padaria),
            3: self.registrar_venda,
            4: self.repor_estoque,
            5: self.alterar_preco,
            6: self.buscar_produto,
            7: lambda: relatorio.imprimir_vendas_da_semana(self.padaria),
            8: lambda: relatorio.imprimir_estoque_baixo(self.padaria),
            9: lambda: relatorio.imprimir_fechamento(self.padaria),
            10: lambda: relatorio.imprimir_historico(self.padaria),
        }

        while True:
            entrada.mostrar_menu()
            opcao = entrada.ler_inteiro("Escolha uma opção: ")

            if opcao == 0:
                relatorio.imprimir_fechamento(self.padaria)
                print("Até logo!")
                break

            acao = acoes.get(opcao)

            if acao is None:
                print("Opção inválida. Digite um número de 0 a 10.")
            else:
                acao()

    def cadastrar_produto(self):
        entrada.cadastrar_produto(self.padaria)

    def registrar_venda(self):
        entrada.registrar_venda(self.padaria)

    def repor_estoque(self):
        entrada.repor_estoque(self.padaria)

    def alterar_preco(self):
        entrada.alterar_preco(self.padaria)

    def buscar_produto(self):
        entrada.buscar_produto(self.padaria)


if __name__ == "__main__":
    Aplicacao().executar()
