import copy
from produto import Produto


class Padaria:
    MAX_PRODUTOS = 20

    def __init__(self, nome="Padaria"):
        self._nome = nome
        self._produtos = []

    def cadastrar_produto(self, nome, preco, quantidade=0, categoria="Geral"):
        # RN01 - Limite maximo de produtos
        if len(self._produtos) >= Padaria.MAX_PRODUTOS:
            print(f"Erro (RN01): limite maximo de {Padaria.MAX_PRODUTOS} produtos atingido.")
            return False

        # RN02 - Nome obrigatorio e unico
        if not nome or not str(nome).strip():
            print("Erro (RN02): o nome do produto nao pode ser vazio.")
            return False

        nome_limpo = str(nome).strip()
        for p in self._produtos:
            if p.get_nome().lower() == nome_limpo.lower():
                print(f"Erro (RN02): ja existe um produto cadastrado com o nome '{nome_limpo}'.")
                return False

        # RN03 - Preco maior que zero
        if preco <= 0:
            print("Erro (RN03): o preco do produto deve ser maior que zero.")
            return False

        # RN04 - Quantidade inicial nao pode ser negativa
        if quantidade < 0:
            print("Erro (RN04): a quantidade inicial nao pode ser negativa.")
            return False

        novo = Produto(nome_limpo, preco, quantidade, categoria)
        self._produtos.append(novo)
        return True

    def buscar_por_codigo(self, codigo):
        for p in self._produtos:
            if p.get_codigo() == codigo:
                return p
        return None

    def buscar_por_nome(self, termo):
        if not termo:
            return []
        termo_busca = str(termo).strip().lower()
        resultado = []
        for p in self._produtos:
            if termo_busca in p.get_nome().lower():
                resultado.append(p)
        return resultado

    def get_produtos(self):
        # Retorna copia para nao alterar a lista original por fora
        return copy.copy(self._produtos)
