# aplicacao.py
from padaria import Padaria
from relatorio import (
    imprimirEstoque,
    imprimirResultadoBusca,
    imprimirVendasDaSemana,
    imprimirEstoqueBaixo,
    imprimirFechamento,
    imprimirHistorico,
)

def ler_int_seguro(msg: str) -> int:
    # RN09 (leitura segura): como você não colou o Apêndice A, usei validação padrão.
    while True:
        s = input(msg).strip()
        try:
            return int(s)
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def carregarDadosIniciais(padaria: Padaria) -> None:
    """
    E4 - Quadros 11 e 12 (produtos e vendas padrão).
    Você ainda não mandou os quadros, então por enquanto carrego só PRODUTOS
    com base no que já aparece no seu main de teste.
    """
    # Produtos padrão (ajuste para seus Quadros 11/12 quando você mandar)
    padaria.cadastrar_produto("Pão Francês", 0.85, 100, "Panificação")
    padaria.cadastrar_produto("Pão de Queijo", 3.50, 40, "Salgados")
    padaria.cadastrar_produto("Bolo de Chocolate", 32.00, 4, "Confeitaria")


def main():
    padaria = Padaria()
    carregarDadosIniciais(padaria)

    executando = True
    while executando:  # do-while equivalente
        print("\n=== MENU PRINCIPAL ===")
        print("1 - Imprimir estoque")
        print("2 - Buscar produto (por código ou nome)")
        print("3 - Imprimir vendas da semana")
        print("4 - Imprimir estoque baixo")
        print("5 - Imprimir fechamento")
        print("6 - Imprimir histórico")
        print("0 - Sair")
        print("======================")

        opcao = ler_int_seguro("Escolha uma opção: ")

        # switch em Python
        match opcao:
            case 0:
                executando = False
                print("Encerrando...")
            case 1:
                imprimirEstoque(padaria)
            case 2:
                sub = ler_int_seguro("Buscar por: 1-Código | 2-Nome : ")
                if sub == 1:
                    cod = ler_int_seguro("Digite o código: ")
                    achado = padaria.buscar_por_codigo(cod)
                    imprimirResultadoBusca([achado] if achado is not None else [])
                elif sub == 2:
                    termo = input("Digite o nome/parcial: ").strip()
                    encontrados = padaria.buscar_por_nome(termo)
                    imprimirResultadoBusca(encontrados)
                else:
                    print("Opção inválida.")
            case 3:
                imprimirVendasDaSemana(padaria)
            case 4:
                limite = ler_int_seguro("Defina o limite (estoque baixo): ")
                imprimirEstoqueBaixo(padaria, limite)
            case 5:
                imprimirFechamento(padaria)
            case 6:
                imprimirHistorico(padaria)
            case _:
                print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
