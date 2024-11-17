import os
import csv
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Alignment, PatternFill
from openpyxl.utils import get_column_letter
import random


# Criar diretórios caso não existam
os.makedirs('dataset', exist_ok=True)
os.makedirs('controle', exist_ok=True)
os.makedirs('professores (bruto)', exist_ok=True)
os.makedirs('professores (importar)', exist_ok=True)
os.makedirs('grafos', exist_ok=True) 

# Ler arquivo da pasta dataset
df = pd.read_csv(os.path.join('dataset', 'semestre1.csv'))

def create_assignment_graphs():
    assignment_graph_name = nx.Graph()
    assignment_graph_code = nx.Graph()
    
    # Criar um dicionário para rastrear ocorrências múltiplas
    disc_occurrences = defaultdict(int)
    code_occurrences = defaultdict(int)
    
    for _, row in df.iterrows():
        # Incrementar contadores
        disc_occurrences[row['Nome da Disciplina']] += 1
        code_occurrences[row['Código da Disciplina']] += 1
        
        # Adicionar sufixo para disciplinas duplicadas
        disciplina_nome = f"{row['Nome da Disciplina']}_{disc_occurrences[row['Nome da Disciplina']]}"
        disciplina_codigo = f"{row['Código da Disciplina']}_{code_occurrences[row['Código da Disciplina']]}"
        
        for i in range(1, 19):
            prof_col = f'Prof {i}'
            if row[prof_col] == 1:
                assignment_graph_name.add_edge(f'Prof {i}', disciplina_nome)
                assignment_graph_code.add_edge(f'Prof {i}', disciplina_codigo)
    
    return assignment_graph_name, assignment_graph_code

def create_constraint_graphs():
    constraint_graph_name = nx.Graph()
    constraint_graph_code = nx.Graph()
    prof_to_disc = defaultdict(list)
    
    # Rastrear ocorrências múltiplas
    disc_occurrences = defaultdict(int)
    code_occurrences = defaultdict(int)
    
    for _, row in df.iterrows():
        # Incrementar contadores
        disc_occurrences[row['Nome da Disciplina']] += 1
        code_occurrences[row['Código da Disciplina']] += 1
        
        disc_nome = f"{row['Nome da Disciplina']}_{disc_occurrences[row['Nome da Disciplina']]}"
        disc_codigo = f"{row['Código da Disciplina']}_{code_occurrences[row['Código da Disciplina']]}"
        periodo = row['Período']
        curso = row['Curso']
        
        constraint_graph_name.add_node(disc_nome)
        constraint_graph_code.add_node(disc_codigo)
        
        for i in range(1, 19):
            if row[f'Prof {i}'] == 1:
                prof_to_disc[f'Prof {i}'].append((disc_nome, disc_codigo))
    
        # Adicionar arestas para disciplinas do mesmo período/curso
        for _, other_row in df.iterrows():
            other_disc_occurrences = disc_occurrences[other_row['Nome da Disciplina']]
            other_code_occurrences = code_occurrences[other_row['Código da Disciplina']]
            
            if (other_row['Período'] == periodo and 
                other_row['Curso'] == curso and 
                other_row['Nome da Disciplina'] != row['Nome da Disciplina']):
                other_disc_nome = f"{other_row['Nome da Disciplina']}_{other_disc_occurrences}"
                other_disc_codigo = f"{other_row['Código da Disciplina']}_{other_code_occurrences}"
                constraint_graph_name.add_edge(disc_nome, other_disc_nome)
                constraint_graph_code.add_edge(disc_codigo, other_disc_codigo)
    
    # Adicionar arestas entre disciplinas do mesmo professor
    for prof_discs in prof_to_disc.values():
        for i in range(len(prof_discs)):
            for j in range(i + 1, len(prof_discs)):
                constraint_graph_name.add_edge(prof_discs[i][0], prof_discs[j][0])
                constraint_graph_code.add_edge(prof_discs[i][1], prof_discs[j][1])
    
    return constraint_graph_name, constraint_graph_code

def check_conflicts(schedule, new_allocation):
    """
    Verifica se há conflitos de horário para a nova alocação
    """
    dia, turno, horario = new_allocation['Dia'], new_allocation['Turno'], new_allocation['Horário']
    curso, periodo = new_allocation['Curso'], new_allocation['Período']
    professor = new_allocation['Professor']
    
    # Verificar conflitos no mesmo horário
    conflitos = schedule[
        (schedule['Dia'] == dia) & 
        (schedule['Turno'] == turno) & 
        (schedule['Horário'] == horario)
    ]
    
    # Se houver alguma aula no mesmo horário
    for _, aula in conflitos.iterrows():
        # Verificar conflito de professor
        if aula['Professor'] == professor:
            return True
        # Verificar conflito de turma (mesmo período/curso)
        if aula['Curso'] == curso and aula['Período'] == periodo:
            return True
    
    return False

