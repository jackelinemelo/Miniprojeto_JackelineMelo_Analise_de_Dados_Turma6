import pandas as pd
import numpy as np

# TRÊS ETAPAS DE LIMPEZA
df = pd.read_csv('Base Varejo.csv', na_values=['#N/D'])
print("--- RELATÓRIO DE QUALIDADE DOS DADOS ---\n")

print("1. VALORES NULOS POR COLUNA:")
nulos = df.isnull().sum()
print(nulos[nulos > 0] if nulos.sum() > 0 else "Nenhum valor nulo encontrado.")
print("-" * 40)

print("2. REGISTROS DUPLICADOS:")
total_duplicadas = df.duplicated().sum()
print(f"Total de linhas completamente duplicadas: {total_duplicadas}")
print("-" * 40)

print("3. POSSÍVEIS INCONSISTÊNCIAS:")

vazios_string = (df == '#N/D').sum().sum()
print(f"Ocorrências da string '#N/D' restante na base: {vazios_string}")

if 'Data' in df.columns:
    datas_convertidas = pd.to_datetime(df['Data'], errors='coerce')
    datas_invalidas = datas_convertidas.isnull().sum() - df['Data'].isnull().sum()
    print(f"Datas em formato inválido/corrompido: {datas_invalidas}")

print(f"Dimensões originais: {df.shape[0]} linhas, {df.shape[1]} colunas\n")

if 'Categoria' in df.columns:
    df['Categoria'] = df['Categoria'].fillna('Não Informado')
if 'Preço' in df.columns:
    df['Preço'] = df['Preço'].fillna(df['Preço'].median())
print(f"Após tratamento de nulos/limpeza final: {df.shape[0]} linhas")

df = df.drop_duplicates()
print(f"Após remover duplicatas: {df.shape[0]} linhas")

if 'Data' in df.columns:
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
    
if 'ID_Cliente' in df.columns:
    df['ID_Cliente'] = df['ID_Cliente'].astype(str)

df.to_csv('Base_Varejo_Limpo.csv', index=False)
print("\nBase 'Base_Varejo_Limpo.csv' salva com sucesso!")


# VALIDAÇÃO IDENTIFICADOR COMPRAS (CO_ID)

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 20)


def carregar_base(caminho="Base_Varejo_Limpo.csv"):
    df = pd.read_csv(caminho, sep=";", encoding="utf-8")
    df = df.drop(columns=[c for c in df.columns if "Unnamed" in c])
    return df

def validar_repeticao_co_id(df):
    print("=" * 70)
    print("1. CO_ID SE REPETE POR VÁRIAS LINHAS (ITEM, NÃO COMPRA)")
    print("=" * 70)

    total_linhas = len(df)
    total_compras = df["CO_ID"].nunique()
    itens_por_compra = df.groupby("CO_ID").size()

    print(f"Total de linhas (itens)   : {total_linhas}")
    print(f"Total de CO_ID únicos     : {total_compras}")
    print(f"Linhas != CO_IDs únicos?  : {'SIM -> confirma 1 linha = 1 item' if total_linhas != total_compras else 'NÃO'}")
    print("\nDistribuição de itens por compra (describe):")
    print(itens_por_compra.describe())
    print(f"\nCompras com apenas 1 item : {(itens_por_compra == 1).sum()}")
    print(f"Compras com mais de 1 item: {(itens_por_compra > 1).sum()} "
          f"({(itens_por_compra > 1).mean():.1%} das compras)")

    co_id_exemplo = itens_por_compra[itens_por_compra > 5].index[0]
    print(f"\nExemplo concreto -> CO_ID={co_id_exemplo} tem "
          f"{itens_por_compra[co_id_exemplo]} linhas (itens):")
    print(df[df["CO_ID"] == co_id_exemplo][["DATA", "CO_ID", "CL_ID", "PR_ID", "PR_NOME"]])

    return itens_por_compra

def validar_unicidade_atributos_compra(df):
    print("\n" + "=" * 70)
    print("2. CO_ID IDENTIFICA UMA ÚNICA COMPRA (1 cliente, 1 data)")
    print("=" * 70)

    checagens = {
        "CO_ID -> CL_ID (1 compra deve ter 1 único cliente)": "CL_ID",
        "CO_ID -> DATA  (1 compra deve ter 1 única data)": "DATA",
    }

    todas_ok = True
    for descricao, coluna in checagens.items():
        qtd_valores_distintos = df.groupby("CO_ID")[coluna].nunique()
        inconsistentes = (qtd_valores_distintos > 1).sum()
        ok = inconsistentes == 0
        todas_ok = todas_ok and ok
        status = "OK - regra válida" if ok else f"FALHOU - {inconsistentes} CO_ID(s) inconsistente(s)"
        print(f"{descricao:55s}: {status}")

    print(f"\nConclusão da validação: "
          f"{'CO_ID pode ser usado com segurança como identificador de compra.' if todas_ok else 'CO_ID apresenta inconsistências -- investigar antes de usar como chave de compra.'}")
    return todas_ok

def agrupar_por_compra(df):
    print("\n" + "=" * 70)
    print("3. AGRUPAMENTO DE ITENS POR COMPRA (groupby CO_ID)")
    print("=" * 70)

    compras = (
        df.groupby("CO_ID")
        .agg(
            CL_ID=("CL_ID", "first"),         
            DATA=("DATA", "first"),            
            CL_GENERO=("CL_GENERO", "first"),
            CL_SEG=("CL_SEG", "first"),
            QTD_ITENS=("PR_ID", "size"),       
            QTD_PRODUTOS_DISTINTOS=("PR_ID", "nunique"),
            QTD_CATEGORIAS_DISTINTAS=("PR_CAT", "nunique"),
            CATEGORIAS=("PR_CAT", lambda x: sorted(set(x))),
        )
        .reset_index()
    )

    print(f"Base em nível de ITEM : {df.shape[0]} linhas")
    print(f"Base em nível de COMPRA: {compras.shape[0]} linhas")
    print("\nAmostra da visão por compra:")
    print(compras.head(5))

    print("\nEstatísticas de itens por compra (na visão agrupada):")
    print(compras["QTD_ITENS"].describe())

    print("\nExemplo de uso prático -> Top 5 compras com mais categorias distintas:")
    print(compras.sort_values("QTD_CATEGORIAS_DISTINTAS", ascending=False)
          [["CO_ID", "CL_ID", "QTD_ITENS", "QTD_CATEGORIAS_DISTINTAS", "CATEGORIAS"]]
          .head(5))

    return compras

if __name__ == "__main__":
    df = carregar_base()

    itens_por_compra = validar_repeticao_co_id(df)
    regra_valida = validar_unicidade_atributos_compra(df)
    compras = agrupar_por_compra(df)

    print("\n" + "=" * 70)
    print("RESUMO DA VALIDAÇÃO")
    print("=" * 70)
    print("- Confirmado: cada linha é um ITEM, e CO_ID se repete por compra.")
    print(f"- Regra de unicidade (1 CO_ID = 1 cliente, 1 data): "
          f"{'VÁLIDA' if regra_valida else 'INVÁLIDA - revisar'}")
    print(f"- CO_ID pode ser usado com groupby('CO_ID') para gerar métricas "
          f"em nível de compra (tamanho de cesta, categorias, etc.), "
          f"como demonstrado na seção 3.")

    compras.to_csv("Base_Varejo_por_compra.csv", sep=";", index=False)
    print("\nVisão agrupada por compra salva em 'Base_Varejo_por_compra.csv'")