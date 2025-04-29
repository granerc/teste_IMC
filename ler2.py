import struct
from datetime import datetime
import logging
from excecoes import IdadeInvalida, GeneroInvalido, DadosInvalidos

class dados:
    def __init__(self, nome: str, nasc: str, genero: str, peso: float, altura: float):
        try:
            self.nome = nome.strip()
            self.nasc = nasc.strip()
            self.genero = genero.strip()
            self.peso = float(peso)
            self.altura = float(altura)
            
            if not self.nome:
                raise DadosInvalidos("Nome não pode ser vazio")
            datetime.strptime(self.nasc, "%Y-%m-%d")  # Valida formato da data
            if self.genero not in ['Masc', 'Femi']:
                raise GeneroInvalido("Gênero deve ser 'Masc' ou 'Femi'")
            if self.peso <= 0 or self.altura <= 0:
                raise DadosInvalidos("Peso e altura devem ser positivos")
        except ValueError as e:
            raise DadosInvalidos(f"Dados inválidos: {str(e)}")
    
    def calcIdade(self) -> int:
        n = datetime.strptime(self.nasc, "%Y-%m-%d")
        return (datetime.now() - n).days // 365

    def getTarget(self) -> int:
        idade = self.calcIdade()
        if idade not in [6, 7, 8]:
            raise IdadeInvalida("A idade deve ser entre 6 e 8 anos")
        
        try:
            imc = self.peso / (self.altura ** 2)
        except ZeroDivisionError:
            raise DadosInvalidos("Altura não pode ser zero")

        tabela_imc = {
            'Masc': {
                6: [(14.5, 0), (16.7, 1), (18.0, 2), (float('inf'), 3)],
                7: [(15.0, 0), (17.4, 1), (19.1, 2), (float('inf'), 3)],
                8: [(15.6, 0), (16.8, 1), (20.3, 2), (float('inf'), 3)]
            },
            'Femi': {
                6: [(14.3, 0), (16.2, 1), (17.4, 2), (float('inf'), 3)],
                7: [(14.9, 0), (17.2, 1), (18.9, 2), (float('inf'), 3)],
                8: [(15.6, 0), (18.2, 1), (20.3, 2), (float('inf'), 3)]
            }
        }
        
        for limite, valor in tabela_imc[self.genero][idade]:
            if imc < limite:
                return valor

    def __str__(self) -> str:
        try:
            idade = self.calcIdade()
            target = self.getTarget()
            interpretacao = ["Abaixo do peso", "Peso normal", "Sobrepeso", "Obesidade"][target]
        except Exception as e:
            interpretacao = f"Erro: {str(e)}"
        
        return f"""Nome: {self.nome}
Data de Nascimento: {self.nasc}
Gênero: {self.genero}
Idade: {self.calcIdade()}
Peso: {self.peso:.2f} Kg
Altura: {self.altura:.2f} m
Interpretação IMC: {interpretacao}"""

def ler_dados(arq: str) -> None:
    logging.info(f"Iniciando leitura do arquivo {arq}")
    form = '30s 11s 4s f f i'
    tam = struct.calcsize(form)

    try:
        with open(arq, 'rb') as f:
            while True:
                record_data = f.read(tam)
                if not record_data:
                    break
                try:
                    record = struct.unpack(form, record_data)
                    string1 = record[0].decode().strip('\x00')
                    string2 = record[1].decode().strip('\x00')
                    string3 = record[2].decode().strip('\x00')
                    float1 = record[3]
                    float2 = record[4]
                    integer = record[5]
                    dado = dados(string1, string2, string3, float1, float2)
                    print(dado)
                    print("-" * 40)
                except Exception as e:
                    logging.error(f"Erro ao processar registro: {str(e)}")
                    print("-" * 40)
    except FileNotFoundError:
        logging.error(f"Arquivo {arq} não encontrado")
    except Exception as e:
        logging.error(f"Erro inesperado: {str(e)}")

if __name__ == '__main__':
    ler_dados('dados.bin')