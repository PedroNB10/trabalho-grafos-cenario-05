# Código desenvolvido em grupo na disciplina de Grafos

import os
import networkx as nx
import matplotlib.pyplot as plt

# Criar o grafo bipartido
G = nx.Graph()

# Conjunto A: Disciplinas com vértices únicos e a carga horária como atributo
disciplinas_info = {
    'Fundamentos de Programação': 4, 
    #'Programação Lógica e Funcional': 4,
    #'Arquitetura de Computadores II': 4,
    #'Algoritmos e Estruturas de Dados I': 4,
    #'Modelagem Computacional': 4,
    #'Organização e Arquitetura de Computadores I': 4,
    #'Economia da Informação': 3,
    #'Análise e Projeto de Algoritmos I': 4,
    'Sistemas Operacionais': 5,
    #'[CCO] Engenharia de Software I': 5,
    #'Computação Orientada a Objetos I': 4,
    #'Paradigmas de Programação': 4,
    #'Compiladores': 4,
    #'Inteligência Artificial': 4,
    #'Computação Gráfica': 3,
    #'Banco de Dados II': 4,
    'Adm. e Gerência de Redes de Computadores': 3,
    'Informática e Sociedade': 3,
    'Programação Orientada a Objetos': 4,
    '[SIN] Engenharia de Software I': 4,
    'Algoritmos e Programação I': 4,
    'Matemática Discreta': 4,
    'Comportamento Organizacional': 3,
    'Organização e Arquitetura de Computadores': 4,
    'Computação Orientada a Objetos II': 4,
    'Engenharia de Software II': 4,
    'Banco de Dados I': 4,
    'Algoritmos e Grafos': 3,
    'Engenharia de Projeto de Software': 4,
    'Sistemas Distribuídos': 4,
    'Desenvolvimento de Sistemas na Web': 5,
    #'Fundamentos de Programação (EPR/EHD)': 4,
    #'Fundamentos de Programação (ECI/EAM)': 4,
    #'Fundamentos de Programação (FBA)': 4,
    #'Tópicos Especiais em Engenharia de Software (PEGA)': 4,
    #'Desenvolvimento de Jogos': 4,
    #'Maratona de Programação I': 3,
    #'Tópicos Especiais em Programação (Programação Paralela)': 4,
    #'Data Mining Aplicado': 4,
    #'Arquitetura de Software (Opt+Pós)': 4,
    #'Visualização de Informação (Opt+Pós)': 4,
    #'Simuladores (Pós)': 4,
    #'Sistemas Operacionais (Pós)': 2,
    #'Tópicos em Engenharia de Software (Pós)': 4
}

# Adicionar vértices para disciplinas com a carga horária como atributo
for disciplina, ch in disciplinas_info.items():
    G.add_node(disciplina, bipartite=0, ch=ch)

# Conjunto B: Professores
professores = ['Prof1', 'Prof2', 'Prof3', 'Prof4', 'Prof5', 
               'Prof6', 'Prof7', 'Prof8', 'Prof9', 
               'Prof10', 'Prof11', 'Prof12', 
               'Prof13', 'Prof14', 
               'Prof15', 'Prof16', 
               'Prof17', 
               'Prof18']

# Adicionar vértices para os professores
for professor in professores:
    G.add_node(professor, bipartite=1)

