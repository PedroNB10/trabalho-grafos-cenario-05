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

- Luara
- Matheus
- Pedro De Paula
- Pedro Nogueira

## Estrutura de pastas e arquivos do projeto

    ├── datasets 
    │   ├── csv # Arquivos CSV do primeiro e segundo semestre
    │   ├── pdf # Dataset Fornecido para elaboração do projeto
    │   └── tabelas-convertidas # Arquivos CSV convertidos para pdf
    ├── docs
    │   └── diretrizesProjeto.pdf  # Contém enunciado do problema
    ├── src
    │   ├── classes # Contém a classe Disciplina que é um nó utilizado para a construção do grafo
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



## Funções do arquivo principal main.py

- **logicalXOR:** Verifica se apenas uma das condições fornecidas é verdadeira.
- **carregarDisciplinasCsv:** Lê um arquivo CSV e retorna uma lista de objetos Disciplina.
- **criarListaAdjacencia:** Gera um grafo representado por uma lista de adjacência conectando disciplinas relacionadas.
- **colorirGrafo:** Atribui cores às disciplinas para evitar conflitos em um grafo.
- **criarGrafoTurmas:** Cria um grafo que conecta disciplinas pertencentes à mesma turma.
- **fazerDivisaoHorario:** Aloca disciplinas em horários específicos com base em suas cores no grafo.


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

## Saída Esperada (to do)
