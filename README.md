# Cenário 05 - Otimização de Programação de Horários Acadêmicos


## Descrição do Cenário

O Problema de Agendamento Acadêmico (Academic Scheduling Problem), aborda a definição de horários de
instituições de ensino como escolas, colégios, faculdades e universidades. A cada novo período letivo, gestores
de curso precisam definir os horários das aulas, sendo que o desafio está em se conciliar os conflitos de horários
das turmas e dos professores, além das limitações de recursos organizacionais (ex. quantidade de salas e de
LDCs).

O Problema de Programação de Horários em Escolas (School Timetabling Problem, STP), também conhecido por
professor/turma, é uma subcategoria do Agendamento Acadêmico. Seu objetivo é associar cada disciplina a
algum horário, evitando conflitos como um professor estar associado a mais de uma turma no mesmo horário, ou
que as turmas não estejam associadas a mais de uma aula por horário, entre outros.

Nos cursos de Sistemas de Informação (SIN) e Ciência da Computação (CCO) do Instituto de Matemática e
Computação da UNIFEI a alocação das disciplinas de SIN ou CCO para um professor e a definição do seu horário
de oferta é uma atribuição dos coordenadores de curso. Uma vez que as disciplinas foram alocadas para os
professores é necessário definir seu dia e horário de oferta.

A definição dos horários acadêmicos das disciplinas dos cursos de Sistemas de Informação e de Ciência da
Computação demanda um tempo significativo dos coordenadores. **Visando reduzir o tempo necessário para essa
tarefa, o objetivo é o desenvolvimento de uma solução para criação de uma grade de horários.**

## Participantes do Projeto

- Luara do Val Perielli
- Matheus Luz de Faria
- Pedro De Paula Goncalves
- Pedro Nogueira Barboza

## Estrutura de pastas e arquivos do projeto

    ├── datasets 
    │   ├── csv # Arquivos CSV do primeiro e segundo semestre
    │   ├── pdf # Dataset Fornecido para elaboração do projeto
    │   └── tabelas-convertidas # Arquivos CSV convertidos para pdf
    ├── docs
    │   └── diretrizesProjeto.pdf  # Contém enunciado do problema
    ├── src
    │   ├── classes # Contém a classe Disciplina que é um nó utilizado para a construção do grafo
    │   ├── aluno # Contém saída do programa com alocação das disciplinas por turma
    │   ├── professor # Contém saída do programa com alocação das disciplinas por professor
    │   ├── controle # Contém saída do programa com alocação das disciplinas por turma e professor
    │   ├── grafo_disciplina_curso.png # Imagem do grafo de disciplinas e professores
    │   ├── grafo_restricoes.png # Imagem do grafo de coloração de disciplinas
    │   ├── utils 
    │   │   └── conversorCsvParaPdf.py # Converte arquivos CSV para PDF e coloca na pasta datasets/tabelas-convertidas
    │   └── main.py 
    ├── .tool-versions # Versão do Python utilizada no projeto 
    ├── requirements.txt # Bibliotecas utilizadas no projeto
    └── .gitignore # Arquivos que não devem ser enviados para o repositório

## Bibliotecas Utilizadas e suas funções

- **csv**:  ler e gravar arquivos no formato CSV
- **os**: manipulação de caminhos de arquivos e diretórios
- **random**:  é usada para gerar números ou sequências aleatórias. No código, ela é empregada na função fazerDivisaoHorario
- **logging:** Registra erros e eventos do sistema, facilitando a depuração e monitoramento do processo de agendamento.
- **networkx:** Criação e manipulação de grafos para modelar as relações entre disciplinas e professores.
- **matplotlib.pyplot:** Visualização de grafos gerados com NetworkX.
- **collections.defaultdict:** Estrutura de dados para armazenar dicionários com valores padrão, útil para organizar horários e restrições.
- **typing:** Tipagem estática para melhor legibilidade e manutenção do código.
- **openpyxl:** Manipulação de arquivos Excel para exportação dos horários.
- **openpyxl.styles:** Estilização de células em planilhas Excel, permitindo formatação personalizada dos horários.
- **classes.Disciplina:** Classe personalizada que representa uma disciplina acadêmica com atributos como nome, código, carga horária, professores, etc.


## Funções do Arquivo Principal `main.py`

### Funções de Verificação de Restrições

