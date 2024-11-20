import csv
import os
import random
from classes.Disciplina import Disciplina

from collections import defaultdict

def logicalXOR(a, b, condition):
    # return (a and not b) or (not a and b)
    return ((a == condition and b != condition) or (a != condition and b == condition))


def carregarDisciplinasCsv(caminhoCsv: str) -> list[Disciplina]:
    # Obtém o caminho absoluto do arquivo CSV
    caminho_absoluto = os.path.abspath(caminhoCsv)

    # Lê os dados do CSV
    with open(caminho_absoluto, encoding="utf-8") as arquivo:
        df = csv.reader(arquivo)
        # Lê o cabeçalho para obter a quantidade de colunas
        cabecalho = next(df)
        TOTAL_COLUNAS_CABECALHO = len(cabecalho)

        nos = []
        indice = 0
        for linha in df:
            professores = []
            for i in range(6, TOTAL_COLUNAS_CABECALHO, 1): # a partir do 6 tem o Prof 1
                if linha[i] == '1': # significa que o professor ministra a disciplina
                    professores.append(i - 5)
        
            curso = linha[0]
            ppc = linha[1]
            periodo = linha[2]
            codigo_disciplina = linha[3]
            nome_disciplina = linha[4]
            ch = int(linha[5])

            
            if ch == 5:
                nos.append(Disciplina(indice, curso, ppc, periodo, codigo_disciplina, nome_disciplina, 3, professores))
                nos.append(Disciplina(indice + 1, curso, ppc, periodo, codigo_disciplina, nome_disciplina, 2, professores))
                indice += 2
            elif ch == 4:
                nos.append(Disciplina(indice, curso, ppc, periodo, codigo_disciplina, nome_disciplina, 2, professores))
                nos.append(Disciplina(indice + 1, curso, ppc, periodo, codigo_disciplina, nome_disciplina, 2, professores))
                indice += 2
            else:
                nos.append(Disciplina(indice, curso, ppc, periodo, codigo_disciplina, nome_disciplina, ch, professores))
                indice += 1

        return nos


def criarListaAdjacencia(nos: list[Disciplina]) -> dict[int, set[int]]:
    listaAdjacencia = {}

    for i in range(len(nos)):

        arestas = set()

        for j in range(len(nos)):

            if i == j:
                continue

            # nao há porque permitir que nos com cargas horarias diferentes se conectem, ja que vao ser colocados em blocos diferentes de qualquer forma
            # if nos[i].ch != nos[j].ch:
            #     continue

            # se um dos cursos for sistemas e o outro nao for, nao precisa fazer as conexoes, ja que um é a noite e o outro nao
            if logicalXOR(nos[i].curso, nos[j].curso, 'SIN'):
                arestas.add(j)
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

def criarGrafoProfessores(nos: list) -> dict:

    grafoProf = {}

    for i in range(len(nos)):
        arestas = set()

        for j in range(len(nos)):

            if i == j:
                continue
            
            for p in nos[i].professores:
                if p in nos[j].professores:
                    arestas.add(j)
        
        grafoProf [i] = arestas

    return grafoProf


