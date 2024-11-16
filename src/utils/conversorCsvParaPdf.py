import pandas as pd
import matplotlib.pyplot as plt
import os

def csvParaImagemTabelaUnica(caminhoCsv, caminhoImagem):
    # Lê o arquivo CSV
    df = pd.read_csv(caminhoCsv)

    # Configura a figura do matplotlib
    fig, ax = plt.subplots(
        figsize=(15, len(df) * 0.5)
    )  # Ajusta o tamanho para melhor visualização
    ax.axis("off")  # Oculta os eixos

    # Cria a tabela
    tabela = ax.table(
        cellText=df.values, colLabels=df.columns, cellLoc="center", loc="center"
    )

    # Ajusta as propriedades da tabela para melhor adaptação
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(15)  # Ajusta o tamanho da fonte conforme necessário
    tabela.scale(1.2, 1.2)  # Ajusta a escala para fazer a tabela caber na imagem

    # Ajusta a largura das colunas para caber o conteúdo
    for chave, celula in tabela.get_celld().items():
        indiceLinha, indiceColuna = chave  # Extrai os índices de linha e coluna

        if indiceColuna == 0:
            celula.set_width(0.16)
        elif indiceColuna == 1:
            celula.set_width(0.08)
        elif indiceColuna == 2:
            celula.set_width(0.25)
        elif indiceColuna == 3:
            celula.set_width(0.25)
        elif indiceColuna == 4:
            celula.set_width(0.55)
        elif indiceColuna == 5:
            celula.set_width(0.06)
        elif indiceColuna > 5:
            celula.set_width(0.08)
        else:
            celula.set_width(0.25)  # Define uma largura fixa para todas as células

        celula.set_height(0.04)  # Define uma altura fixa para todas as células

    # Cria o diretório para salvar a imagem
    os.makedirs(os.path.dirname(caminhoImagem), exist_ok=True)

    # Salva a tabela como uma imagem
    plt.savefig(caminhoImagem, bbox_inches="tight", dpi=400, format="pdf")

# Exemplo de uso:
caminhoPdf = os.path.join("..", "..", "datasets","tabelas-convertidas", "semestre2.pdf")
arquivo_csv = 'semestre2.csv'
csvParaImagemTabelaUnica(f"../../datasets/csv/{arquivo_csv}", caminhoPdf)