- **verificar_restricoes_professor**: Garante que nenhum professor tenha múltiplas disciplinas no mesmo horário.
- **verificar_restricoes_turma**: Assegura que nenhuma turma tenha múltiplas disciplinas no mesmo horário.
- **verificar_restricoes_curso**: Verifica restrições de horários específicas para cursos como SIN e CCO.

### Funções de Criação e Salvamento de Grafos

- **criar_grafo_disciplina_curso**: Cria um grafo relacionando disciplinas e professores.
- **criar_grafo_coloracao_restricoes**: Cria um grafo representando as restrições de agendamento entre disciplinas.
- **salvar_grafo_como_imagem**: Salva a visualização do grafo como uma imagem PNG.

### Funções de Exportação de Horários

- **exportar_horarios**: Exporta os horários gerados para arquivos CSV organizados por professores, alunos e um horário global.

### Funções de Carregamento e Criação de Lista de Adjacência

- **carregarDisciplinasCsv**: Carrega disciplinas de um arquivo CSV e retorna uma lista de objetos `Disciplina`.
- **criarListaAdjacencia**: Gera uma lista de adjacência conectando disciplinas relacionadas.

### Funções de Coloração de Grafo

- **colorirGrafoDSatur**: Aplica o algoritmo DSatur para colorir o grafo de disciplinas.
- **colorirGrafo**: Aplica um método básico de coloração para evitar conflitos no grafo.

### Funções de Criação de Grafos para Turmas e Divisão de Horários

- **criarGrafoTurmas**: Cria um grafo conectando disciplinas da mesma turma.
- **fazerDivisaoHorario**: Aloca disciplinas em horários específicos com base em suas cores no grafo.

### Funções Auxiliares

- **logicalXOR**: Retorna `True` se apenas uma das duas condições fornecidas for verdadeira.
- **exibirHorariosPorTurma**: Exibe os horários organizados por turma no console.

### Funções de Geração de Planilhas

- **gerar_planilha_horarios**: Gera planilhas Excel de horários para professores ou alunos a partir de arquivos CSV.

## Classes Implementadas

- **Disciplina**: Classe que representa um nó do grafo
  - **self.indice**: Índice da disciplina **(int)**
  - **self.codigo**: Código da disciplina **(str)**
  - **self.nome**: Nome da disciplina **(str)**
  - **self.curso**: Curso da disciplina **(str)**
  - **self.ppc**: PPC da disciplina **(str)**
  - **self.periodo**: Período da disciplina **(str)**
  - **self.ch**: Carga horária da disciplina **(int)**
  - **self.professores**: Lista de professores que ministram a disciplina **List[int]** (armazena o número do professor correspondente. Ex: Professor 1, Professor 2, Professor 3 => `[1, 2, 3]`)
  - **self.turma**: Curso + PPC + '.' + período **(str)**
  - **self.cor**: Cor da disciplina **(int)**


## Classes Implementadas

- **Disciplina**: Classe que representa um nó do grafo
  - **self.indice:** índice da disciplina **(int)**
  - **self.codigo:** código da disciplina **(str)**
  - **self.nome:** nome da disciplina **(str)**
  - **self.curso:** curso da disciplina **(str)**
  - **self.ppc:** ppc da disciplina **(str)**
  - **self.periodo:** período da disciplina **(str)**
  - **self.ch:** carga horária da disciplina **(int)**
  - **self.professores:** lista de professores que ministram a disciplina **Array[int]** (armazena o número do professor correspondentem. Ex: Professor 1, Professor 2, Professor 3 => [1, 2, 3]) 
  - **self.turma:** curso + ppc + '.' + periodo **(str)**
  - **self.cor:** cor da disciplina **(int)**  


## Como rodar o projeto 

```bash
# Instale as dependências do projeto
$ pip install -r requirements.txt

# Selecione o diretório src
$ cd src

# Execute o arquivo main.py
$ python main.py
```
O projeto foi testado tanto em ambientes Windows quanto Linux, utilizando Python 3.12.3. Verifique se a sua versão do Python é compatível com o projeto.

## Saída Esperada 

- Ao rodar o código você terá o resultado da alocação das disciplinas em horários específicos, evitando conflitos de horários entre professores e turmas. Na pasta aluno você terá arquivos csv e xlsx com alocação de disciplinas por turma. Na pasta professor haverá arquivos csv e xlsx com alocação de disciplinas por professor. Na pasta controle haverá os horários de todas as turmas em um único arquivo csv e xlsx.
