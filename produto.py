
class Produto:
    """Produto da padaria: protege os dados e valida preço e estoque."""

    _proximo_codigo = 1

    def __init__(self, nome, preco, quantidade=0, categoria="Geral"):
        self._codigo = Produto._proximo_codigo
        Produto._proximo_codigo += 1

        self._nome = str(nome).strip()
        categoria = str(categoria).strip() if categoria else ""
        self._categoria = categoria or "Sem categoria"

        self._preco = float(preco) if self._numero_positivo(preco) else 0.0

        self._quantidade = (
            quantidade if self._inteiro(quantidade) and quantidade >= 0 else 0
        )

    @staticmethod
    def _inteiro(valor):
        return isinstance(valor, int) and not isinstance(valor, bool)

    @staticmethod
    def _numero_positivo(valor):
        return (
            isinstance(valor, (int, float))
            and not isinstance(valor, bool)
            and valor > 0
        )

    def get_codigo(self):
        return self._codigo

    def get_nome(self):
        return self._nome

    def get_categoria(self):
        return self._categoria

    def get_preco(self):
        return self._preco

    def get_quantidade(self):
        return self._quantidade

    def set_preco(self, novo_preco):
        if not self._numero_positivo(novo_preco):
            return False

        self._preco = float(novo_preco)
        return True

    def adicionar_estoque(self, quantidade):
        if not self._inteiro(quantidade) or quantidade <= 0:
            return False

        self._quantidade += quantidade
        return True

    def remover_estoque(self, quantidade):
        if (
            not self._inteiro(quantidade)
            or quantidade <= 0
            or quantidade > self._quantidade
        ):
            return False

        self._quantidade -= quantidade
        return True

    def valor_em_estoque(self):
        return self._preco * self._quantidade

    def estoque_baixo(self, limite=5):
        return self._quantidade < limite

    def __str__(self):
        aviso = " [ESTOQUE BAIXO]" if self.estoque_baixo() else ""

        return (
            f"Cód.: {self._codigo} | {self._nome} ({self._categoria}) | "
            f"R$ {self._preco:.2f} | Qtd.: {self._quantidade} | "
            f"Total: R$ {self.valor_em_estoque():.2f}{aviso}"
        )


if __name__ == "__main__":
    p1 = Produto("Pão francês", 0.75, 200, "Pães")

    print(p1)
    print("Preço inválido aceito?", p1.set_preco(-2))
    print("Reposição aceita?", p1.adicionar_estoque(10))
    print("Remoção aceita?", p1.remover_estoque(5))
    print(p1)
