class IdadeInvalida(Exception):
    """Exceção lançada quando a idade não está entre 6 e 8 anos"""
    pass

class GeneroInvalido(Exception):
    """Exceção lançada quando o gênero não é 'Masc' ou 'Femi'"""
    pass

class DadosInvalidos(Exception):
    """Exceção lançada quando os dados de entrada são inválidos"""
    pass