def dsatur_coloring(graph):
    colors = {}
    vertices = sorted(graph.nodes(), key=lambda x: graph.degree(x), reverse=True)
    colors[vertices[0]] = 0
    
    def get_saturation(vertex):
        neighbor_colors = set()
        for neighbor in graph[vertex]:
            if neighbor in colors:
                neighbor_colors.add(colors[neighbor])
        return len(neighbor_colors)
    
    for _ in range(1, len(vertices)):
        max_sat = -1
        max_vertex = None
        for vertex in vertices:
            if vertex not in colors:
                sat = get_saturation(vertex)
                if sat > max_sat:
                    max_sat = sat
                    max_vertex = vertex
        
        used_colors = set(colors[neighbor] for neighbor in graph[max_vertex] if neighbor in colors)
        color = 0
        while color in used_colors:
            color += 1
        colors[max_vertex] = color
    
    return colors

def generate_schedules():
    schedules = {}
    dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
    turnos = ['M', 'T', 'N']
    horarios = range(1, 6)
    
    # Criar um DataFrame global para rastrear todas as alocações
    global_schedule = pd.DataFrame(columns=['Dia', 'Turno', 'Horário', 'Curso', 'PPC', 
                                          'Período', 'Código', 'Disciplina', 'CH', 'Professor'])
    
    # Ordenar disciplinas por restrições
    disciplinas = []
    for _, row in df.iterrows():
        profs = sum([1 for i in range(1, 19) if row[f'Prof {i}'] == 1])
        disciplinas.append({
            'row': row,
            'restricoes': profs + (1 if row['Curso'] in ['CCO', 'SIN'] else 0)
        })
    
    disciplinas.sort(key=lambda x: x['restricoes'], reverse=True)
    
    # Alocar disciplinas
    for disc in disciplinas:
        row = disc['row']
        ch = row['CH']
        
        # Identificar professor(es)
        profs = [f'Prof {i}' for i in range(1, 19) if row[f'Prof {i}'] == 1]
        
        # Definir turnos preferenciais
        turnos_pref = []
        if row['Curso'] == 'CCO':
            turnos_pref = ['M', 'T', 'N']
        elif row['Curso'] == 'SIN':
            turnos_pref = ['N', 'T', 'M']
        else:
            turnos_pref = ['M', 'T', 'N']
        
        # Alocar blocos de aula
        remaining_ch = ch
        while remaining_ch > 0:
            block_size = min(2, remaining_ch)
            allocated = False
            
            for prof in profs:
                for dia in dias:
                    for turno in turnos_pref:
                        for horario in horarios:
                            if horario + block_size <= 6:
                                pode_alocar = True
                                
                                for h in range(block_size):
                                    new_allocation = {
                                        'Dia': dia,
                                        'Turno': turno,
                                        'Horário': horario + h,
                                        'Curso': row['Curso'],
                                        'PPC': row['PPC'],
                                        'Período': row['Período'],
                                        'Código': row['Código da Disciplina'],
                                        'Disciplina': row['Nome da Disciplina'],
                                        'CH': row['CH'],
                                        'Professor': prof
                                    }
                                    
                                    if check_conflicts(global_schedule, new_allocation):
                                        pode_alocar = False
                                        break
                                
                                if pode_alocar:
                                    for h in range(block_size):
                                        new_allocation = {
                                            'Dia': dia,
                                            'Turno': turno,
                                            'Horário': horario + h,
                                            'Curso': row['Curso'],
                                            'PPC': row['PPC'],
                                            'Período': row['Período'],
                                            'Código': row['Código da Disciplina'],
                                            'Disciplina': row['Nome da Disciplina'],
                                            'CH': row['CH'],
                                            'Professor': prof
                                        }
                                        global_schedule = pd.concat([global_schedule, 
                                                                   pd.DataFrame([new_allocation])], 
                                                                  ignore_index=True)
                                    allocated = True
                                    break
                            
                        if allocated:
                            break
                    if allocated:
                        break
                if allocated:
                    break
            
            if not allocated:
                if block_size == 2:
                    continue
                else:
                    print(f"Não foi possível alocar completamente a disciplina {row['Nome da Disciplina']}")
                    break
            
            remaining_ch -= block_size
    
    # Separar schedules por professor
    for i in range(1, 19):
        prof = f'Prof {i}'
        schedules[prof] = global_schedule[global_schedule['Professor'] == prof].copy()
    
    return schedules, global_schedule

