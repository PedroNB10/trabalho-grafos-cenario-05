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

        self.turma = curso + '-' + ppc + '.' + str(periodo)
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
                if row[i] == '1':
                    professores.append(i-5)
            
            # coloca as disciplinas no modelo Node
            # nodes.append(Node(row[0], row[1], row[2], row[3], row[4], row[5], professores))

            # Pra cada ch, coloca uma cópia da disciplina
            for cloneNum in range(int(row[5])):
                nodes.append(Node(row[0], row[1], row[2], row[3], row[4], row[5], professores))

        
        return nodes

def fazerArestas(nodes: list) -> list:
    matrizArestas = [[0] * len(nodes)] * len(nodes)
    #print(matrizArestas)

    # criar arestas
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes), 1):

            print(nodes[i].nome, nodes[j].nome)

            # professor
            for p in nodes[i].professores:
                if p in nodes[j].professores:
                    matrizArestas[i][j] += 1
                    matrizArestas[j][i] += 1
                    print("Professor igual")
            
            # turmas
            if nodes[i].turma == nodes[j].turma:
                matrizArestas[i][j] += 1
                matrizArestas[j][i] += 1
                print("Turma igual")


    return matrizArestas

def fazerListaAdj(nodes: list) -> dict:

    listaAdj = {}

    for i in range(len(nodes)):

        arestas = set()

        for j in range(0, len(nodes)):

            if i == j:
                continue
            

            if nodes[i].turma == nodes[j].turma:
                arestas.add(j)

            for p in nodes[i].professores:
                if p in nodes[j].professores:
                    arestas.add(j)


        listaAdj[i] = arestas

    
    return listaAdj



def colorirGrafo(nodes: list, listaAdj: dict) -> int:
    # numero de cores ate agora registradas
    cores = 0

    # Pra cada node, vamos tentar colori-lo
    for i in range(len(nodes)):

        # listaCores representa as  cores que não podem ser usadas
        listaCores = []

        # Pra cada aresta encontrada, vamos adicionar sua cor na lista de cores bloqueadas
        for aresta in listaAdj[i]:
            
            if nodes[aresta].cor != None:

                listaCores.append(nodes[aresta].cor)

        # agora colocamos a cor Final como -1 para fazer um teste
        corFinal = -1

        # começando da primeira cor criada, vamos procurar uma cor que não seja bloqueada
        for cor in range(cores):

            if cor not in listaCores:

                corFinal = cor
                break

        # se nao achamos uma cor utilizavel, criamos uma nova cor
        if corFinal == -1:
            corFinal = cores
            cores += 1
        
        # por ultimo, pintamos o vertice
        nodes[i].cor = corFinal

    return cores


if __name__ == "__main__":
    nodes = classifyDF("cenario-5-semestre-2.csv")
    # arestas = fazerArestas(nodes)
    arestas = fazerListaAdj(nodes)

    # print(arestas)

    print(colorirGrafo(nodes, arestas))
    
    for i in range(len(nodes)):
        print(nodes[i].nome, nodes[i].cor)


    # # for i in range(len(nodes)):
    # #     print(nodes[i].nome, nodes[i].turma, nodes[i].professores)

    # for i in range(len(nodes)):
    #     for j in range(len(nodes)):
    #         if arestas[i][j] > 1:
    #             # print(nodes[i].nome, nodes[j].nome, arestas[i][j], "-->", nodes[i].ch, nodes[j].ch)
    #             if nodes[i].nome == nodes[j].nome:
    #                 print(nodes[i].nome, nodes[i].turma, 'AND', nodes[j].turma, '+', nodes[i].professores, 'VS', nodes[j].professores)

    # for i in range(len(nodes)):
    #     print(arestas[i][i])

