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
    matrizArestas = [[0] * len(nodes)] * len(nodes)

    # criar arestas
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes), 1):

            # professor
            for p in nodes[i].professores:
                if p in nodes[j].professores:
                    matrizArestas[i][j] += 1
                    matrizArestas[j][i] += 1
            
            # turmas
            if nodes[i].turma == nodes[j].turma:
                matrizArestas[i][j] += 1
                matrizArestas[j][i] += 1


    return matrizArestas
    




if __name__ == "__main__":
    nodes = classifyDF("cenario-5-semestre-2.csv")
    arestas = fazerArestas(nodes)

    print(arestas)