def plot_graph(graph, title, colors=None):
    plt.figure(figsize=(15, 10))
    pos = nx.spring_layout(graph, k=1, iterations=50)
    
    if colors:
        node_colors = [colors.get(node, 'white') for node in graph.nodes()]
        nx.draw(graph, pos, with_labels=True, node_color=node_colors,
               node_size=1500, font_size=6, font_weight='bold')
    else:
        nx.draw(graph, pos, with_labels=True,
               node_size=1500, font_size=6, font_weight='bold')
    
    plt.title(title)
    
    # Salvar o gráfico na pasta 'grafos'
    plt.savefig(os.path.join('grafos', f'{title}.png'))  # Salva o gráfico com o título como nome do arquivo
    
    # Exibir o gráfico
    plt.show()

def display_professor_schedule(schedules):
    """
    Exibe o horário de cada professor em formato organizado
    e salva os dados em um arquivo CSV.
    """
    dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
    turnos = ['M', 'T', 'N']
    horarios = range(1, 6)

    # Lista para armazenar dados que serão salvos no CSV
    csv_data = []
    
    for i in range(1, 19):
        prof = f'Prof {i}'
        print(f"\nHorário do {prof}:")
        print("-" * 80)
        
        prof_schedule = schedules[prof]
        
        for dia in dias:
            print(f"\n{dia}:")
            for turno in turnos:
                print(f"\nTurno {turno}:")
                for horario in horarios:
                    aula = prof_schedule[
                        (prof_schedule['Dia'] == dia) & 
                        (prof_schedule['Turno'] == turno) & 
                        (prof_schedule['Horário'] == horario)
                    ]
                    
                    if len(aula) > 0:
                        row = aula.iloc[0]
                        disciplina = f"{row['Disciplina']} ({row['Curso']} - {row['Período']}º período)"
                        print(f"Horário {horario}: {disciplina}")
                    else:
                        disciplina = "livre"
                        print(f"Horário {horario}: livre")

                    # Adiciona os dados na lista para o CSV
                    csv_data.append({
                        'Professor': prof,
                        'Dia': dia,
                        'Turno': turno,
                        'Horário': horario,
                        'Disciplina': disciplina
                    })
        print("=" * 80)
    
    # Salva os dados no arquivo CSV dentro da pasta 'controle'
    with open('controle/planilha.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Professor', 'Dia', 'Turno', 'Horário', 'Disciplina'])
        writer.writeheader()
        writer.writerows(csv_data)

def save_schedules(schedules, global_schedule):
    # Salvar arquivo global
    global_schedule.to_csv(os.path.join('controle', 'horario_global.csv'), index=False)
    
    # Salvar grades individuais
    for i in range(1, 19):
        prof = f'Prof {i}'
        prof_schedule = schedules[prof]
        prof_schedule.to_csv(os.path.join('professores (bruto)', f'{prof}_schedule.csv'), index=False)
    
    print("Horários salvos com sucesso.")

# Executar as funções
assignment_graph_name, assignment_graph_code = create_assignment_graphs()
constraint_graph_name, constraint_graph_code = create_constraint_graphs()

# Aplicar coloração DSATUR
colors_name = dsatur_coloring(constraint_graph_name)
colors_code = dsatur_coloring(constraint_graph_code)

# Mostrar quantidade de cores utilizadas
num_colors_name = len(set(colors_name.values()))
num_colors_code = len(set(colors_code.values()))
print(f"Número de cores utilizadas (grafo de nomes): {num_colors_name}")
print(f"Número de cores utilizadas (grafo de códigos): {num_colors_code}")

# Gerar visualizações
plot_graph(assignment_graph_name, "Grafo de Atribuição (Nomes das Disciplinas)")
plot_graph(assignment_graph_code, "Grafo de Atribuição (Códigos das Disciplinas)")
plot_graph(constraint_graph_name, "Grafo de Restrições (Nomes das Disciplinas)", colors_name)
plot_graph(constraint_graph_code, "Grafo de Restrições (Códigos das Disciplinas)", colors_code)

schedules, global_schedule = generate_schedules()
display_professor_schedule(schedules)
save_schedules(schedules, global_schedule)

# GERA ARQUIVOS IMPORTÁVEIS PARA SPREADSHEET OU EXCEL (PROFESSORES)
# Dicionário para mapear turno e horário
# Serve para professores e alunos
horarios = {
    "M1": "07:00 - 07:55", "M2": "07:55 - 08:50", "M3": "08:50 - 09:45",
    "M4": "10:10 - 11:00", "M5": "11:00 - 11:55", "T1": "13:30 - 14:25",
    "T2": "14:25 - 15:20", "T3": "15:45 - 16:40", "T4": "16:40 - 17:35",
    "T5": "17:35 - 18:30", "N1": "19:00 - 19:50", "N2": "19:50 - 20:40",
    "N3": "21:00 - 21:50", "N4": "21:50 - 22:40", "N5": "22:40 - 23:30"
}

# Carregar o arquivo CSV
arquivo_csv = "controle/planilha.csv"
df = pd.read_csv(arquivo_csv)

