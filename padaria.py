        )

    def repor_estoque(self, codigo, unidades):
        indice = self._indice_do_produto(codigo)
        if indice == -1:
            return f"ERRO: produto de código {codigo} não encontrado."

        if not self._quantidade_inteira_positiva(unidades):
            return "ERRO: a quantidade para reposição deve ser maior que zero."

        produto = self._produtos[indice]
        produto.adicionar_estoque(unidades)
        self._registrar_no_historico(
            f"Reposição: {unidades} unidade(s) de {produto.get_nome()}"
        )
        return (
            f"OK: estoque de {produto.get_nome()} agora é "
            f"{produto.get_quantidade()}."
        )

    def alterar_preco(self, codigo, novo_preco):
        indice = self._indice_do_produto(codigo)
        if indice == -1:
            return f"ERRO: produto de código {codigo} não encontrado."

        if not self._numero_positivo(novo_preco):
            return "ERRO: o preço deve ser maior que zero."

        produto = self._produtos[indice]
        produto.set_preco(novo_preco)
        self._registrar_no_historico(
            f"Alteração de preço: {produto.get_nome()} "
            f"para R$ {float(novo_preco):.2f}"
        )
        return f"OK: preço de {produto.get_nome()} alterado para R$ {float(novo_preco):.2f}."

    def get_vendas(self, posicao_produto, dia):
        """Retorna uma célula da matriz; posição do produto começa em zero."""
        if (not isinstance(posicao_produto, int)
                or isinstance(posicao_produto, bool)
                or not 0 <= posicao_produto < len(self._produtos)
                or not self._dia_valido(dia)):
            return 0
        return self._vendas[posicao_produto][dia - 1]

    def total_vendido_do_produto(self, posicao_produto):
        """Soma uma linha da matriz (todas as vendas de um produto)."""
        if (not isinstance(posicao_produto, int)
                or isinstance(posicao_produto, bool)
                or not 0 <= posicao_produto < len(self._produtos)):
            return 0
        return sum(self._vendas[posicao_produto])

    def total_vendido_no_dia(self, dia):
        """Soma uma coluna da matriz (vendas de todos os produtos no dia)."""
        if not self._dia_valido(dia):
            return 0
        coluna = dia - 1
        return sum(linha[coluna] for linha in self._vendas[:len(self._produtos)])

    def get_faturamento_do_dia(self, dia):
        if not self._dia_valido(dia):
            return 0.0
        return self._faturamento_por_dia[dia - 1]

    def get_faturamento_total(self):
        return sum(self._faturamento_por_dia)

    def produto_mais_vendido(self):
        """Retorna o Produto com maior total semanal; None se não houve vendas."""
        if not self._produtos:
            return None
        totais = [
            self.total_vendido_do_produto(i)
            for i in range(len(self._produtos))
        ]
        maior = max(totais, default=0)
        if maior == 0:
            return None
        return self._produtos[totais.index(maior)]

    def dia_de_maior_faturamento(self):
        """Retorna o dia de 1 a 7; retorna 0 se ainda não houve faturamento."""
        maior = max(self._faturamento_por_dia, default=0.0)
        if maior <= 0:
            return 0
        return self._faturamento_por_dia.index(maior) + 1

    def produtos_com_estoque_baixo(self):
        return [
            produto for produto in self._produtos
            if produto.estoque_baixo(self.LIMITE_ESTOQUE_BAIXO)
        ]

    def valor_total_em_estoque(self):
        return sum(produto.valor_em_estoque() for produto in self._produtos)

    def get_historico(self):
        return self._historico.copy()

    # Métodos extras de leitura para facilitar os relatórios da Pessoa 3.
    def get_dias(self):
        return self.DIAS

    def get_matriz_vendas(self):
        """Devolve uma cópia das linhas utilizadas da matriz."""
        return [linha.copy() for linha in self._vendas[:len(self._produtos)]]