def fazerDivisaoHorario(nos: list[Disciplina]):
    # Define uma semente fixa para os números aleatórios
    random.seed(42)

    # Primeiro passo: Criar os horarios, que são dicionários com os horarios de cada dia da semana
    horarios = [{}, {}, {}, {}, {}]
    for i in range(5):
        horarios[i] = {'M123': None, 'M45': None, 'T12': None, 'T345': None, 'N12': None, 'N345': None}

    
    # Segundo passo: Separar em listas de carga horaria 3 e 2
    ch3: list[Disciplina] = []
    ch2: list[Disciplina] = []
    for no in nos:
        if no.ch == 3:
            ch3.append(no)
        else:
            ch2.append(no)
    # Vamos usar o metodo shuffle para aleatoriezar um pouco a sequencia de horarios, evitando 5 horarios seguidos da mesma disciplina
    random.shuffle(ch3)
    random.shuffle(ch2)

    # Terceiro passo: Precisaremos checar se os professores estão trabalhando 6 horas ou menos por dia. Por isso, uma lista de horas trabalhadas por dia por professor pode ser util
    listaCHProfessor = []
    for i in range(18):
        listaCHProfessor.append({0: 0, # Seg
                                 1: 0, # Ter
                                 2: 0, # Qua
                                 3: 0, # Qui
                                 4: 0}) # Sex

    
    # Quarto passo: Se separar uma cor para cada horario, podemos simplesmente conectar as disciplinas a suas respectivas cores
    for i in range(len(ch3)):

        # Uma condição de loop é estabelecida para captar erros onde um horario não foi encontrado
        sucesso = False
        while not sucesso:

            for dia in range(5):

                if ch3[i].curso == 'SIN':
                    if (horarios[dia]['N345'] == None or horarios[dia]['N345'] == ch3[i].cor):
                        horarios[dia]['N345'] = ch3[i].cor
                        ch3[i].horario = 'N345'
                        sucesso = True
                
                else:
                    if horarios[dia]['T345'] == None or horarios[dia]['T345'] == ch3[i].cor:
                        horarios[dia]['T345'] = ch3[i].cor
                        ch3[i].horario = 'T345'
                        sucesso = True

                    elif horarios[dia]['M123'] == None or horarios[dia]['M123'] == ch3[i].cor:
                        horarios[dia]['M123'] = ch3[i].cor
                        ch3[i].horario = 'M123'
                        sucesso = True
                
                if sucesso:
                    break

            # se nao tiver achado um horario bom, tentamos outras cores até achar uma que não tenha
            if not sucesso:
                ch3[i].cor += 1

                # se a cor for maior que 20 (só há 20 horarios no turno semanal mais longo), então um erro ocorreu na hora de criar as disciplinas
                if ch2[i].cor > 20:
                    print('Horario nao adicionado : ' + ch3[i].nome, ch3[i].curso, ch3[i].cor, ch3[i].turma, ch3[i].ch)
                    return None

    # Uma condição de loop é estabelecida para captar erros onde um horario não foi encontrado
    sucesso = False
    while not sucesso:

        # Agora faço a busca para as disciplinas de carga horaria 2
        for i in range(len(ch2)):
            sucesso = False

            # Primeiro procuro se a cor já está no horario
            for dia in range(5):

                if ch2[i].curso == 'SIN':
                    if (horarios[dia]['N345'] == ch2[i].cor):
                        ch2[i].horario = 'N34'
                        sucesso = True

                    elif (horarios[dia]['N12'] == ch2[i].cor):
                        ch2[i].horario = 'N12'
                        sucesso = True

                
                else:
                    if horarios[dia]['T345'] == ch2[i].cor:
                        ch2[i].horario = 'T34'
                        sucesso = True

                    elif horarios[dia]['T12'] == ch2[i].cor:
                        ch2[i].horario = 'T12'
                        sucesso = True


                    elif horarios[dia]['M123'] == ch2[i].cor:
                        ch2[i].horario = 'M12'
                        sucesso = True

                    elif horarios[dia]['M45'] == ch2[i].cor:
                        ch2[i].horario = 'M45'
                        sucesso = True

                # se ja tiver achado a cor, quebra o loop
                if sucesso:
                    break
                    # disciplinas = getDisciplinasPorCor()
                    # for no in disciplinas:
                    #     if not checkProfessores(no, dia):
                    #         sucesso = False
                    #         break
                    # if sucesso:
                    #     for no in disciplinas:
                    #         aumentarCargaHorariaProfessor(no, dia)
                    #     break

            # se nao tiver achado o numero, coloca no primeiro None que achar
            if not sucesso:

                for dia in range(5):

                    if ch2[i].curso == 'SIN':
                        if (horarios[dia]['N345'] == None):
                            horarios[dia]['N345'] = ch2[i].cor
                            ch2[i].horario = 'N34'
                            sucesso = True

                        elif (horarios[dia]['N12'] == None):
                            horarios[dia]['N12'] = ch2[i].cor
                            ch2[i].horario = 'N12'
                            sucesso = True

                
                    else:
                        if horarios[dia]['T345'] == None:
                            horarios[dia]['T345'] = ch2[i].cor
                            ch2[i].horario = 'T34'
                            sucesso = True

                        elif horarios[dia]['T12'] == None:
                            horarios[dia]['T12'] = ch2[i].cor
                            ch2[i].horario = 'T12'
                            sucesso = True


                        elif horarios[dia]['M123'] == None:
                            horarios[dia]['M123'] = ch2[i].cor
                            ch2[i].horario = 'M12'
                            sucesso = True

                        elif horarios[dia]['M45'] == None:
                            horarios[dia]['M45'] = ch2[i].cor
                            ch2[i].horario = 'M45'
                            sucesso = True
                    
                    # se ja tiver achado a cor, quebra o loop
                    if sucesso:
                        break


            # se nao tiver achado um horario bom, tentamos outras cores até achar uma que não tenha
            if not sucesso:
                ch3[i].cor += 1

                # se a cor for maior que 20 (só há 20 horarios no turno semanal mais longo), então um erro ocorreu na hora de criar as disciplinas
                if ch2[i].cor > 20:
                    print('Horario nao adicionado : ' + ch2[i].nome, ch2[i].curso, ch2[i].cor, ch2[i].turma, ch2[i].ch)
                    return None
                
                
                
    def checkHorasProfessor():
        problemas = []

        for prof in range(18):
            for dia, ch in listaCHProfessor[prof].items():
                if ch > 6:
                    problemas.append((prof, dia, ch))
        
        return problemas
    
    def updateHorasProfessor():
        for i in range(len(nos)):

            for dia in range(5):
                if nos[i].cor in list(horarios[dia].values()):
                    for prof in nos[i].professores:
                        listaCHProfessor[prof-1][dia] += nos[i].ch

    # def trySwitchingColors():
    #     for info in conflitos:
    #         dia = info[1]

    #         cor = 

    
    updateHorasProfessor()
    conflitos = checkHorasProfessor()
    print(conflitos)

    # if conflitos != []:
    #     # trySwitchingColors()
    #     updateHorasProfessor()
    #     conflitos = checkHorasProfessor()


    # def checkProfessores(no: Disciplina, dia: int):
    #     profs = no.professores
    #     for prof in no:
    #         if listaCHProfessor[prof][dia] + no.ch > 6:
    #             return False
        
    #     return True
    
    # def getDisciplinasPorCor(cor: int):
    #     return [no for no in nos if no.cor == cor]
    
    # def aumentarCargaHorariaProfessor(no: Disciplina, dia: int):
    #     profs = no.professores
    #     for prof in no:
    #         listaCHProfessor[prof][dia] += no.ch




    return horarios

    