# Substituir os identificadores pelos horários no DataFrame
df["Turno_Horário"] = (df["Turno"].astype(str) + df["Horário"].astype(str)).map(horarios)

# Agrupar os dados por professor
professores = df.groupby("Professor")

# Cores para as células
red_fill = PatternFill(start_color="FF9999", end_color="FF9999", fill_type="solid")
green_fill = PatternFill(start_color="99FF99", end_color="99FF99", fill_type="solid")

# Gerar um arquivo para cada professor
for professor, dados in professores:
    wb = Workbook()
    ws = wb.active
    ws.title = professor

    # Adicionar título com nome do professor
    row = 1
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=3)
    ws.cell(row=row, column=1).value = professor
    ws.cell(row=row, column=1).alignment = Alignment(horizontal="center", vertical="center")
    row += 1

    # Adicionar cabeçalho
    ws.cell(row=row, column=1).value = "Dia da Semana"
    ws.cell(row=row, column=2).value = "Horário"
    ws.cell(row=row, column=3).value = "Disciplina"
    ws.row_dimensions[row].height = 20
    row += 1

    # Preencher os dados
    for _, linha in dados.iterrows():
        ws.cell(row=row, column=1).value = linha["Dia"]
        ws.cell(row=row, column=2).value = linha["Turno_Horário"]
        ws.cell(row=row, column=3).value = linha["Disciplina"]

        # Aplicar cor de fundo
        if linha["Disciplina"].lower() != "livre":
            ws.cell(row=row, column=3).fill = red_fill
        else:
            ws.cell(row=row, column=3).fill = green_fill

        row += 1

    # Ajustar largura das colunas
    for col in range(1, 4):
        ws.column_dimensions[get_column_letter(col)].width = 25  # Aproximadamente 250 pixels

    # Salvar o arquivo para o professor na pasta especificada
    nome_arquivo = os.path.join("professores (importar)", f"{professor}_horarios.xlsx")
    wb.save(nome_arquivo)

print("Planilhas de professores geradas com sucesso!")

# GERA ARQUIVOS IMPORTÁVEIS PARA SPREADSHEET OU EXCEL (ALUNOS)
# Função para concatenar os horários
def get_horario(dia, turno, horario):
    # Construir a chave para o dicionário de horários
    chave = f"{turno}{horario}"
    # Se o horário existir no dicionário, retornamos o valor correspondente
    if chave in horarios:
        return f"{dia} {turno} {horarios[chave]}"
    else:
        return "Desconhecido"

# Função para ler o arquivo CSV e gerar as planilhas
def gerar_planilhas():
    # Caminho do arquivo CSV
    caminho_csv = os.path.join('controle', 'horario_global.csv')

    # Ler o arquivo CSV
    df = pd.read_csv(caminho_csv)

    # Criar pasta "alunos (importar)" se não existir
    os.makedirs('alunos (importar)', exist_ok=True)

    # Agrupar por Curso, PPC e Período
    grupos = df.groupby(['Curso', 'PPC', 'Período'])

    for (curso, ppc, periodo), grupo in grupos:
        # Criar uma nova planilha
        wb = Workbook()
        ws = wb.active
        ws.title = f'{curso}_{periodo}'

        # Adicionar cabeçalho
        ws['A1'] = f'{curso} {ppc} {periodo}'
        ws['A2'] = 'Horário (dia + turno + horário concatenados)'
        ws['B2'] = 'Código + Nome da Disciplina + Carga Horária + Professor'

        # Definir a largura das colunas
        ws.column_dimensions['A'].width = 35
        ws.column_dimensions['B'].width = 100

        # Estilo para as células
        for cell in ws["1:2"]:
            for c in cell:
                c.alignment = Alignment(horizontal="center", vertical="center")

        # Preencher as células com os dados
        row_idx = 3
        for _, row in grupo.iterrows():
            dia = row['Dia']
            turno = row['Turno']
            horario = row['Horário']
            codigo = row['Código']
            disciplina = row['Disciplina']
            carga_horaria = row['CH']
            professor = row['Professor']

            # Adicionar o horário formatado
            horario_formatado = get_horario(dia, turno, horario)

            # Concatenar a descrição do código + nome da disciplina + carga horária + professor
            descricao = f"{codigo} {disciplina} {carga_horaria} {professor}"

            # Adicionar os dados na planilha
            ws[f'A{row_idx}'] = horario_formatado
            ws[f'B{row_idx}'] = descricao

            row_idx += 1

        # Salvar a planilha
        nome_arquivo = f"alunos (importar)/{curso}_{periodo}.xlsx"
        wb.save(nome_arquivo)

# Chamar a função para gerar as planilhas
gerar_planilhas()

print("Planilhas de alunos geradas com sucesso!")