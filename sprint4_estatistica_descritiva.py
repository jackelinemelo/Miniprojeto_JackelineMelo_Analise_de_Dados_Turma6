import pandas as pd

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 20)

def carregar_base(caminho="Base Varejo.csv"):
    df = pd.read_csv(caminho, sep=";", encoding="utf-8")
    df = df.drop(columns=[c for c in df.columns if "Unnamed" in c])
    return df

def estatisticas_filhos(df):
    print("=" * 70)
    print("1. ESTATÍSTICAS DESCRITIVAS - CL_FHL (número de filhos do cliente)")
    print("=" * 70)

    filhos_por_cliente = df.drop_duplicates(subset="CL_ID")["CL_FHL"]

    print(f"Linhas na base (nível item)      : {len(df)}")
    print(f"Clientes únicos (nível cliente)  : {filhos_por_cliente.shape[0]}")

    media = filhos_por_cliente.mean()
    mediana = filhos_por_cliente.median()
    desvio_padrao = filhos_por_cliente.std()
    moda = filhos_por_cliente.mode().tolist()
    maximo = filhos_por_cliente.max()
    minimo = filhos_por_cliente.min()
    contagem = filhos_por_cliente.count()
    quartis = filhos_por_cliente.quantile([0.25, 0.5, 0.75])

    print("\nResumo estatístico (nível cliente):")
    print(f"  Contagem (count)   : {contagem}")
    print(f"  Média              : {media:.3f}")
    print(f"  Mediana            : {mediana:.3f}")
    print(f"  Desvio padrão      : {desvio_padrao:.3f}")
    print(f"  Moda               : {moda}")
    print(f"  Mínimo             : {minimo}")
    print(f"  Máximo             : {maximo}")
    print(f"  Quartil 25% (Q1)   : {quartis[0.25]:.3f}")
    print(f"  Quartil 50% (Q2)   : {quartis[0.50]:.3f}")
    print(f"  Quartil 75% (Q3)   : {quartis[0.75]:.3f}")

    print("\nAtalho com .describe():")
    print(filhos_por_cliente.describe())

    print("\nDistribuição de frequência (quantos clientes por nº de filhos):")
    print(filhos_por_cliente.value_counts().sort_index())

    return filhos_por_cliente


def agrupamento_por_genero(df):
    print("\n" + "=" * 70)
    print("2a. AGRUPAMENTO POR GÊNERO (groupby) - itens e compras")
    print("=" * 70)

    resumo_genero = df.groupby("CL_GENERO").agg(
        QTD_ITENS_VENDIDOS=("PR_ID", "count"),
        QTD_COMPRAS_DISTINTAS=("CO_ID", "nunique"),
        QTD_CLIENTES_DISTINTOS=("CL_ID", "nunique"),
    )
    resumo_genero["ITENS_POR_COMPRA"] = (
        resumo_genero["QTD_ITENS_VENDIDOS"] / resumo_genero["QTD_COMPRAS_DISTINTAS"]
    ).round(2)

    print(resumo_genero)
    genero_mais_itens = resumo_genero["QTD_ITENS_VENDIDOS"].idxmax()
    print(f"\n-> Gênero com mais itens vendidos: {genero_mais_itens}")

    return resumo_genero

def agrupamento_genero_x_categoria(df):
    print("\n" + "=" * 70)
    print("2b. AGRUPAMENTO GÊNERO x CATEGORIA (pivot_table) - itens vendidos")
    print("=" * 70)

    pivot = pd.pivot_table(
        df,
        index="PR_CAT",
        columns="CL_GENERO",
        values="PR_ID",
        aggfunc="count",
        fill_value=0,
        margins=True,
        margins_name="TOTAL",
    )
    print(pivot)

    print("\n-> Categoria mais vendida no total:", pivot["TOTAL"].drop("TOTAL").idxmax())

    return pivot

def agrupamento_segmento_x_genero(df):
    print("\n" + "=" * 70)
    print("2c. AGRUPAMENTO SEGMENTO x GÊNERO (pivot_table) - tamanho médio de compra")
    print("=" * 70)

    compras = df.groupby("CO_ID").agg(
        ITENS=("PR_ID", "count"),
        CL_SEG=("CL_SEG", "first"),
        CL_GENERO=("CL_GENERO", "first"),
    )

    pivot = pd.pivot_table(
        compras,
        index="CL_SEG",
        columns="CL_GENERO",
        values="ITENS",
        aggfunc="mean",
    ).round(2)

    print("Tamanho médio da cesta (itens por compra), por segmento e gênero:")
    print(pivot)

    return pivot


if __name__ == "__main__":
    df = carregar_base()

    estatisticas_filhos(df)
    agrupamento_por_genero(df)
    agrupamento_genero_x_categoria(df)
    agrupamento_segmento_x_genero(df)