def exibirHorariosPorTurma(horarios, nos):
    dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
    turnos = ['M123', 'M45', 'T12', 'T345', 'N12', 'N345']

    # Agrupa as disciplinas por turma
    disciplinas_por_turma = defaultdict(list)
    for no in nos:
        disciplinas_por_turma[no.turma].append(no)

    # Itera por cada turma e exibe os horários
    for turma, disciplinas in disciplinas_por_turma.items():
        print(f"\nHorários para a turma {turma}:")
        
        for dia, horario in enumerate(horarios):
            print(f"\n  {dias[dia]}:")
            for turno in turnos:
                cor = horario[turno]
                if cor is not None:
                    # Filtra as disciplinas da turma que têm a mesma cor
                    disciplinas_no_turno = [
                        no.nome for no in disciplinas if no.cor == cor
                    ]
                    if disciplinas_no_turno:
                        print(f"    {turno}: {', '.join(disciplinas_no_turno)}")
                    else:
                        print(f"    {turno}: Livre")
                else:
                    print(f"    {turno}: Livre")

# Exibe os horários organizados por turma

def colorirGrafoDSatur(nos: list, listaAdjacencia: dict) -> int:
    # Inicialização
    cores_usadas = set()
    grau_saturacao = [0] * len(nos)
    cores_nos = [None] * len(nos)
    nao_coloridos = set(range(len(nos)))

    while nao_coloridos:
        # Seleciona o nó com maior grau de saturação
        # Em caso de empate, escolhe o de maior grau (número de vizinhos)
        max_saturacao = -1
        candidatos = []
        for i in nao_coloridos:
            sat = len(set(cores_nos[vizinho] for vizinho in listaAdjacencia[i] if cores_nos[vizinho] is not None))
            if sat > max_saturacao:
                max_saturacao = sat
                candidatos = [i]
            elif sat == max_saturacao:
                candidatos.append(i)
        # Seleciona o nó com maior grau entre os candidatos
        grau_max = -1
        for i in candidatos:
            grau = len(listaAdjacencia[i])
            if grau > grau_max:
                grau_max = grau
                no_escolhido = i
        # Atribui a menor cor possível
        cores_vizinhos = set(cores_nos[vizinho] for vizinho in listaAdjacencia[no_escolhido] if cores_nos[vizinho] is not None)
        cor = 0
        while cor in cores_vizinhos:
            cor += 1
        cores_nos[no_escolhido] = cor
        cores_usadas.add(cor)
        nao_coloridos.remove(no_escolhido)
        # Atualiza o grau de saturação dos vizinhos
        for vizinho in listaAdjacencia[no_escolhido]:
            if cores_nos[vizinho] is None:
                grau_saturacao[vizinho] += 1
    # Atribui as cores aos nós
    for i in range(len(nos)):
        nos[i].cor = cores_nos[i]
    return len(cores_usadas)

        
