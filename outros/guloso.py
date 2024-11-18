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

def visualize_graph(graph, color_map, seed=42):
    """Visualiza o grafo com as cores atribuídas."""
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph, seed=seed)
    colors = [color_map[node] for node in graph.nodes]
    nx.draw(graph, pos, with_labels=True, node_color=colors, cmap=plt.cm.Set3, node_size=5000, font_size=10)
    plt.show()

def color_graph(graph):
    """Aplica coloração ao grafo para minimizar conflitos."""
    start_time = time.time()
    color_map = nx.coloring.greedy_color(graph, strategy="largest_first")
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
    
    plt.title("Grafo de Restrições de Disciplinas")
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
    
    plt.title("Grafo de Restrições de Disciplinas (Códigos)")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(f'{filename_prefix}_codigos.png')
    plt.close()

def main():
    start_total_time = time.time()
    
    # Carregar e criar grafo de restrições
    print("Iniciando criação do grafo...")
    G = create_restriction_graph(os.path.join('dataset', 'semestre1.csv'))
    
    # Colorir o grafo
    print("Aplicando coloração ao grafo...")
    colors, coloring_time = color_graph(G)
    
    # Plotar grafos
    print("Gerando visualizações...")
    plot_graph(G, colors, 'restricoes_disciplinas')
    
    # Calcular tempo total
    end_total_time = time.time()
    total_execution_time = end_total_time - start_total_time
    
    # Informações adicionais
    num_cores = len(set(colors.values()))
    print("\nResultados:")
    print(f"Número de cores necessárias: {num_cores}")
    print(f"Tempo de execução da coloração: {coloring_time:.4f} segundos")
    print(f"Tempo total de execução: {total_execution_time:.4f} segundos")
    print("\nCores das disciplinas:")
    for disciplina, cor in sorted(colors.items()):
        print(f"{disciplina}: Cor {cor}")

if __name__ == '__main__':
    main()