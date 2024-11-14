import csv

class Node():
    def __init__(self, curso, ppc, periodo, codigo, nome, ch, professores: list):
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


def logicalXOR(a, b, condition):
    # return (a and not b) or (not a and b)
    return ((a == condition and b != condition) or (a != condition and b == condition))


def classificarDf(caminhoCsv: str) -> list:
    # Lê os dados do CSV
    with open(caminhoCsv, encoding="utf-8") as arquivo:
        df = csv.reader(arquivo)

        # Pula o cabeçalho
        next(df)

        nos = []

        for linha in df:
            # Adiciona os professores em uma lista para colocar nos nós
            professores = []
            for i in range(6, len(linha), 1):
                if linha[i] == '1':
                    professores.append(i-5)
            
            # coloca as disciplinas no modelo Node
            # nos.append(Node(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], professores))

            # Pra cada CH, coloca uma cópia da disciplina
            # for cloneNum in range(int(linha[5])):
            #     nos.append(Node(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], professores))
            
            # Divide as disciplinas conforme necessário para a tabela de horários
            if linha[5] == '5':
                nos.append(Node(linha[0], linha[1], linha[2], linha[3], linha[4], 3, professores))
                nos.append(Node(linha[0], linha[1], linha[2], linha[3], linha[4], 2, professores))
            elif linha[5] == '4':
                nos.append(Node(linha[0], linha[1], linha[2], linha[3], linha[4], 2, professores))
                nos.append(Node(linha[0], linha[1], linha[2], linha[3], linha[4], 2, professores))
            else:
                nos.append(Node(linha[0], linha[1], linha[2], linha[3], linha[4], int(linha[5]), professores))

        return nos


def criarListaAdjacencia(nos: list) -> dict:
    listaAdjacencia = {}

    for i in range(len(nos)):

        arestas = set()

        for j in range(0, len(nos)):

            if i == j:
                continue

            # nao há porque permitir que nos com cargas horarias diferentes se conectem, ja que vao ser colocados em blocos diferentes de qualquer forma
            if nos[i].ch != nos[j].ch:
                continue

            # se um dos cursos for sistemas e o outro nao for, nao precisa fazer as conexoes, ja que um é a noite e o outro nao
            if logicalXOR(nos[i].curso, nos[j].curso, 'SIN'):
                #print(nos[i].curso, nos[j].curso)
                continue
            
            if nos[i].turma == nos[j].turma:
                arestas.add(j)

            for p in nos[i].professores:
                if p in nos[j].professores:
                    arestas.add(j)

        listaAdjacencia[i] = arestas

    return listaAdjacencia



def colorirGrafo(nos: list, listaAdjacencia: dict) -> int:
    # Número de cores usadas até agora
    cores = 0

    # Para cada nó, vamos tentar colori-lo
    for i in range(len(nos)):

        # Lista de cores que não podem ser usadas
        coresBloqueadas = []

        # Para cada aresta, adiciona sua cor à lista de cores bloqueadas
        for aresta in listaAdjacencia[i]:
            
            if nos[aresta].cor != None:

                coresBloqueadas.append(nos[aresta].cor)

        # Inicializa corFinal como -1 para buscar uma cor disponível
        corFinal = -1

        # Procura uma cor que não esteja na lista de cores bloqueadas
        for cor in range(cores):

            if cor not in coresBloqueadas:

                corFinal = cor
                break

        # Se nenhuma cor disponível foi encontrada, cria uma nova cor
        if corFinal == -1:
            corFinal = cores
            cores += 1
        
        # Atribui a cor ao nó
        nos[i].cor = corFinal

    return cores


def criarGrafoTurmas(nos: list) -> dict:

    grafoTurmas = {}

    for i in range(len(nos)):
        arestas = set()

        for j in range(len(nos)):

            if i == j:
                continue

            if nos[i].turma == nos[j].turma:
                arestas.add(j)
        
        grafoTurmas [i] = arestas

    return grafoTurmas 


def fazerDivisaoHorario(nos: list):
    # Primeiro passo: Criar os horarios
    horarios = [{}, {}, {}, {}, {}]
    for i in range(5):
        horarios[i] = {'M123': None, 'M45': None, 'T12': None, 'T345': None, 'N12': None, 'N345': None}
    
    # se separar uma cor para cada horario, podemos simplesmente conectar as disciplinas a suas respectivas cores
    for i in range(len(nos)):

        sucesso = False

        # curso de sistemas sempre é à noite
        if nos[i].curso == 'SIN':

            for dia in range(5):
                
                if nos[i].ch == 3:
                    if horarios[dia]['N345'] == None or horarios[dia]['N345'] == nos[i].cor:
                        horarios[dia]['N345'] = nos[i].cor
                        sucesso = True
                
                else:
                    if horarios[dia]['N12'] == None or horarios[dia]['N12'] == nos[i].cor:
                        horarios[dia]['N12'] = nos[i].cor
                        sucesso = True
                
                if sucesso:
                    break
            
            # se nao tiver tido sucesso ainda, teremos que pegar um horario de 3 para uma disciplina de 2
            if not sucesso:

                for dia in range(5):
                    if horarios[dia]['N345'] == None or horarios[dia]['N345'] == nos[i].cor:
                        horarios[dia]['N345'] = nos[i].cor
                        sucesso = True
                
                    if sucesso:
                        break
                    
        
        # outros cursos conseguem horarios de dia ou de tarde
        else:
            for dia in range(5):
                
                if nos[i].ch == 3:
                    if horarios[dia]['T345'] == None or horarios[dia]['T345'] == nos[i].cor:
                        horarios[dia]['T345'] = nos[i].cor
                        sucesso = True

                    elif horarios[dia]['M123'] == None or horarios[dia]['M123'] == nos[i].cor:
                        horarios[dia]['M123'] = nos[i].cor
                        sucesso = True

                else:
                    if horarios[dia]['T12'] == None or horarios[dia]['T12'] == nos[i].cor:
                        horarios[dia]['T12'] = nos[i].cor
                        sucesso = True

                    elif horarios[dia]['M45'] == None or horarios[dia]['M45'] == nos[i].cor:
                        horarios[dia]['M45'] = nos[i].cor
                        sucesso = True

                if sucesso:
                    break

            # se nao tiver tido sucesso ainda, teremos que pegar um horario de 3 para uma disciplina de 2
            if not sucesso:

                for dia in range(5):
                    if horarios[dia]['T345'] == None or horarios[dia]['T345'] == nos[i].cor:
                        horarios[dia]['T345'] = nos[i].cor
                        sucesso = True

                    elif horarios[dia]['M123'] == None or horarios[dia]['M123'] == nos[i].cor:
                        horarios[dia]['M123'] = nos[i].cor
                        sucesso = True
                
                    if sucesso:
                        break
        
        # debug pra quando uma dissciplina não tiver horario disponivel
        if not sucesso:
            print('Horario nao adicionado : ' + nos[i].nome, nos[i].curso, nos[i].cor, nos[i].ch)
        
    return horarios
                

if __name__ == "__main__":
    nos = classificarDf("..\\datasets\\csv\\semestre2.csv")
    # arestas = fazerArestas(nos)
    arestas = criarListaAdjacencia(nos)

    # print(arestas)

    print(colorirGrafo(nos, arestas))

    # grafoPorTurmas = criarGrafoTurmas(nos)

    horarios = fazerDivisaoHorario(nos)

    print(horarios)



