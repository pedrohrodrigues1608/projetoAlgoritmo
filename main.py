from padaria import Padaria


def carregar_dados_iniciais(padaria):
    """Dados dos Quadros 11 e 12 do enunciado original."""
    produtos = [
        ("Pão francês", "Pães", 0.75, 200),
        ("Pão de queijo", "Salgados", 4.50, 60),
        ("Bolo de cenoura", "Doces", 28.00, 6),
        ("Sonho", "Doces", 6.00, 25),
        ("Café coado", "Bebidas", 5.00, 80),
    ]

    for nome, categoria, preco, quantidade in produtos:
        print(padaria.cadastrar_produto(nome, preco, quantidade, categoria))

    vendas = [
        (1, 120, 1), (2, 15, 1), (5, 30, 1),
        (1, 60, 2), (3, 2, 2),
        (4, 10, 3), (2, 20, 3), (5, 25, 3),
    ]

    for codigo, unidades, dia in vendas:
        print(padaria.registrar_venda(codigo, unidades, dia))


def mostrar_resumo(padaria):
    print("\n--- RESUMO DA PARTE 2 ---")
    for dia, nome in enumerate(padaria.get_dias(), start=1):
        print(
            f"{nome}: {padaria.total_vendido_no_dia(dia)} unidades | "
            f"R$ {padaria.get_faturamento_do_dia(dia):.2f}"
        )

    mais_vendido = padaria.produto_mais_vendido()
    if mais_vendido:
        print(
            f"Produto mais vendido: {mais_vendido.get_nome()} "
            f"({padaria.total_vendido_do_produto(
                padaria.get_produtos().index(mais_vendido)
            )} unidades)"
        )
    else:
        print("Produto mais vendido: ainda não houve vendas.")

    dia_maior = padaria.dia_de_maior_faturamento()
    print(
        "Dia de maior faturamento:",
        padaria.get_dias()[dia_maior - 1] if dia_maior else "Sem vendas"
    )
    print(f"Faturamento total: R$ {padaria.get_faturamento_total():.2f}")
    print(f"Valor em estoque: R$ {padaria.valor_total_em_estoque():.2f}")

    baixos = padaria.produtos_com_estoque_baixo()
    print("Estoque baixo:", ", ".join(p.get_nome() for p in baixos) if baixos else "Nenhum")


if __name__ == "__main__":
    padaria = Padaria("Padaria Pão Quente")
    carregar_dados_iniciais(padaria)
    mostrar_resumo(padaria)

    print("\n--- TESTES ADICIONAIS ---")
    print(padaria.registrar_venda(3, 5, 4))  # deve recusar: estoque insuficiente
    print(padaria.registrar_venda(1, 10, 4))  # deve aceitar
    print(padaria.repor_estoque(3, 12))
    print(padaria.alterar_preco(1, 0.80))

    print("\n--- HISTÓRICO ---")
    for operacao in padaria.get_historico():
        print(operacao)
