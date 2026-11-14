# relatorio.py
from typing import List
from produto import Produto  # opcional (só para type hints)

LINHA = "-" * 70

def imprimirEstoque(padaria) -> None:
    print("\nESTOQUE ATUAL")
    print(LINHA)

    produtos: List[Produto] = padaria.get_produtos()
    if not produtos:
        print("Sem produtos cadastrados.")
        print(LINHA)
        return

    print(f"{'COD':<6} {'NOME':<28} {'CATEGORIA':<14} {'PRECO':>10} {'QTD':>8}")
    print(LINHA)

    for p in produtos:
        print(
            f"{p.get_codigo():<6} "
            f"{p.get_nome()[:28]:<28} "
            f"{p.get_categoria()[:14]:<14} "
            f"R$ {p.get_preco():>7.2f} "
            f"{p.get_quantidade():>8d}"
        )

    print(LINHA)


def imprimirResultadoBusca(lista_produtos: List[Produto]) -> None:
    print("\nRESULTADO DA BUSCA")
    print(LINHA)

    if not lista_produtos:
        print("Nenhum produto encontrado.")
        print(LINHA)
        return

    print(f"{'COD':<6} {'NOME':<28} {'CATEGORIA':<14} {'PRECO':>10} {'QTD':>8}")
    print(LINHA)

    for p in lista_produtos:
        print(
            f"{p.get_codigo():<6} "
            f"{p.get_nome()[:28]:<28} "
            f"{p.get_categoria()[:14]:<14} "
            f"R$ {p.get_preco():>7.2f} "
            f"{p.get_quantidade():>8d}"
        )

    print(LINHA)


def imprimirEstoqueBaixo(padaria, limite: int = 5) -> None:
    print("\nESTOQUE BAIXO")
    print(LINHA)

    produtos = padaria.get_produtos()
    baixos = [p for p in produtos if p.get_quantidade() < limite]

    if not baixos:
        print(f"Nenhum produto com estoque baixo (limite < {limite}).")
        print(LINHA)
        return

    print(f"{'COD':<6} {'NOME':<28} {'CATEGORIA':<14} {'PRECO':>10} {'QTD':>8}")
    print(LINHA)

    for p in baixos:
        print(
            f"{p.get_codigo():<6} "
            f"{p.get_nome()[:28]:<28} "
            f"{p.get_categoria()[:14]:<14} "
            f"R$ {p.get_preco():>7.2f} "
            f"{p.get_quantidade():>8d}"
        )

    print(LINHA)


# ======= Pendências para E4 (vendas) — seu Padaria não implementa vendas =======
def imprimirVendasDaSemana(padaria) -> None:
    print("\nVENDAS DA SEMANA")
    print(LINHA)
    print("Pendente: seu Padaria não possui métodos de vendas (ex: get_vendas/registrar_venda).")
    print(LINHA)


def imprimirFechamento(padaria) -> None:
    print("\nFECHAMENTO")
    print(LINHA)
    print("Pendente: seu Padaria não possui métodos de vendas (ex: get_vendas/registrar_venda).")
    print(LINHA)


def imprimirHistorico(padaria) -> None:
    print("\nHISTÓRICO")
    print(LINHA)
    print("Pendente: seu Padaria não possui métodos de vendas (ex: get_vendas/registrar_venda).")
    print(LINHA)
