import pandas as pd
import matplotlib.pyplot as plt
import os


def carregar_dados(caminho):
    """
    Carrega os dados de um arquivo CSV em um DataFrame do Pandas.
    """
    return pd.read_csv(caminho)


def inspecao_inicial(df):
    """
    Exibe as primeiras linhas, informações gerais e estatísticas descritivas do DataFrame.
    """
    print("\n--- Primeiras 5 linhas do DataFrame ---")
    print(df.head())

    print("\n--- Informações gerais do DataFrame ---")
    # Imprime um resumo conciso do DataFrame, incluindo tipos de dados e valores não-nulos
    df.info()

    print("\n--- Estatísticas descritivas ---")
    # Gera estatísticas descritivas das colunas numéricas (contagem, média, desvio padrão, min, max, quartis)
    print(df.describe())


def tratamento_valores_ausentes(df):
    """
    Identifica e trata valores ausentes no DataFrame.
    Para este projeto, preenchemos colunas numéricas com a média.
    """
    print("\n--- Valores ausentes por coluna (antes do tratamento) ---")
    print(df.isnull().sum())

    # Seleciona apenas colunas com tipos numéricos (int64, float64)
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns

    for col in numeric_cols:
        # Verifica se a coluna tem valores ausentes antes de tentar preencher
        if df[col].isnull().any():
            df[col].fillna(df[col].mean(), inplace=True)

    print("\nValores ausentes tratados (colunas numéricas preenchidas com a média).")
    print("Verificação de valores ausentes após tratamento:")
    print(df.isnull().sum())


def analise_simples(df):
    """
    Realiza análises estatísticas simples no DataFrame.
    Calcula a média da primeira coluna numérica e a contagem de valores únicos da primeira coluna categórica.
    """
    print("\n--- Análises Simples ---")

    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
    if not numeric_cols.empty:
        coluna_numerica = numeric_cols[0]  # Pega a primeira coluna numérica
        media = df[coluna_numerica].mean()
        print(f"\nMédia da coluna '{coluna_numerica}': {media:.2f}")
    else:
        print("\nNão há colunas numéricas para calcular a média.")

    object_cols = df.select_dtypes(include=["object"]).columns
    if not object_cols.empty:
        coluna_categorica = object_cols[0]  # Pega a primeira coluna categórica
        contagem_unicos = df[coluna_categorica].value_counts()
        print(f"\nContagem de valores únicos na coluna '{coluna_categorica}':")
        print(contagem_unicos)
    else:
        print("\nNão há colunas categóricas para contagem de valores únicos.")


def visualizacao(df):
    """
    Cria e salva gráficos básicos para visualização dos dados:
    - Histograma para a primeira coluna numérica.
    - Gráfico de barras para a primeira coluna categórica.
    Os gráficos são salvos como PNG e também exibidos.
    """
    print("\n--- Gerando Visualizações ---")

    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
    if not numeric_cols.empty:
        coluna_numerica = numeric_cols[0]
        plt.figure(figsize=(10, 5))
        df[coluna_numerica].hist(
            bins=30, edgecolor="black"
        )  # Adiciona borda para melhor visualização das barras
        plt.title(f"Histograma da coluna {coluna_numerica}")
        plt.xlabel(coluna_numerica)
        plt.ylabel("Frequência")
        plt.grid(axis="y", alpha=0.75)
        plt.tight_layout()  # Ajusta o layout para evitar cortar labels
        plt.savefig("histograma.png")
        print(f"Histograma salvo como 'histograma.png'")
        plt.show()  # Exibe o gráfico
    else:
        print("Não há colunas numéricas para gerar histograma.")

    object_cols = df.select_dtypes(include=["object"]).columns
    if not object_cols.empty:
        coluna_categorica = object_cols[0]
        plt.figure(figsize=(10, 5))
        df[coluna_categorica].value_counts().plot(
            kind="bar", color="skyblue"
        )  # Cor para o gráfico de barras
        plt.title(f"Gráfico de barras da coluna {coluna_categorica}")
        plt.xlabel(coluna_categorica)
        plt.ylabel("Contagem")
        plt.xticks(rotation=45, ha="right")  # Gira labels para melhor leitura
        plt.tight_layout()  # Ajusta o layout para evitar cortar labels
        plt.savefig("grafico_barras.png")
        print(f"Gráfico de barras salvo como 'grafico_barras.png'")
        plt.show()  # Exibe o gráfico
    else:
        print("Não há colunas categóricas para gerar gráfico de barras.")


def main():
    """
    Função principal que orquestra o fluxo da Análise Exploratória de Dados (EDA).
    Solicita o caminho do arquivo, carrega, inspeciona, trata valores ausentes,
    realiza análises simples, gera visualizações e salva o DataFrame processado.
    """
    print("--- Iniciando Análise Exploratória de Dados (EDA) ---")
    caminho = input("Digite o caminho do arquivo CSV (ex: titanic.csv): ")

    # Verifica se o arquivo existe antes de tentar carregar
    if not os.path.exists(caminho):
        print(
            f"Erro: O arquivo '{caminho}' não foi encontrado. Verifique o caminho e tente novamente."
        )
        return

    # Tenta carregar o DataFrame, tratando possíveis erros de leitura
    try:
        df = carregar_dados(caminho)
        print(f"\nArquivo '{caminho}' carregado com sucesso.")
    except Exception as e:
        print(
            f"Erro ao carregar o arquivo CSV: {e}\nCertifique-se de que o arquivo é um CSV válido."
        )
        return

    # Realiza as etapas de EDA
    inspecao_inicial(df)
    tratamento_valores_ausentes(df)
    analise_simples(df)
    visualizacao(df)

    # Salva o DataFrame tratado em um novo arquivo CSV, pronto para Power BI ou outras ferramentas
    nome_arquivo_saida_powerbi = "dados_tratados_para_powerbi.csv"
    try:
        # index=False evita que o Pandas salve o índice do DataFrame como uma coluna no CSV
        # encoding='utf-8' garante a compatibilidade com caracteres especiais em diferentes sistemas
        df.to_csv(nome_arquivo_saida_powerbi, index=False, encoding="utf-8")
        print(
            f"\nDataFrame tratado salvo como '{nome_arquivo_saida_powerbi}' para uso externo (ex: Power BI)."
        )
    except Exception as e:
        print(f"Erro ao salvar o arquivo CSV '{nome_arquivo_saida_powerbi}': {e}")


if __name__ == "__main__":
    main()
