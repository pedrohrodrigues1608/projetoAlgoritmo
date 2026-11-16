
"""Relatórios de estoque, vendas e fechamento da Padaria Pão Quente."""

from padaria import formatar_moeda


def _linha():
    print("-" * 92)


def imprimir_estoque(padaria):
    print("\n========== RELATÓRIO DE ESTOQUE ==========")

    produtos = padaria.get_produtos()

    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    print(
        f"{'Cód.':<6}{'Produto':<25}{'Categoria':<16}"
        f"{'Preço':>13}{'Qtd.':>8}{'Valor':>16}"
    )

    _linha()

    for produto in produtos:
        print(
            f"{produto.get_codigo():<6}"
            f"{produto.get_nome()[:24]:<25}"
            f"{produto.get_categoria()[:15]:<16}"
            f"{formatar_moeda(produto.get_preco()):>13}"
            f"{produto.get_quantidade():>8}"
            f"{formatar_moeda(produto.valor_em_estoque()):>16}"
        )

    _linha()

    print(f"Quantidade de produtos: {padaria.get_quantidade_de_produtos()}")
    print(
        f"Valor total em estoque: "
        f"{formatar_moeda(padaria.valor_total_em_estoque())}"
    )


def imprimir_resultado_busca(produtos, trecho=""):
    print(f"\n========== RESULTADO DA BUSCA: {trecho!r} ==========")

    if not produtos:
        print("Nenhum produto encontrado.")
        return

    for produto in produtos:
        print(
            f"Código: {produto.get_codigo()} | "
            f"Nome: {produto.get_nome()} | "
            f"Categoria: {produto.get_categoria()} | "
            f"Preço: {formatar_moeda(produto.get_preco())} | "
            f"Estoque: {produto.get_quantidade()}"
        )

    print(f"Total encontrado: {len(produtos)}")


def imprimir_vendas_da_semana(padaria):
    print("\n========== RELATÓRIO DE VENDAS DA SEMANA ==========")

    produtos = padaria.get_produtos()
    dias = padaria.get_dias()

    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    colunas = [f"{dia:>7}" for dia in dias]

    print(
        f"{'Produto':<24}"
        + "".join(colunas)
        + f"{'Total':>9}"
    )

    _linha()

    total_geral = 0

    for indice, produto in enumerate(produtos):
        valores = [
            padaria.get_vendas(indice, dia)
            for dia in range(1, 8)
        ]

        total_produto = sum(valores)
        total_geral += total_produto

        print(
            f"{produto.get_nome()[:23]:<24}"
            + "".join(f"{valor:>7}" for valor in valores)
            + f"{total_produto:>9}"
        )

    _linha()

    totais_dia = [
        padaria.total_vendido_no_dia(dia)
        for dia in range(1, 8)
    ]

    print(
        f"{'Total por dia':<24}"
        + "".join(f"{valor:>7}" for valor in totais_dia)
        + f"{total_geral:>9}"
    )

    print(f"Total de unidades vendidas na semana: {total_geral}")


def imprimir_estoque_baixo(padaria):
    print("\n========== PRODUTOS COM ESTOQUE BAIXO ==========")

    produtos = padaria.produtos_com_estoque_baixo()

    if not produtos:
        print("Não há produtos com estoque baixo.")
        return

    print("Critério: quantidade inferior a 5 unidades.")

    for produto in produtos:
        print(
            f"Código: {produto.get_codigo()} | "
            f"{produto.get_nome()} | "
            f"Estoque atual: {produto.get_quantidade()}"
        )

    print(f"Total de produtos com estoque baixo: {len(produtos)}")


def imprimir_fechamento(padaria):
    print("\n========== FECHAMENTO DA SEMANA ==========")

    dias = padaria.get_dias()

    for numero, dia in enumerate(dias, start=1):
        print(
            f"{dia:<5}: "
            f"{formatar_moeda(padaria.get_faturamento_do_dia(numero))}"
        )

    _linha()

    print(
        f"Faturamento total: "
        f"{formatar_moeda(padaria.get_faturamento_total())}"
    )

    mais_vendido = padaria.produto_mais_vendido()

    if mais_vendido is None:
        print("Produto mais vendido: ainda não houve vendas.")
    else:
        indice = next(
            (
                i for i, p in enumerate(padaria.get_produtos())
                if p.get_codigo() == mais_vendido.get_codigo()
            ),
            None,
        )

        quantidade = (
            padaria.total_vendido_do_produto(indice)
            if indice is not None else 0
        )

        print(
            f"Produto mais vendido: "
            f"{mais_vendido.get_nome()} ({quantidade} unidades)"
        )

    melhor_dia = padaria.dia_de_maior_faturamento()

    if melhor_dia == 0:
        print("Dia de maior faturamento: ainda não houve vendas.")
    else:
        print(
            f"Dia de maior faturamento: "
            f"{dias[melhor_dia - 1]} "
            f"({formatar_moeda(padaria.get_faturamento_do_dia(melhor_dia))})"
        )

    print(
        f"Valor atual do estoque: "
        f"{formatar_moeda(padaria.valor_total_em_estoque())}"
    )


def imprimir_historico(padaria):
    print("\n========== HISTÓRICO DE OPERAÇÕES ==========")

    historico = padaria.get_historico()

    if not historico:
        print("Nenhuma operação registrada.")
        return

    for operacao in historico:
        print(operacao)

    print(f"Total de operações registradas: {len(historico)}")


# Aliases em camelCase, caso o grupo esteja usando os nomes do enunciado.

imprimirEstoque = imprimir_estoque
imprimirResultadoBusca = imprimir_resultado_busca
imprimirVendasDaSemana = imprimir_vendas_da_semana
imprimirEstoqueBaixo = imprimir_estoque_baixo
imprimirFechamento = imprimir_fechamento
imprimirHistorico = imprimir_historico
