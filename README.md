# Sistema de Análise de IMC Infantil

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Coverage](https://img.shields.io/badge/coverage-93%25-brightgreen)

Projeto para classificação de IMC conforme faixa etária e gênero, desenvolvido para a disciplina de Teste de Software.

## 📦 Arquivos Essenciais
teste-imc/
├── excecoes.py # Exceções personalizadas
├── ler2.py # Classe principal
├── ler2_teste.py # Testes automatizados
└── README.md # Este arquivo


## 🚀 Como Executar
```bash
# Instalar dependências (se necessário)
pip install coverage

# Executar testes
python ler2_teste.py

# Ver cobertura de testes
python -m coverage run -m unittest ler2_teste.py
python -m coverage report -m