# Arestas conectando disciplinas a professores (disponibilidade)
arestas = [
    ('Fundamentos de Programação', 'Prof12'),
    #('Programação Lógica e Funcional', 'Prof7'),
    #('Arquitetura de Computadores II', 'Prof13'),
    #('Algoritmos e Estruturas de Dados I', 'Prof6'), ('Algoritmos e Estruturas de Dados I', 'Prof15'),
    #('Modelagem Computacional', 'Prof5'),
    #('Organização e Arquitetura de Computadores I', 'Prof13'),
    #('Economia da Informação', 'Prof2'),
    #('Análise e Projeto de Algoritmos I', 'Prof14'),
    ('Sistemas Operacionais', 'Prof13'), # ('Sistemas Operacionais', 'Prof11'), removido por ser de CCO
    #('[CCO] Engenharia de Software I', 'Prof8'),
    #('Computação Orientada a Objetos I', 'Prof9'),
    #('Paradigmas de Programação', 'Prof7'),
    #('Compiladores', 'Prof5'),
    #('Inteligência Artificial', 'Prof3'),
    #('Computação Gráfica', 'Prof6'),
    #('Banco de Dados II', 'Prof18'),
    ('Adm. e Gerência de Redes de Computadores', 'Prof4'),
    ('Informática e Sociedade', 'Prof2'),
    ('Programação Orientada a Objetos', 'Prof9'),
    ('[SIN] Engenharia de Software I', 'Prof8'),
    ('Algoritmos e Programação I', 'Prof14'),
    ('Matemática Discreta', 'Prof5'),
    ('Comportamento Organizacional', 'Prof2'),
    ('Organização e Arquitetura de Computadores', 'Prof11'),
    ('Computação Orientada a Objetos II', 'Prof15'),
    ('Engenharia de Software II', 'Prof10'),
    ('Banco de Dados I', 'Prof12'),
    ('Algoritmos e Grafos', 'Prof16'),
    ('Engenharia de Projeto de Software', 'Prof1'),
    ('Sistemas Distribuídos', 'Prof16'),
    ('Desenvolvimento de Sistemas na Web', 'Prof9'),
    #('Fundamentos de Programação (EPR/EHD)', 'Prof15'),
    #('Fundamentos de Programação (ECI/EAM)', 'Prof8'),
    #('Fundamentos de Programação (FBA)', 'Prof3'),
    #('Tópicos Especiais em Engenharia de Software (PEGA)', 'Prof4'),
    #('Desenvolvimento de Jogos', 'Prof6'), ('Desenvolvimento de Jogos', 'Prof15'),
    #('Maratona de Programação I', 'Prof11'),
    #('Tópicos Especiais em Programação (Programação Paralela)', 'Prof5'), ('Tópicos Especiais em Programação (Programação Paralela)', 'Prof13'),
    #('Data Mining Aplicado', 'Prof18'),
    #('Arquitetura de Software (Opt+Pós)', 'Prof10'),
    #('Visualização de Informação (Opt+Pós)', 'Prof12'),
    #('Simuladores (Pós)', 'Prof3'),
    #('Sistemas Operacionais (Pós)', 'Prof4'),
    #('Tópicos em Engenharia de Software (Pós)', 'Prof17')
]


# Adicionar as arestas ao grafo
for aresta in arestas:
     if isinstance(aresta[1], list):
         for professor in aresta[1]:
             G.add_edge(aresta[0], professor)
     else:
         G.add_edge(aresta[0], aresta[1])

plt.figure(figsize=(20, 14))  # Largura, altura

# Definir o layout bipartido para visualização
pos = {}
# Aumentar ainda mais o espaçamento entre as disciplinas
discipline_spacing = 5  # Aumentar o espaçamento entre disciplinas
pos.update((n, (0, i * discipline_spacing)) for i, n in enumerate(disciplinas_info))

# Manter o espaçamento grande para os professores
professor_spacing = 8  # Ajustando um pouco mais o espaçamento vertical dos professores
pos.update((professor, (1, i * professor_spacing)) for i, professor in enumerate(professores))

# Desenhar os nós das disciplinas e professores
disciplinas = [n for n in G.nodes if G.nodes[n].get('bipartite') == 0]
professores = [n for n in G.nodes if G.nodes[n].get('bipartite') == 1]

# Desenhar nós
nx.draw_networkx_nodes(G, pos, nodelist=disciplinas, node_color='skyblue', node_size=1000)
nx.draw_networkx_nodes(G, pos, nodelist=professores, node_color='orange', node_size=1000)

# Definir cores das arestas com base na carga horária das disciplinas
edge_colors = []
for u, v in G.edges():
     carga_horaria = G.nodes[u].get('ch')
     if carga_horaria >= 4:
         edge_colors.append('blue') # Azul para carga horária >= 4
     else:
         edge_colors.append('red') # Vermelho para carga horária < 4

# Desenhar as arestas com as cores definidas
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=1, edge_color=edge_colors)

# Adicionar rótulos para os nós (Disciplinas e Professores)
nx.draw_networkx_labels(G, pos, font_size=8)

# Exibir o grafo
plt.title("Grafo Bipartido: Disciplinas e Professores com Carga Horária")
plt.savefig(fr"C:\Users\omath\OneDrive\Área de Trabalho\Frinhani\grafo_professor_disciplina.png", format="png", bbox_inches="tight")
plt.show()