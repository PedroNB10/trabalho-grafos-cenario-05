import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
import os
import time

def load_disciplines(file_path):
    """Carrega dados do CSV."""
    df = pd.read_csv(file_path, encoding='utf-8')
    return df

def create_restriction_graph(file_path):
    """Cria grafo de restrições considerando múltiplos critérios."""
    df = pd.read_csv(file_path, encoding='utf-8')
    
    # Filtrar disciplinas de CCO e SIN
    df_filtered = df[(df['Curso'] == 'CCO') | (df['Curso'] == 'SIN')]
    
    # Mapear professores para disciplinas
    disciplina_professores = {}
    for _, row in df_filtered.iterrows():
        professores = [col for col in df.columns if col.startswith('Prof ') and row[col] == 1]
        disciplina_professores[row['Nome da Disciplina']] = professores
    
    # Criar grafo de restrições
    G = nx.Graph()
    
    # Adicionar restrições Professor-Disciplina (professores compartilhados)
    disciplinas = list(disciplina_professores.keys())
    for d1, d2 in combinations(disciplinas, 2):
        professores_d1 = set(disciplina_professores[d1])
        professores_d2 = set(disciplina_professores[d2])
        if professores_d1 & professores_d2:  # Professores em comum
            G.add_edge(d1, d2, reason="Professor compartilhado")
    
    # Adicionar restrições Disciplina-Período (mesmo período)
    for period, group in df_filtered.groupby('Período'):
        for d1, d2 in combinations(group['Nome da Disciplina'], 2):
            G.add_edge(d1, d2, reason="Mesmo período")
    
    # Adicionar restrições Disciplina-Curso (mesmo curso)
    for course, group in df_filtered.groupby('Curso'):
        for d1, d2 in combinations(group['Nome da Disciplina'], 2):
            G.add_edge(d1, d2, reason="Mesmo curso")
    
    return G

def get_saturation_degree(vertex, graph, colored_vertices):
    """Calcula o grau de saturação de um vértice."""
    # Conjunto de cores diferentes usadas pelos vizinhos
    neighbor_colors = set()
    for neighbor in graph.neighbors(vertex):
        if neighbor in colored_vertices:
            neighbor_colors.add(colored_vertices[neighbor])
    return len(neighbor_colors)

def get_max_saturation_vertex(graph, colored_vertices, uncolored_vertices):
    """Retorna o vértice não colorido com maior grau de saturação."""
    max_saturation = -1
    max_degree = -1
    selected_vertex = None
    
    for vertex in uncolored_vertices:
        saturation = get_saturation_degree(vertex, graph, colored_vertices)
        degree = graph.degree(vertex)
        
        # Se encontrarmos uma saturação maior ou igual com maior grau
        if (saturation > max_saturation) or \
           (saturation == max_saturation and degree > max_degree):
            max_saturation = saturation
            max_degree = degree
            selected_vertex = vertex
            
    return selected_vertex

def dsatur_coloring(graph):
    """Implementa o algoritmo DSATUR para coloração do grafo."""
    colored_vertices = {}  # Dicionário para armazenar as cores dos vértices
    uncolored_vertices = set(graph.nodes())  # Conjunto de vértices não coloridos
    
    # Enquanto houver vértices não coloridos
    while uncolored_vertices:
        # Seleciona o vértice com maior grau de saturação
        vertex = get_max_saturation_vertex(graph, colored_vertices, uncolored_vertices)
        
        # Encontra a menor cor disponível
        used_colors = set(colored_vertices[neighbor] 
                         for neighbor in graph.neighbors(vertex) 
                         if neighbor in colored_vertices)
        
        # Encontra a primeira cor não utilizada pelos vizinhos
        color = 0
        while color in used_colors:
            color += 1
            
        # Atribui a cor ao vértice
        colored_vertices[vertex] = color
        uncolored_vertices.remove(vertex)
    
    return colored_vertices

def color_graph(graph):
    """Aplica coloração DSATUR ao grafo e mede o tempo."""
    start_time = time.time()
    color_map = dsatur_coloring(graph)
    end_time = time.time()
    execution_time = end_time - start_time
    return color_map, execution_time

def plot_graph(G, colors, filename_prefix):
    """Plota o grafo com cores."""
    plt.figure(figsize=(20,15))
    pos = nx.spring_layout(G, k=0.5)  # Melhora disposição dos nós
    
    # Plotar nós coloridos
    nx.draw_networkx_nodes(
        G, pos, 
        node_color=[colors[node] for node in G.nodes()], 
        cmap=plt.cm.rainbow,
        node_size=3000
    )
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold")
    
    plt.title("Grafo de Restrições de Disciplinas (DSATUR)")
    plt.axis('off')
    plt.tight_layout()
    
    # Salvar versões com diferentes identificadores
    plt.savefig(f'{filename_prefix}_nomes.png')
    plt.close()

    # Versão com códigos
    plt.figure(figsize=(20,15))
    nx.draw_networkx_nodes(
        G, pos, 
        node_color=[colors[node] for node in G.nodes()], 
        cmap=plt.cm.rainbow,
        node_size=3000
    )
    nx.draw_networkx_edges(G, pos)
    
    # Mapeamento de rótulos para códigos
    df = load_disciplines(os.path.join('dataset', 'semestre1.csv'))
    codigo_para_nome = dict(zip(df['Nome da Disciplina'], df['Código da Disciplina']))
    labels = {node: codigo_para_nome.get(node, node) for node in G.nodes()}
    
    nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight="bold")
    
    plt.title("Grafo de Restrições de Disciplinas (Códigos) - DSATUR")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(f'{filename_prefix}_codigos.png')
    plt.close()

def main():
    start_total_time = time.time()
    
    # Carregar e criar grafo de restrições
    print("Iniciando criação do grafo...")
    G = create_restriction_graph(os.path.join('dataset', 'semestre1.csv'))
    
    # Colorir o grafo usando DSATUR
    print("Aplicando coloração DSATUR ao grafo...")
    colors, coloring_time = color_graph(G)
    
    # Plotar grafos
    print("Gerando visualizações...")
    plot_graph(G, colors, 'restricoes_disciplinas_dsatur')
    
    # Calcular tempo total
    end_total_time = time.time()
    total_execution_time = end_total_time - start_total_time
    
    # Informações adicionais
    num_cores = len(set(colors.values()))
    print("\nResultados:")
    print(f"Número de cores necessárias (DSATUR): {num_cores}")
    print(f"Tempo de execução da coloração DSATUR: {coloring_time:.4f} segundos")
    print(f"Tempo total de execução: {total_execution_time:.4f} segundos")
    print("\nCores das disciplinas (DSATUR):")
    for disciplina, cor in sorted(colors.items()):
        print(f"{disciplina}: Cor {cor}")

if __name__ == '__main__':
    main()