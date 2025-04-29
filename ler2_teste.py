import unittest
from unittest import mock
from datetime import datetime, timedelta
import struct
import logging
from ler2 import dados, ler_dados
from excecoes import IdadeInvalida, GeneroInvalido, DadosInvalidos

class TestIMC(unittest.TestCase):
    def setUp(self):
        self.hoje = datetime.now()
        self.data_6_anos = (self.hoje - timedelta(days=6*365)).strftime("%Y-%m-%d")
        self.data_7_anos = (self.hoje - timedelta(days=7*365)).strftime("%Y-%m-%d")
        self.data_8_anos = (self.hoje - timedelta(days=8*365)).strftime("%Y-%m-%d")
    
    # Testes básicos
    def test_menina_idade_6(self):
        self.assertEqual(dados("Ana", self.data_6_anos, "Femi", 14, 1.1).getTarget(), 0)

    def test_menina_idade_7(self):
        self.assertEqual(dados("Lia", self.data_7_anos, "Femi", 17, 1.1).getTarget(), 0)

    def test_menina_idade_8(self):
        self.assertEqual(dados("Bia", self.data_8_anos, "Femi", 21, 1.2).getTarget(), 0)

    def test_menino_idade_6(self):
        self.assertEqual(dados("João", self.data_6_anos, "Masc", 18, 1.1).getTarget(), 1)

    def test_menino_idade_7(self):
        self.assertEqual(dados("Lucas", self.data_7_anos, "Masc", 16, 1.1).getTarget(), 0)

    def test_menino_idade_8(self):
        self.assertEqual(dados("Pedro", self.data_8_anos, "Masc", 17, 1.1).getTarget(), 0)

    # Testes de limites
    def test_limites_menino_6(self):
        self.assertEqual(dados("M6", self.data_6_anos, "Masc", 14.49, 1.0).getTarget(), 0)
        self.assertEqual(dados("M6", self.data_6_anos, "Masc", 14.5, 1.0).getTarget(), 1)
        self.assertEqual(dados("M6", self.data_6_anos, "Masc", 16.69, 1.0).getTarget(), 1)
        self.assertEqual(dados("M6", self.data_6_anos, "Masc", 16.7, 1.0).getTarget(), 2)
        self.assertEqual(dados("M6", self.data_6_anos, "Masc", 17.99, 1.0).getTarget(), 2)
        self.assertEqual(dados("M6", self.data_6_anos, "Masc", 18.0, 1.0).getTarget(), 3)

    # Testes de exceções
    def test_idade_invalida(self):
        with self.assertRaises(IdadeInvalida):
            dados("Velho", "2000-01-01", "Masc", 70, 1.7).getTarget()

    def test_genero_invalido(self):
        with self.assertRaises(GeneroInvalido):
            dados("Inv", self.data_7_anos, "Outro", 20, 1.2).getTarget()

    def test_dados_invalidos(self):
        with self.assertRaises(DadosInvalidos):
            dados("", self.data_7_anos, "Masc", 20, 1.2)
        with self.assertRaises(DadosInvalidos):
            dados("Inv", "data-invalida", "Masc", 20, 1.2)
        with self.assertRaises(DadosInvalidos):
            dados("Inv", self.data_7_anos, "Masc", -1, 1.2)
        with self.assertRaises(DadosInvalidos):
            dados("Inv", self.data_7_anos, "Masc", 20, 0)

    # Testes adicionais para cobertura
    def test_validacao_dados_nome_vazio(self):
        with self.assertRaises(DadosInvalidos):
            dados(" ", "2018-01-01", "Masc", 20, 1.2)

    def test_validacao_peso_negativo(self):
        with self.assertRaises(DadosInvalidos):
            dados("Teste", "2018-01-01", "Masc", -1, 1.2)

    # Testes de métodos
    def test_calc_idade(self):
        p = dados("Teste", self.data_7_anos, "Masc", 20, 1.2)
        self.assertEqual(p.calcIdade(), 7)

    def test_str_completo(self):
        p = dados("Maria", self.data_7_anos, "Femi", 17, 1.1)
        output = str(p)
        self.assertIn("Nome: Maria", output)
        self.assertIn("Gênero: Femi", output)
        self.assertIn("Idade: 7", output)

    def test_str_com_erro(self):
        with self.assertRaises(DadosInvalidos):
            p = dados("Erro", "data-invalida", "Masc", 20, 1.2)
            str(p)

    # Testes da função ler_dados
    def test_ler_dados_com_erro(self):
        with mock.patch('builtins.open', mock.mock_open(read_data=b'invalid')):
            with self.assertLogs(level='ERROR'):
                ler_dados('dados.bin')

    def test_ler_dados_valido(self):
        record = struct.pack('30s 11s 4s f f i', 
                           b'Joao', b'2018-01-01', b'Masc', 20.0, 1.2, 1)
        with mock.patch('builtins.open', mock.mock_open(read_data=record)):
            with self.assertLogs(level='INFO'):
                ler_dados('dados.bin')

    def test_ler_dados_arquivo_inexistente(self):
        with mock.patch('builtins.open', side_effect=FileNotFoundError):
            with self.assertLogs(level='ERROR'):
                ler_dados('inexistente.bin')

    # Teste do bloco principal (opcional)
    @unittest.skip("Teste opcional do bloco main")
    def test_main_block(self):
        with mock.patch('ler2.ler_dados') as mock_ler:
            with mock.patch('ler2.__name__', '__main__'):
                import ler2
                mock_ler.assert_called_once_with('dados.bin')

if __name__ == '__main__':
    unittest.main()