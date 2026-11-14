
import unittest

from padaria import Padaria


class TestesPadaria(unittest.TestCase):

    def setUp(self):
        self.padaria = Padaria("Padaria Pão Quente")

        self.padaria.cadastrar_produto(
            "Pão francês", 0.75, 200, "Pães"
        )
        self.padaria.cadastrar_produto(
            "Pão de queijo", 4.50, 60, "Salgados"
        )
        self.padaria.cadastrar_produto(
            "Bolo de cenoura", 28.00, 6, "Doces"
        )

        self.codigo_pao = self.padaria.get_produtos()[0].get_codigo()
        self.codigo_queijo = self.padaria.get_produtos()[1].get_codigo()
        self.codigo_bolo = self.padaria.get_produtos()[2].get_codigo()

    # T01 - Cadastro de produto válido
    def test_T01_cadastrar_produto(self):
        resultado = self.padaria.cadastrar_produto(
            "Café", 5.00, 30, "Bebidas"
        )
        self.assertIn("OK", resultado)
        self.assertEqual(
            self.padaria.get_quantidade_de_produtos(), 4
        )

    # T02 - Impedir cadastro com nome vazio
    def test_T02_nome_vazio(self):
        resultado = self.padaria.cadastrar_produto(
            "", 5.00, 10, "Bebidas"
        )
        self.assertIn("ERRO", resultado)

    # T03 - Impedir produto duplicado
    def test_T03_produto_duplicado(self):
        resultado = self.padaria.cadastrar_produto(
            "Pão francês", 1.00, 10, "Pães"
        )
        self.assertIn("ERRO", resultado)

    # T04 - Impedir preço ou quantidade inválidos
    def test_T04_dados_invalidos(self):
        preco = self.padaria.cadastrar_produto(
            "Produto A", -2, 10, "Geral"
        )
        quantidade = self.padaria.cadastrar_produto(
            "Produto B", 2.00, -5, "Geral"
        )

        self.assertIn("ERRO", preco)
        self.assertIn("ERRO", quantidade)

    # T05 - Venda recusada por estoque insuficiente
    def test_T05_estoque_insuficiente(self):
        resultado = self.padaria.registrar_venda(
            self.codigo_bolo, 10, 4
        )
        self.assertIn("estoque insuficiente", resultado)

    # T06 - Registrar venda válida
    def test_T06_venda_valida(self):
        resultado = self.padaria.registrar_venda(
            self.codigo_pao, 10, 4
        )

        produto = self.padaria.buscar_por_codigo(self.codigo_pao)

        self.assertIn("OK", resultado)
        self.assertEqual(produto.get_quantidade(), 190)
        self.assertEqual(
            self.padaria.get_vendas(0, 4), 10
        )

    # T07 - Impedir dia inválido
    def test_T07_dia_invalido(self):
        resultado = self.padaria.registrar_venda(
            self.codigo_pao, 1, 8
        )
        self.assertIn("ERRO", resultado)

    # T08 - Impedir código inexistente
    def test_T08_codigo_inexistente(self):
        resultado = self.padaria.registrar_venda(
            9999, 1, 1
        )
        self.assertIn("não encontrado", resultado)

    # T09 - Impedir quantidade inválida na venda
    def test_T09_quantidade_invalida(self):
        resultado = self.padaria.registrar_venda(
            self.codigo_pao, 0, 1
        )
        self.assertIn("ERRO", resultado)

    # T10 - Reposição de estoque
    def test_T10_repor_estoque(self):
        resultado = self.padaria.repor_estoque(
            self.codigo_bolo, 12
        )

        produto = self.padaria.buscar_por_codigo(self.codigo_bolo)

        self.assertIn("OK", resultado)
        self.assertEqual(produto.get_quantidade(), 18)

    # T11 - Impedir alteração para preço negativo
    def test_T11_preco_invalido(self):
        resultado = self.padaria.alterar_preco(
            self.codigo_pao, -2
        )
        self.assertIn("ERRO", resultado)

    # T12 - Busca por parte do nome
    def test_T12_busca_por_nome(self):
        encontrados = self.padaria.buscar_por_nome("pão")

        self.assertEqual(len(encontrados), 2)

    # T13 - Identificar produtos com estoque baixo
    def test_T13_estoque_baixo(self):
        self.padaria.buscar_por_codigo(
            self.codigo_bolo
        ).remover_estoque(2)

        produtos = self.padaria.produtos_com_estoque_baixo()

        self.assertIn(
            self.codigo_bolo,
            [p.get_codigo() for p in produtos]
        )

    # T14 - Conferir matriz de vendas e faturamento
    def test_T14_relatorio_vendas(self):
        self.padaria.registrar_venda(
            self.codigo_pao, 10, 4
        )
        self.padaria.registrar_venda(
            self.codigo_queijo, 2, 4
        )

        self.assertEqual(
            self.padaria.get_vendas(0, 4), 10
        )
        self.assertEqual(
            self.padaria.get_vendas(1, 4), 2
        )
        self.assertAlmostEqual(
            self.padaria.get_faturamento_do_dia(4),
            16.50
        )

    # T15 - Conferir fechamento, estoque e histórico
    def test_T15_fechamento(self):
        self.padaria.registrar_venda(
            self.codigo_pao, 10, 1
        )

        self.assertAlmostEqual(
            self.padaria.get_faturamento_total(),
            7.50
        )

        self.assertEqual(
            self.padaria.get_produtos()[0].get_quantidade(),
            190
        )

        self.assertGreater(
            len(self.padaria.get_historico()), 0
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