def criarCsvHorariosPorTurma(nos: list, grafoTurmas: dict):
    dados = []
    campos = ["Turma", "Nome_Disciplina", "CH", "Professor", "Horario"]  # Define as colunas

    indice = 0
    while indice < len(nos):
        no : Disciplina = nos[indice]

        dicionario = {campos[0]: no.turma, campos[1]: no.nome, campos[2]: no.ch, campos[3]: no.professores, campos[4]: no.horario}

        dados.append(dicionario)

        for disciplina in grafoTurmas:
            no : Disciplina = nos[disciplina]

            dicionario = {campos[0]: no.turma, campos[1]: no.nome, campos[2]: no.ch, campos[3]: no.professores, campos[4]: no.horario}
        
            dados.append(dicionario)
        
        indice = disciplina + 1

    # Criando o arquivo e escrevendo os dados
    nome_arquivo = "teste.csv"
    with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()  # Escreve o cabeçalho
        escritor.writerows(dados)  # Escreve os dados

        

if __name__ == "__main__":
    # Constrói o caminho para o arquivo CSV de forma compatível com qualquer sistema operacional
    caminho_csv = os.path.join("..", "datasets", "csv", "semestre2.csv")

    # Chama a função com o caminho ajustado
    nos = carregarDisciplinasCsv(caminho_csv)
    # arestas = fazerArestas(nos)
    arestas = criarListaAdjacencia(nos)

    # print(arestas)

    print(f'Quantidade de cores: {colorirGrafo(nos, arestas)}')

    grafoPorTurmas = criarGrafoTurmas(nos)
    grafoPorProfessores = criarGrafoProfessores(nos)
    # print(grafoPorTurmas)

    horarios = fazerDivisaoHorario(nos)

    # print(horarios)

    # Exibe os horários formatados
    # exibirHorariosPorTurma(horarios, nos)

    # imprimirHorariosPorTurma(nos, grafoPorTurmas)






    # for i in range(len(grafoPorTurmas)):
    #     print(grafoPorTurmas[i], nos[list(grafoPorTurmas[i])[0]].turma)


    # print([i for i in range(len(nos)) if nos[i].nome == 'Algoritmos e Programação I'])
    # print(arestas[36])

    # for no in nos:
    #     if no.curso == 'SIN':
    #         print(no.nome, no.turma, no.ch, no.cor)

