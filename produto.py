class Produto:
    """Representa um produto da padaria e protege seus dados por meio de métodos."""

    proximo_codigo = 1

    def __init__(self, nome, preco, quantidade=0, categoria="Geral"):
        self._codigo = Produto.proximo_codigo
        Produto.proximo_codigo += 1

        self._nome = str(nome).strip()
        self._categoria = str(categoria).strip() if categoria and str(categoria).strip() else "Sem categoria"
        self._preco = float(preco) if isinstance(preco, (int, float)) and not isinstance(preco, bool) and preco > 0 else 0.0
        self._quantidade = int(quantidade) if isinstance(quantidade, int) and not isinstance(quantidade, bool) and quantidade >= 0 else 0

    # Getters: permitem consultar os atributos sem alterá-los diretamente.
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
        if (not isinstance(novo_preco, (int, float))
                or isinstance(novo_preco, bool)
                or novo_preco <= 0):
            return False
        self._preco = float(novo_preco)
        return True

    def adicionar_estoque(self, quantidade):
        if (not isinstance(quantidade, int)
                or isinstance(quantidade, bool)
                or quantidade <= 0):
            return False
        self._quantidade += quantidade
        return True

    def remover_estoque(self, quantidade):
        if (not isinstance(quantidade, int)
                or isinstance(quantidade, bool)
                or quantidade <= 0
                or quantidade > self._quantidade):
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
    # Teste isolado da classe Produto.
    p1 = Produto("Pão francês", 0.75, 200, "Pães")
    print(p1)
    print("Preço inválido aceito?", p1.set_preco(-2))
    print("Reposição aceita?", p1.adicionar_estoque(10))
    print("Remoção aceita?", p1.remover_estoque(5))
    print(p1)
