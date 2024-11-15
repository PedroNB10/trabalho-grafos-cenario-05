class Disciplina():
    def __init__(self, index: int , curso: str, ppc: str, periodo: str, codigo: str, nome: str, ch: int, professores: list[int]):
        self.index = index
        self.codigo = codigo
        self.nome = nome
        self.curso = curso
        self.ppc = ppc
        self.periodo = periodo
        self.ch = ch
        self.professores = professores

        self.turma = curso + '-' + ppc + '.' + str(periodo)
        self.cor = None 
        self.horario = None