
from produto import Produto


def formatar_moeda(valor):
    """Formata em reais com vírgula decimal."""
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


class Padaria:
    """Regras de negócio e armazenamento da padaria."""

    MAX_PRODUTOS = 20
    LIMITE_ESTOQUE_BAIXO = 5
    DIAS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

    def __init__(self, nome):
        self._nome = nome
        self._produtos = []
        self._historico = []
        self._vendas = [[0] * 7 for _ in range(self.MAX_PRODUTOS)]
        self._faturamento_por_dia = [0.0] * 7

    def get_nome(self):
        return self._nome

    def cadastrar_produto(self, nome, preco, quantidade, categoria=""):
        nome = str(nome).strip()

        if not nome:
            return "ERRO: o nome não pode ficar vazio."

        if self._existe_produto_com_nome(nome):
            return f"ERRO: já existe um produto chamado {nome}."

        if not self._numero_positivo(preco):
            return "ERRO: o preço deve ser maior que zero."

        if not self._inteiro(quantidade) or quantidade < 0:
            return "ERRO: a quantidade inicial não pode ser negativa."

        if len(self._produtos) >= self.MAX_PRODUTOS:
            return f"ERRO: limite de {self.MAX_PRODUTOS} produtos atingido."

        categoria = str(categoria).strip() or "Sem categoria"
        produto = Produto(nome, preco, quantidade, categoria)
        self._produtos.append(produto)

        self._registrar_no_historico(
            f"Cadastro: {nome} ({categoria}) a "
            f"{formatar_moeda(preco)}, {quantidade} un."
        )

        return f"OK: produto cadastrado com o código {produto.get_codigo()}."

    def buscar_por_codigo(self, codigo):
        indice = self._indice_do_produto(codigo)
        return None if indice == -1 else self._produtos[indice]

    def buscar_por_nome(self, trecho):
        busca = str(trecho).strip().lower()
        return [
            p for p in self._produtos
            if busca in p.get_nome().lower()
        ]

    def get_produtos(self):
        return self._produtos.copy()

    def get_quantidade_de_produtos(self):
        return len(self._produtos)

    def registrar_venda(self, codigo, unidades, dia):
        indice = self._indice_do_produto(codigo)

        if indice == -1:
            return f"ERRO: produto de código {codigo} não encontrado."

        if not self._quantidade_inteira_positiva(unidades):
            return "ERRO: a quantidade vendida deve ser maior que zero."

        if not self._dia_valido(dia):
            return "ERRO: dia inválido. Use um número de 1 (Seg) a 7 (Dom)."

        produto = self._produtos[indice]

        if unidades > produto.get_quantidade():
            return (
                "ERRO: estoque insuficiente. "
                f"Disponível: {produto.get_quantidade()} unidade(s)."
            )

        produto.remover_estoque(unidades)
        total = unidades * produto.get_preco()

        self._vendas[indice][dia - 1] += unidades
        self._faturamento_por_dia[dia - 1] += total

        self._registrar_no_historico(
            f"Venda: {unidades} x {produto.get_nome()} "
            f"({self.DIAS[dia - 1]}) = {formatar_moeda(total)}"
        )

        return (
            f"OK: venda registrada. Total: {formatar_moeda(total)}. "
            f"Estoque restante: {produto.get_quantidade()}."
        )

    def repor_estoque(self, codigo, unidades):
        produto = self.buscar_por_codigo(codigo)

        if produto is None:
            return f"ERRO: produto de código {codigo} não encontrado."

        if not self._quantidade_inteira_positiva(unidades):
            return "ERRO: a quantidade para reposição deve ser maior que zero."

        produto.adicionar_estoque(unidades)

        self._registrar_no_historico(
            f"Reposição: {unidades} x {produto.get_nome()}"
        )

        return (
            f"OK: estoque de {produto.get_nome()} agora é "
            f"{produto.get_quantidade()}."
        )

    def alterar_preco(self, codigo, novo_preco):
        produto = self.buscar_por_codigo(codigo)

        if produto is None:
            return f"ERRO: produto de código {codigo} não encontrado."

        if not self._numero_positivo(novo_preco):
            return "ERRO: o preço deve ser maior que zero."

        produto.set_preco(novo_preco)

        self._registrar_no_historico(
            f"Preço: {produto.get_nome()} passou a "
            f"{formatar_moeda(novo_preco)}"
        )

        return (
            f"OK: preço de {produto.get_nome()} alterado para "
            f"{formatar_moeda(novo_preco)}."
        )

    def get_vendas(self, posicao_produto, dia):
        if (
            not 0 <= posicao_produto < len(self._produtos)
            or not self._dia_valido(dia)
        ):
            return 0

        return self._vendas[posicao_produto][dia - 1]

    def total_vendido_do_produto(self, posicao_produto):
        if not 0 <= posicao_produto < len(self._produtos):
            return 0

        return sum(self._vendas[posicao_produto])

    def total_vendido_no_dia(self, dia):
        if not self._dia_valido(dia):
            return 0

        return sum(
            self._vendas[i][dia - 1]
            for i in range(len(self._produtos))
        )

    def get_faturamento_do_dia(self, dia):
        if not self._dia_valido(dia):
            return 0.0

        return self._faturamento_por_dia[dia - 1]

    def get_faturamento_total(self):
        return sum(self._faturamento_por_dia)

    def produto_mais_vendido(self):
        melhor = None
        melhor_total = 0

        for i, produto in enumerate(self._produtos):
            total = self.total_vendido_do_produto(i)

            if total > melhor_total:
                melhor = produto
                melhor_total = total

        return melhor

    def dia_de_maior_faturamento(self):
        melhor_dia = 0
        melhor_valor = 0.0

        for dia in range(1, 8):
            if self._faturamento_por_dia[dia - 1] > melhor_valor:
                melhor_dia = dia
                melhor_valor = self._faturamento_por_dia[dia - 1]

        return melhor_dia

    def produtos_com_estoque_baixo(self):
        return [
            p for p in self._produtos
            if p.estoque_baixo(self.LIMITE_ESTOQUE_BAIXO)
        ]

    def valor_total_em_estoque(self):
        return sum(
            p.valor_em_estoque()
            for p in self._produtos
        )

    def get_historico(self):
        return self._historico.copy()

    def get_dias(self):
        return self.DIAS

    def _indice_do_produto(self, codigo):
        for i, produto in enumerate(self._produtos):
            if produto.get_codigo() == codigo:
                return i

        return -1

    def _existe_produto_com_nome(self, nome):
        return any(
            p.get_nome().lower() == nome.strip().lower()
            for p in self._produtos
        )

    def _dia_valido(self, dia):
        return self._inteiro(dia) and 1 <= dia <= 7

    @staticmethod
    def _inteiro(valor):
        return isinstance(valor, int) and not isinstance(valor, bool)

    def _quantidade_inteira_positiva(self, valor):
        return self._inteiro(valor) and valor > 0

    @staticmethod
    def _numero_positivo(valor):
        return (
            isinstance(valor, (int, float))
            and not isinstance(valor, bool)
            and valor > 0
        )

    def _registrar_no_historico(self, descricao):
        self._historico.append(
            f"{len(self._historico) + 1:03d} | {descricao}"
        )
