class Produto:
    proximo_codigo = 1

    def __init__(self, nome, preco, quantidade=0, categoria="Geral"):
        self._codigo = Produto.proximo_codigo
        Produto.proximo_codigo += 1
        self._nome = str(nome).strip()
        self._categoria = str(categoria).strip() if categoria else "Geral"
        self._preco = float(preco)
        self._quantidade = int(quantidade)

    # Getters
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

    # Setters e validacoes
    def set_nome(self, novo_nome):
        if not novo_nome or not str(novo_nome).strip():
            print("Erro: o nome nao pode ser vazio.")
            return False
        self._nome = str(novo_nome).strip()
        return True

    def set_categoria(self, nova_categoria):
        if not nova_categoria or not str(nova_categoria).strip():
            print("Erro: a categoria nao pode ser vazia.")
            return False
        self._categoria = str(nova_categoria).strip()
        return True

    def set_preco(self, novo_preco):
        if novo_preco <= 0:
            print("Erro: o preco deve ser maior que zero.")
            return False
        self._preco = float(novo_preco)
        return True

    def adicionar_estoque(self, quantidade):
        if quantidade <= 0:
            print("Erro: a quantidade para adicionar deve ser maior que zero.")
            return False
        self._quantidade += int(quantidade)
        return True

    def remover_estoque(self, quantidade):
        if quantidade <= 0:
            print("Erro: a quantidade para remover deve ser maior que zero.")
            return False
        if quantidade > self._quantidade:
            print(f"Erro: estoque insuficiente de {self._nome} (disponivel: {self._quantidade}).")
            return False
        self._quantidade -= int(quantidade)
        return True

    def valor_em_estoque(self):
        return self._preco * self._quantidade

    def estoque_baixo(self, limite=5):
        return self._quantidade < limite

    def __str__(self):
        aviso = " [ESTOQUE BAIXO]" if self.estoque_baixo() else ""
        return (
            f"Cod: {self._codigo} | {self._nome} ({self._categoria}) | "
            f"R$ {self._preco:.2f} | Qtd: {self._quantidade} | "
            f"Total: R$ {self.valor_em_estoque():.2f}{aviso}"
        )


# Teste rapido da classe Produto
if __name__ == "__main__":
    p1 = Produto("Pão Francês", 0.80, 50, "Padaria")
    p2 = Produto("Bolo de Cenoura", 25.00, 3, "Confeitaria")

    print(p1)
    print(p2)

    p1.set_preco(-2.0)  # deve dar erro
    p1.set_preco(0.95)

    p1.adicionar_estoque(10)
    p1.remover_estoque(100)  # deve dar erro de falta de estoque
    p1.remover_estoque(15)

    print("Depois das alteracoes:")
    print(p1)
    print("Valor em estoque p1:", p1.valor_em_estoque())
    print("Estoque baixo p2?", p2.estoque_baixo())
