import networkx as nx
import matplotlib.pyplot as plt
import os

# Criar um grafo de restrições
grafoRestricoes = nx.Graph()

# Adicionar disciplinas como vértices
disciplinas = [
    'Fundamentos de Programação',
    'Programação Lógica e Funcional',
    'Arquitetura de Computadores II',
    'Algoritmos e Estruturas de Dados I',
    'Algoritmos e Estruturas de Dados I',
    'Modelagem Computacional',
    'Organização e Arquitetura de Computadores I',
    'Economia da Informação',
    'Análise e Projeto de Algoritmos I',
    'Sistemas Operacionais',
    'Engenharia de Software I',
    'Computação Orientada a Objetos I',
    'Paradigmas de Programação',
    'Compiladores',
    'Inteligência Artificial',
    'Computação Gráfica',
    'Banco de Dados II',
    'Adm. e Gerência de Redes de Computadores',
    'Informática e Sociedade',
    'Programação Orientada a Objetos',
    'Engenharia de Software I',
    'Algoritmos e Programação I',
    'Matemática Discreta',
    'Comportamento Organizacional',
    'Organização e Arquitetura de Computadores',
    'Computação Orientada a Objetos II',
    'Sistemas Operacionais',
    'Engenharia de Software II',
    'Banco de Dados I',
    'Algoritmos e Grafos',
    'Informática e Sociedade',
    'Engenharia de Projeto de Software',
    'Adm. e Gerência de Redes de Computadores',
    'Sistemas Distribuídos',
    'Desenvolvimento de Sistemas na Web',
    'Fundamentos de Programação (EPR/EHD)',
    'Fundamentos de Programação (ECI/EAM)',
    'Fundamentos de Programação (FBA)',
    'Tópicos Especiais em Engenharia de Software (PEGA)',
    'Desenvolvimento de Jogos',
    'Maratona de Programação I',
    'Tópicos Especiais em Programação (Programação Paralela)',
    'Data Mining Aplicado',
    'Arquitetura de Software (Opt+Pós)',
    'Visualização de Informação (Opt+Pós)',
    'Simuladores (Pós)',
    'Sistemas Operacionais (Pós)',
    'Tópicos em Engenharia de Software (Pós)'
]

