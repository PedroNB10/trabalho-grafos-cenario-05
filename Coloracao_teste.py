import csv

class Node():
    def __init__(self, curso, ppc, periodo, cod, nome, ch, professores: list):
        self.cod = cod
        self.nome = nome
        self.curso = curso
        self.ppc = ppc
        self.periodo = periodo
        self.ch = ch
        self.professores = professores

        self.turma = curso + ppc + str(periodo)
        self.cor = None

    
    def setCor(self, cor):
        self.cor = cor

def classifyDF(csv_path: str) -> list:
    # le os dados
    with open(csv_path, encoding="utf-8") as file:
        df = csv.reader(file)

        # pula o cabecalho
        next(df)

        nodes = []

        for row in df:
            
            # adiciona os professores em uma lista para colocar nos nodes
            professores = []
            for i in range(6, len(row), 1):
                if row[i] == 1:
                    professores.append(i-5)
            
            # coloca as disciplinas no modelo Node
            nodes.append(Node(row[0], row[1], row[2], row[3], row[4], row[5], professores))

        
        return nodes

def fazerArestas(nodes: list) -> list:
    matrizAdj = []

    




if __name__ == "__main__":
    nodes = classifyDF("cenario-5-semestre-2.csv")

