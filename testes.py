"""Testes automatizados correspondentes aos cenários T01 a T15 da seção 9.

Execute na pasta do projeto com: python -m unittest -v testes.py
"""

import contextlib
import io
import unittest
from unittest.mock import patch

import main
import relatorio
from padaria import Padaria
from produto import Produto


class TestesSecao9(unittest.TestCase):
    def setUp(self):
        # Os códigos são sequenciais durante a execução real. Reiniciamos apenas
        # entre cenários isolados para que cada teste comece com códigos 1 a 5.
        Produto._proximo_codigo = 1
        self.padaria = Padaria("Padaria Pão Quente")
        main.carregar_dados_iniciais(self.padaria)

    def test_T01_listar_estoque_inicial(self):
        saida = io.StringIO()
        with contextlib.redirect_stdout(saida):
            relatorio.imprimir_estoque(self.padaria)
        self.assertIn("Pão francês", saida.getvalue())
        self.assertIn("R$ 454,50", saida.getvalue())
        self.assertEqual(self.padaria.get_quantidade_de_produtos(), 5)

    def test_T02_cadastrar_produto_e_tratar_preco_digitado_invalido(self):
        with patch("builtins.input", side_effect=["abc", "3,50"]):
            saida = io.StringIO()
            with contextlib.redirect_stdout(saida):
                preco = main.ler_decimal("Preço: ")
        self.assertEqual(preco, 3.5)
        self.assertIn("Valor inválido", saida.getvalue())
        resposta = self.padaria.cadastrar_produto("Broa de milho", preco, 40, "Pães")
        self.assertIn("OK:", resposta)
        self.assertIn("código 6", resposta)

    def test_T03_impedir_nome_duplicado_sem_diferenciar_maiusculas(self):
        resposta = self.padaria.cadastrar_produto("pão francês", 2.0, 10, "Pães")
        self.assertTrue(resposta.startswith("ERRO:"))

    def test_T04_impedir_preco_zero(self):
        resposta = self.padaria.cadastrar_produto("Rosca", 0, 10, "Pães")
        self.assertTrue(resposta.startswith("ERRO:"))

    def test_T05_rejeitar_venda_sem_estoque_e_sem_alterar_dados(self):
        estoque_antes = self.padaria.buscar_por_codigo(3).get_quantidade()
        faturamento_antes = self.padaria.get_faturamento_total()
        resposta = self.padaria.registrar_venda(3, 5, 4)
        self.assertIn("Disponível: 4", resposta)
        self.assertEqual(self.padaria.buscar_por_codigo(3).get_quantidade(), estoque_antes)
        self.assertEqual(self.padaria.get_faturamento_total(), faturamento_antes)

    def test_T06_registrar_venda_valida(self):
        resposta = self.padaria.registrar_venda(1, 10, 4)
        self.assertIn("OK:", resposta)
        self.assertIn("R$ 7,50", resposta)
        self.assertEqual(self.padaria.buscar_por_codigo(1).get_quantidade(), 10)

    def test_T07_rejeitar_dia_invalido(self):
        self.assertTrue(self.padaria.registrar_venda(2, 1, 8).startswith("ERRO:"))

    def test_T08_rejeitar_codigo_inexistente(self):
        self.assertTrue(self.padaria.registrar_venda(99, 1, 1).startswith("ERRO:"))

    def test_T09_entrada_inteira_invalida_nao_encerrar_programa(self):
        with patch("builtins.input", side_effect=["x", "99"]):
            saida = io.StringIO()
            with contextlib.redirect_stdout(saida):
                valor = main.ler_inteiro("Opção: ")
        self.assertEqual(valor, 99)
        self.assertIn("Valor inválido", saida.getvalue())

    def test_T10_repor_estoque(self):
        resposta = self.padaria.repor_estoque(3, 12)
        self.assertIn("OK:", resposta)
        self.assertEqual(self.padaria.buscar_por_codigo(3).get_quantidade(), 16)

    def test_T11_impedir_preco_negativo(self):
        self.assertTrue(self.padaria.alterar_preco(1, -2).startswith("ERRO:"))

    def test_T12_buscar_por_nome_parcial(self):
        encontrados = self.padaria.buscar_por_nome("pão")
        self.assertEqual([p.get_nome() for p in encontrados],
                         ["Pão francês", "Pão de queijo"])

    def test_T13_relatorio_sem_estoque_baixo_apos_reposicao(self):
        self.padaria.repor_estoque(3, 12)
        self.assertEqual(self.padaria.produtos_com_estoque_baixo(), [])

    def test_T14_relatorio_matriz_apos_venda_adicional(self):
        self.padaria.registrar_venda(1, 10, 4)
        total_unidades = sum(
            self.padaria.total_vendido_no_dia(dia) for dia in range(1, 8)
        )
        self.assertEqual(total_unidades, 292)
        self.assertEqual(self.padaria.total_vendido_no_dia(4), 10)
        saida = io.StringIO()
        with contextlib.redirect_stdout(saida):
            relatorio.imprimir_vendas_da_semana(self.padaria)
        self.assertIn("Total de unidades vendidas na semana: 292", saida.getvalue())

    def test_T15_fechamento_final_do_cenario_completo(self):
        # Reproduz as operações aceitas do roteiro T02-T14 na ordem da seção 9.
        self.padaria.cadastrar_produto("Broa de milho", 3.50, 40, "Pães")
        self.padaria.registrar_venda(1, 10, 4)
        self.padaria.repor_estoque(3, 12)
        self.assertAlmostEqual(self.padaria.get_faturamento_total(), 691.00)
        self.assertAlmostEqual(self.padaria.valor_total_em_estoque(), 923.00)
        saida = io.StringIO()
        with contextlib.redirect_stdout(saida):
            relatorio.imprimir_fechamento(self.padaria)
        self.assertIn("R$ 691,00", saida.getvalue())
        self.assertIn("R$ 923,00", saida.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
