import pandas as pd
import networkx as nx
import time
import random

# Definindo a semente para reprodução dos resultados
random.seed(42)

# Carregar o arquivo CSV
data = pd.read_csv('dataset/semestre1.csv')

# Criar um grafo vazio
G = nx.Graph()

# Adicionando arestas para professor x disciplina
for index, row in data.iterrows():
    for prof in range(1, 19):  # Prof 1 a Prof 18
        if row[f'Prof {prof}'] == 1:
            G.add_edge(row['Nome da Disciplina'], f'Prof {prof}')

# Adicionando arestas para disciplina x período (mesmo período)
for index, row in data.iterrows():
    disciplina_atual = row['Nome da Disciplina']
    periodo_atual = row['Período']
    # Encontrar outras disciplinas no mesmo período
    for idx, other_row in data.iterrows():
        if other_row['Período'] == periodo_atual and other_row['Nome da Disciplina'] != disciplina_atual:
            G.add_edge(disciplina_atual, other_row['Nome da Disciplina'])

# Adicionando arestas para disciplina x curso (mesmo curso)
for index, row in data.iterrows():
    disciplina_atual = row['Nome da Disciplina']
    curso_atual = row['Curso']
    # Encontrar outras disciplinas no mesmo curso
    for idx, other_row in data.iterrows():
        if other_row['Curso'] == curso_atual and other_row['Nome da Disciplina'] != disciplina_atual:
            G.add_edge(disciplina_atual, other_row['Nome da Disciplina'])

# Função para coloração greedy
def greedy_coloring(graph):
    start_time = time.time()
    coloring = nx.coloring.greedy_color(graph, strategy='largest_first')
    end_time = time.time()
    num_colors = len(set(coloring.values()))
    return coloring, num_colors, end_time - start_time

# Função para coloração DSATUR
def dsatur_coloring(graph):
    start_time = time.time()
    
    # Inicializando variáveis
    coloring = {}
    degrees = {node: len(list(graph.neighbors(node))) for node in graph.nodes()}
    saturation = {node: 0 for node in graph.nodes()}
    
    while len(coloring) < len(graph.nodes()):
        # Encontrar o nó com maior grau de saturação
        max_saturation_node = max((node for node in graph.nodes() if node not in coloring), 
                                   key=lambda n: (saturation[n], degrees[n]))
        
        # Encontrar as cores já usadas pelos vizinhos
        neighbor_colors = {coloring[neighbor] for neighbor in graph.neighbors(max_saturation_node) if neighbor in coloring}
        
        # Atribuir a menor cor disponível ao nó selecionado
        color = 0
        while color in neighbor_colors:
            color += 1
        
        coloring[max_saturation_node] = color
        
        # Atualizar a saturação dos vizinhos
        for neighbor in graph.neighbors(max_saturation_node):
            if neighbor not in coloring:
                saturation[neighbor] += 1
    
    end_time = time.time()
    num_colors = len(set(coloring.values()))
    return coloring, num_colors, end_time - start_time

# Executando os algoritmos de coloração
greedy_result, greedy_colors, greedy_time = greedy_coloring(G)
dsatur_result, dsatur_colors, dsatur_time = dsatur_coloring(G)

# Análise dos resultados
print("Resultados da Coloração Greedy:")
print(f"Número de Cores Usadas: {greedy_colors}")
print(f"Tempo de Execução: {greedy_time:.6f} segundos\n")

print("Resultados da Coloração DSATUR:")
print(f"Número de Cores Usadas: {dsatur_colors}")
print(f"Tempo de Execução: {dsatur_time:.6f} segundos\n")

# Comparação Final
comparison_table = f"""
| Algoritmo         | Número de Cores | Tempo de Execução (s) |
|-------------------|-----------------|------------------------|
| Coloracao Greedy  | {greedy_colors} | {greedy_time:.6f}      |
| Coloracao DSATUR  | {dsatur_colors} | {dsatur_time:.6f}      |
"""

print(comparison_table)