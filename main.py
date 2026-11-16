import math

import relatorio
from padaria import Padaria


# ------------------------------------------------------------ leitura segura
def ler_inteiro(mensagem):
    """Lê um inteiro; se o usuário digitar algo inválido, pergunta de novo."""
    while True:
        texto = input(mensagem).strip()
        try:
            return int(texto)
        except ValueError:
            print("Valor inválido: digite um número inteiro.")


def ler_decimal(mensagem):
    """Lê um decimal; aceita vírgula ou ponto (5,50 ou 5.50)."""
    while True:
        texto = input(mensagem).strip().replace(",", ".")
        try:
            valor = float(texto)
            if math.isfinite(valor):  # recusa "nan" e "inf"
                return valor
        except ValueError:
            pass
        print("Valor inválido: digite um número, como 5,50.")


def ler_texto(mensagem):
    """Lê um texto que não pode ficar vazio."""
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        print("Este campo não pode ficar vazio.")


# -------------------------------------------------------------- dados iniciais
def carregar_dados_iniciais(padaria):
    """Quadros 11 e 12 do enunciado: 5 produtos e 8 vendas, nessa ordem."""
    produtos = [
        ("Pão francês", "Pães", 0.75, 200),
        ("Pão de queijo", "Salgados", 4.50, 60),
        ("Bolo de cenoura", "Doces", 28.00, 6),
        ("Sonho", "Doces", 6.00, 25),
        ("Café coado", "Bebidas", 5.00, 80),
    ]
    for nome, categoria, preco, quantidade in produtos:
        padaria.cadastrar_produto(nome, preco, quantidade, categoria)

    vendas = [
        (1, 120, 1), (2, 15, 1), (5, 30, 1),
        (1, 60, 2), (3, 2, 2),
        (4, 10, 3), (2, 20, 3), (5, 25, 3),
    ]
    for codigo, unidades, dia in vendas:
        padaria.registrar_venda(codigo, unidades, dia)


# ------------------------------------------------------------------------ menu
def mostrar_menu():
    print()
    print("===== PADARIA PÃO QUENTE =====")
    print(" 1 - Cadastrar produto")
    print(" 2 - Listar estoque")
    print(" 3 - Registrar venda")
    print(" 4 - Repor estoque")
    print(" 5 - Alterar preço")
    print(" 6 - Buscar produto por nome")
    print(" 7 - Relatório de vendas da semana")
    print(" 8 - Produtos com estoque baixo")
    print(" 9 - Fechamento")
    print("10 - Histórico de operações")
    print(" 0 - Sair")


def cadastrar_produto(padaria):
    print("--- Cadastro de produto ---")
    nome = ler_texto("Nome: ")
    categoria = input("Categoria: ").strip()  # pode ficar vazia
    preco = ler_decimal("Preço (R$): ")
    quantidade = ler_inteiro("Quantidade inicial: ")
    print(padaria.cadastrar_produto(nome, preco, quantidade, categoria))


def registrar_venda(padaria):
    print("--- Registro de venda ---")
    codigo = ler_inteiro("Código do produto: ")
    unidades = ler_inteiro("Quantidade vendida: ")
    dia = ler_inteiro("Dia (1-Seg 2-Ter 3-Qua 4-Qui 5-Sex 6-Sáb 7-Dom): ")
    print(padaria.registrar_venda(codigo, unidades, dia))


def repor_estoque(padaria):
    print("--- Reposição de estoque ---")
    codigo = ler_inteiro("Código do produto: ")
    unidades = ler_inteiro("Unidades a repor: ")
    print(padaria.repor_estoque(codigo, unidades))


def alterar_preco(padaria):
    print("--- Alteração de preço ---")
    codigo = ler_inteiro("Código do produto: ")
    novo_preco = ler_decimal("Novo preço (R$): ")
    print(padaria.alterar_preco(codigo, novo_preco))


def buscar_produto(padaria):
    print("--- Busca por nome ---")
    trecho = ler_texto("Parte do nome: ")
    relatorio.imprimir_resultado_busca(padaria.buscar_por_nome(trecho), trecho)


def main():
    padaria = Padaria("Padaria Pão Quente")
    carregar_dados_iniciais(padaria)

    acoes = {
        1: cadastrar_produto,
        2: relatorio.imprimir_estoque,
        3: registrar_venda,
        4: repor_estoque,
        5: alterar_preco,
        6: buscar_produto,
        7: relatorio.imprimir_vendas_da_semana,
        8: relatorio.imprimir_estoque_baixo,
        9: relatorio.imprimir_fechamento,
        10: relatorio.imprimir_historico,
    }

    opcao = -1
    while opcao != 0:
        mostrar_menu()
        opcao = ler_inteiro("Escolha uma opção: ")
        if opcao == 0:
            relatorio.imprimir_fechamento(padaria)
            print("Até logo!")
        elif opcao in acoes:
            acoes[opcao](padaria)
        else:
            print("Opção inválida. Digite um número de 0 a 10.")


if __name__ == "__main__":
    main()