# Definindo os dados de exemplo
# Padrão ==> (Nome, Curso, Periodo, Professor)
dadosDisciplinas = [
    ('Fundamentos de Programação', 'CCO', '2', 'Prof 12'),
    ('Programação Lógica e Funcional', 'CCO', '2', 'Prof 7'),
    ('Arquitetura de Computadores II', 'CCO', '2', 'Prof 10'),
    ('Algoritmos e Estruturas de Dados I', 'CCO', '2', 'Prof 5'), ('Algoritmos e Estruturas de Dados I', 'CCO', '2', 'Prof 6'),
    ('Modelagem Computacional', 'CCO', '2', 'Prof 5'),
    ('Organização e Arquitetura de Computadores I', 'CCO', '2', 'Prof 13'),
    ('Economia da Informação', 'CCO', '2', 'Prof 2'),
    ('Análise e Projeto de Algoritmos I', 'CCO', '4', 'Prof 14'),
    ('Sistemas Operacionais', 'CCO', '4', 'Prof 5'),
    ('Engenharia de Software I', 'CCO', '4', 'Prof 8'),
    ('Computação Orientada a Objetos I', 'CCO', '4', 'Prof 9'),
    ('Paradigmas de Programação', 'CCO', '6', 'Prof 7'),
    ('Compiladores', 'CCO', '6', 'Prof 5'),
    ('Inteligência Artificial', 'CCO', '6', 'Prof 3'),
    ('Computação Gráfica', 'CCO', '6', 'Prof 6'),
    ('Banco de Dados II', 'CCO', '6', 'Prof 18'),
    ('Adm. e Gerência de Redes de Computadores', 'CCO', '6', 'Prof 4'),
    ('Informática e Sociedade', 'CCO', '6', 'Prof 2'),
    ('Programação Orientada a Objetos', 'SIN', '2', 'Prof 9'),
    ('Engenharia de Software I', 'SIN', '2', 'Prof 8'),
    ('Algoritmos e Programação I', 'SIN', '2', 'Prof 14'),
    ('Matemática Discreta', 'SIN', '2', 'Prof 5'),
    ('Comportamento Organizacional', 'SIN', '2', 'Prof 2'),
    ('Organização e Arquitetura de Computadores', 'SIN', '2', 'Prof 11'),
    ('Computação Orientada a Objetos II', 'SIN', '4', 'Prof 15'),
    ('Sistemas Operacionais', 'SIN', '4', 'Prof 13'),
    ('Engenharia de Software II', 'SIN', '4', 'Prof 10'),
    ('Banco de Dados I', 'SIN', '4', 'Prof 12'),
    ('Algoritmos e Grafos', 'SIN', '4', 'Prof 16'),
    ('Informática e Sociedade', 'SIN', '6', 'Prof 2'),
    ('Engenharia de Projeto de Software', 'SIN', '6', 'Prof 1'),
    ('Adm. e Gerência de Redes de Computadores', 'SIN', '6', 'Prof 4'),
    ('Sistemas Distribuídos', 'SIN', '6', 'Prof 16'),
    ('Desenvolvimento de Sistemas na Web', 'SIN', '6', 'Prof 9'),
    ('Fundamentos de Programação (EPR/EHD)', 'Outros Cursos', '2', 'Prof 15'),
    ('Fundamentos de Programação (ECI/EAM)', 'Outros Cursos', '2', 'Prof 8'),
    ('Fundamentos de Programação (FBA)', 'Outros Cursos', '2', 'Prof 3'),
    ('Tópicos Especiais em Engenharia de Software (PEGA)', 'Optativas', '4', 'Prof 4'),
    ('Desenvolvimento de Jogos', 'Optativas', '4', 'Prof 6'),
    ('Maratona de Programação I', 'Optativas', '6', 'Prof 11'),
    ('Tópicos Especiais em Programação (Programação Paralela)', 'Optativas', '6', 'Prof 5'),
    ('Data Mining Aplicado', 'Optativas', '4', 'Prof 18'),
    ('Arquitetura de Software (Opt+Pós)', 'Pós Graduação', '4', 'Prof 10'),
    ('Visualização de Informação (Opt+Pós)', 'Pós Graduação', '4', 'Prof 12'),
    ('Simuladores (Pós)', 'Pós Graduação', '6', 'Prof 3'),
    ('Sistemas Operacionais (Pós)', 'Pós Graduação', '4', 'Prof 4'),
    ('Tópicos em Engenharia de Software (Pós)', 'Pós Graduação', '6', 'Prof 17'),
]

# Adicionando nós
for i in range(len(disciplinas)):
    if dadosDisciplinas[i][1] == "SIN":
        grafoRestricoes.add_node(disciplinas[i])

# Adicionar arestas para restrições
for i in range(len(dadosDisciplinas)):
    for j in range(i + 1, len(dadosDisciplinas)):

        # Travando para um curso só
        if (dadosDisciplinas[i][1] != "SIN"):
            break
        if (dadosDisciplinas[j][1] != "SIN"):
            continue

        # Verificando mesmo curso e mesmo período
        if (dadosDisciplinas[i][1] == dadosDisciplinas[j][1] and 
            dadosDisciplinas[i][2] == dadosDisciplinas[j][2]):
            grafoRestricoes.add_edge(dadosDisciplinas[i][0], dadosDisciplinas[j][0])
        
        # Verificando mesmo professor
        if set(dadosDisciplinas[i][3]) & set(dadosDisciplinas[j][3]):  # Interseção dos professores
            grafoRestricoes.add_edge(dadosDisciplinas[i][0], dadosDisciplinas[j][0])

# Desenhando o grafo
plt.figure(figsize=(10, 10))
nx.draw(grafoRestricoes, with_labels=True, font_weight='bold', node_size=3000, node_color='lightblue', font_size=10)

# Caminho do diretório raiz
diretorioRaiz = os.path.dirname(os.path.abspath(__file__))  # Caminho do script atual
diretorioImagens = os.path.join(diretorioRaiz, '..', 'imagens')  # Caminho para a pasta 'imagens'

diretorio_saida = "../representacao-grafos"
if not os.path.exists(diretorio_saida):
    os.makedirs(diretorio_saida)

# Salvar a imagem no caminho especificado
plt.savefig(f"{diretorio_saida}/grafoRestricoes.png", format="png", bbox_inches="tight")

plt.show()






