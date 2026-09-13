#Sprint 1 (Importação dos dados)
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('Base Varejo.csv', sep=';', encoding='utf-8')


print(f"Número de registros (linhas): {df.shape[0]}")
print(f"Número de colunas: {df.shape[1]}")
print("\nTipos de dados por coluna:")
print(df.dtypes)

# Sprint 2 (Transformação dos dados)
from datetime import datetime

pd.set_option("display.width", 120)

MARCADORES_NULOS = {"#N/D", "#N/A", "NA", "N/A", "NULL", "NAN", "-", ""}

def limpar_texto(valor, maiusculas=True, debug=False):
  
    if debug:
        print(f"  [limpar_texto] entrada bruta: {valor!r}")

    if pd.isnull(valor):
        if debug:
            print("  [limpar_texto] valor nulo (NaN) -> retorna NaN")
        return np.nan

    texto = str(valor).strip()
    if debug:
        print(f"  [limpar_texto] após strip()       : {texto!r}")

   
    if texto.upper() in MARCADORES_NULOS:
        if debug:
            print(f"  [limpar_texto] é marcador de nulo ({texto!r}) -> retorna NaN")
        return np.nan

    texto = re.sub(r"\s+", " ", texto)                 
    if debug:
        print(f"  [limpar_texto] espaços normalizados: {texto!r}")

    texto = re.sub(r"[^\w\sÀ-ÿ]", "", texto)            
    if debug:
        print(f"  [limpar_texto] pontuação removida  : {texto!r}")

    correcoes_conhecidas = {
        r"\bLIMaO\b": "LIMAO",
    }
    for padrao, substituto in correcoes_conhecidas.items():
        antes = texto
        texto = re.sub(padrao, substituto, texto)
        if debug and antes != texto:
            print(f"  [limpar_texto] encoding corrigido  : {antes!r} -> {texto!r}")

    texto = texto.strip()
    if texto == "" or texto.upper() in MARCADORES_NULOS:
        if debug:
            print("  [limpar_texto] ficou vazio/nulo após limpeza -> retorna NaN")
        return np.nan

    resultado = texto.upper() if maiusculas else texto.lower()
    if debug:
        print(f"  [limpar_texto] resultado final     : {resultado!r}")
    return resultado

def limpar_inteiro(valor, debug=False):
    if debug:
        print(f"  [limpar_inteiro] entrada bruta: {valor!r}")

    if pd.isnull(valor):
        if debug:
            print("  [limpar_inteiro] valor nulo (NaN) -> retorna NaN")
        return np.nan
    if isinstance(valor, (int, np.integer)):
        if debug:
            print(f"  [limpar_inteiro] já é int -> retorna {int(valor)}")
        return int(valor)
    if isinstance(valor, float) and valor.is_integer():
        if debug:
            print(f"  [limpar_inteiro] float inteiro -> retorna {int(valor)}")
        return int(valor)

    texto = str(valor).strip()
    if debug:
        print(f"  [limpar_inteiro] após strip()        : {texto!r}")

    if texto.upper() in MARCADORES_NULOS:
        if debug:
            print(f"  [limpar_inteiro] é marcador de nulo -> retorna NaN")
        return np.nan

    texto = re.sub(r"(?<=\d)\.(?=\d{3}\b)", "", texto)
    if debug:
        print(f"  [limpar_inteiro] sem separador milhar: {texto!r}")

    texto_limpo = re.sub(r"[^\d\-]", "", texto)  
    if debug:
        print(f"  [limpar_inteiro] só dígitos/sinal    : {texto_limpo!r}")

    if texto_limpo in ("", "-"):
        if debug:
            print("  [limpar_inteiro] nada restou -> retorna NaN")
        return np.nan
    try:
        resultado = int(texto_limpo)
        if debug:
            print(f"  [limpar_inteiro] resultado final     : {resultado}")
        return resultado
    except ValueError:
        if debug:
            print("  [limpar_inteiro] falha na conversão -> retorna NaN")
        return np.nan

def limpar_decimal(valor, debug=False):
    if debug:
        print(f"  [limpar_decimal] entrada bruta: {valor!r}")

    if pd.isnull(valor):
        if debug:
            print("  [limpar_decimal] valor nulo (NaN) -> retorna NaN")
        return np.nan
    if isinstance(valor, (int, float, np.integer, np.floating)):
        if debug:
            print(f"  [limpar_decimal] já é numérico -> retorna {float(valor)}")
        return float(valor)

    texto = str(valor).strip()
    if debug:
        print(f"  [limpar_decimal] após strip()         : {texto!r}")

    if texto.upper() in MARCADORES_NULOS:
        if debug:
            print("  [limpar_decimal] é marcador de nulo -> retorna NaN")
        return np.nan

    texto = re.sub(r"[^\d,.\-]~ ´", "", texto)  
    if debug:
        print(f"  [limpar_decimal] símbolos removidos   : {texto!r}")
    if texto in ("", "-"):
        if debug:
            print("  [limpar_decimal] nada restou -> retorna NaN")
        return np.nan

    tem_virgula = "," in texto
    tem_ponto = "." in texto

    if tem_virgula and tem_ponto:
        if texto.rfind(",") > texto.rfind("."):
            texto = texto.replace(".", "").replace(",", ".")
            if debug:
                print(f"  [limpar_decimal] formato BR detectado : {texto!r}")
        else:
            texto = texto.replace(",", "")
            if debug:
                print(f"  [limpar_decimal] formato intl detectado: {texto!r}")
    elif tem_virgula:
        texto = texto.replace(",", ".")
        if debug:
            print(f"  [limpar_decimal] vírgula -> ponto      : {texto!r}")

    try:
        resultado = float(texto)
        if debug:
            print(f"  [limpar_decimal] resultado final       : {resultado}")
        return resultado
    except ValueError:
        if debug:
            print("  [limpar_decimal] falha na conversão -> retorna NaN")
        return np.nan

def limpar_data(valor, debug=False):
    if debug:
        print(f"  [limpar_data] entrada bruta: {valor!r}")

    if pd.isnull(valor):
        if debug:
            print("  [limpar_data] valor nulo -> retorna NaT")
        return pd.NaT
    if isinstance(valor, (pd.Timestamp, datetime)):
        if debug:
            print(f"  [limpar_data] já é datetime -> retorna {valor}")
        return pd.Timestamp(valor)

    texto = str(valor).strip()
    if debug:
        print(f"  [limpar_data] após strip()   : {texto!r}")

    if texto.upper() in MARCADORES_NULOS:
        if debug:
            print("  [limpar_data] é marcador de nulo -> retorna NaT")
        return pd.NaT

    padroes = [
        (r"^\d{2}/\d{2}/\d{4}$", "%d/%m/%Y"),
        (r"^\d{2}-\d{2}-\d{4}$", "%d-%m-%Y"),
        (r"^\d{4}-\d{2}-\d{2}$", "%Y-%m-%d"),
        (r"^\d{2}/\d{2}/\d{2}$", "%d/%m/%y"),
    ]
    for regex, formato in padroes:
        if re.match(regex, texto):
            if debug:
                print(f"  [limpar_data] padrão casado  : {regex!r} -> formato {formato!r}")
            try:
                resultado = pd.to_datetime(texto, format=formato)
                if debug:
                    print(f"  [limpar_data] resultado final: {resultado}")
                return resultado
            except ValueError:
                if debug:
                    print("  [limpar_data] falha ao converter -> retorna NaT")
                return pd.NaT

    if debug:
        print("  [limpar_data] nenhum padrão bateu -> tentando fallback do pandas")
   
    resultado = pd.to_datetime(texto, errors="coerce", dayfirst=True)
    if debug:
        print(f"  [limpar_data] resultado do fallback: {resultado}")
    return resultado

def _rodar_testes():
    print("=" * 70)
    print("TESTES - limpar_texto")
    print("=" * 70)
    casos_texto = [
        "  refrigerante   guarana  ",
        "REFRIGERANTE LIMaO",
        "#N/D",
        "Açaí!!! (250ml)",
        None,
    ]
    print(">>> Exemplo passo a passo (debug=True) com o primeiro caso:")
    limpar_texto(casos_texto[0], debug=True)
    print("\n>>> Resultado resumido de todos os casos:")
    for caso in casos_texto:
        print(f"{caso!r:35s} -> {limpar_texto(caso)!r}")

    print("\n" + "=" * 70)
    print("TESTES - limpar_inteiro")
    print("=" * 70)
    casos_inteiro = [" 1.234 ", "42", "abc", "-15", "", None, 99.0]
    print(">>> Exemplo passo a passo (debug=True) com o primeiro caso:")
    limpar_inteiro(casos_inteiro[0], debug=True)
    print("\n>>> Resultado resumido de todos os casos:")
    for caso in casos_inteiro:
        print(f"{caso!r:15s} -> {limpar_inteiro(caso)!r}")

    print("\n" + "=" * 70)
    print("TESTES - limpar_decimal")
    print("=" * 70)
    casos_decimal = ["R$ 1.234,56", "1234.56", "12,5", "1.234", "", None, "abc"]
    print(">>> Exemplo passo a passo (debug=True) com o primeiro caso:")
    limpar_decimal(casos_decimal[0], debug=True)
    print("\n>>> Resultado resumido de todos os casos:")
    for caso in casos_decimal:
        print(f"{caso!r:15s} -> {limpar_decimal(caso)!r}")

    print("\n" + "=" * 70)
    print("TESTES - limpar_data")
    print("=" * 70)
    casos_data = ["01/02/2019", "2019-02-01", "01-02-2019", "01/02/19", "", None, "31/13/2019"]
    print(">>> Exemplo passo a passo (debug=True) com o primeiro caso:")
    limpar_data(casos_data[0], debug=True)
    print("\n>>> Resultado resumido de todos os casos:")
    for caso in casos_data:
        print(f"{caso!r:15s} -> {limpar_data(caso)}")


def _aplicar_na_base(caminho="Base Varejo.csv"):
    print("\n" + "=" * 70)
    print("APLICAÇÃO DAS FUNÇÕES NA BASE VAREJO.CSV")
    print("=" * 70)

    print(f"[Etapa 0] Carregando arquivo: {caminho}")
    df = pd.read_csv(caminho, sep=";", encoding="utf-8")
    df = df.drop(columns=[c for c in df.columns if "Unnamed" in c])
    print(f"[Etapa 0] Base carregada -> {df.shape[0]} linhas, {df.shape[1]} colunas")
    print("[Etapa 0] Amostra ANTES de qualquer limpeza:")
    print(df.head(3))


    print("\n[Etapa 1] Convertendo coluna DATA (str -> datetime)...")
    print(f"[Etapa 1] Tipo ANTES : {df['DATA'].dtype} | exemplo: {df['DATA'].iloc[0]!r}")
    df["DATA"] = df["DATA"].apply(limpar_data)
    print(f"[Etapa 1] Tipo DEPOIS: {df['DATA'].dtype} | exemplo: {df['DATA'].iloc[0]}")
    print(f"[Etapa 1] DATA convertida -> nulos gerados: {df['DATA'].isnull().sum()}")
    print("[Etapa 1] Concluída.")

    
    print("\n[Etapa 2] Limpando colunas de texto (CL_GENERO, CL_SEG, PR_CAT, PR_NOME)...")
    for col in ["CL_GENERO", "CL_SEG", "PR_CAT", "PR_NOME"]:
        print(f"\n  -> Processando coluna: {col}")
        antes_nulos = (df[col].astype(str).str.upper().isin(MARCADORES_NULOS)).sum()
        exemplo_antes = df[col].iloc[0]
        df[col] = df[col].apply(limpar_texto)
        exemplo_depois = df[col].iloc[0]
        depois_nulos = df[col].isnull().sum()
        print(f"     exemplo: {exemplo_antes!r} -> {exemplo_depois!r}")
        print(f"     nulos textuais tratados: {antes_nulos} | nulos após limpeza: {depois_nulos}")
    print("[Etapa 2] Concluída.")

    print("\n[Etapa 2.1] Verificando correção de encoding (LIMaO -> LIMAO):")
    print(df.loc[df["PR_NOME"] == "LIMAO", "PR_NOME"].value_counts())


    print("\n[Etapa 3] Revalidando colunas inteiras (CO_ID, CL_ID, CL_EC, CL_FHL, PR_ID)...")
    for col in ["CO_ID", "CL_ID", "CL_EC", "CL_FHL", "PR_ID"]:
        antes_dtype = df[col].dtype
        df[col] = df[col].apply(limpar_inteiro)
        print(f"  -> {col:8s}: dtype antes={antes_dtype} | dtype depois={df[col].dtype} "
              f"| nulos gerados={df[col].isnull().sum()}")
    print("[Etapa 3] Concluída.")

    print("\n[Etapa 4] Amostra DEPOIS de toda a limpeza:")
    print(df.head(3))

    return df

if __name__ == "__main__":
    print("### INICIANDO SPRINT 2 - TRANSFORMAÇÃO DE STRINGS, INTEIRO, FLOAT E DATETIME ###\n")

    print(">>> PARTE 1: Testes unitários das funções de limpeza\n")
    _rodar_testes()

    print("\n>>> PARTE 2: Aplicação das funções na base real\n")
    df_limpo = _aplicar_na_base()

    print("\n>>> PARTE 3: Resultado final")
    print("\nBase final pronta para as próximas sprints (agregações/análises).")
    print(df_limpo.dtypes)

    print("\n### SPRINT 2 CONCLUÍDA ###")

    #Sprint 3 (Limpeza de Nulos e Duplicatas)

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

#Sprint 4 (Estatística Descritiva)
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

# Sprint 5 ((Relatório e Documentação)

pd.set_option("display.width", 120)


def carregar_base(caminho="Base Varejo.csv"):
    df = pd.read_csv(caminho, sep=";", encoding="utf-8")
    df = df.drop(columns=[c for c in df.columns if "Unnamed" in c])
    df["DATA_dt"] = pd.to_datetime(df["DATA"], format="%d/%m/%Y")
    return df


def gerar_paineis(df, caminho_saida="painel_insights_base_varejo.pdf"):
    fig, eixos = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle("Base_Varejo.csv - Principais Insights", fontsize=16, fontweight="bold")

    # ------------------------------------------------------------------
    # 1. Volume mensal de registros (sazonalidade / possível truncamento)
    # ------------------------------------------------------------------
    volume_mensal = df["DATA_dt"].dt.to_period("M").value_counts().sort_index()
    ax = eixos[0, 0]
    ax.plot(volume_mensal.index.astype(str), volume_mensal.values, color="#2563eb", linewidth=1.5)
    ax.axhline(volume_mensal.mean(), color="gray", linestyle="--", linewidth=1, label="Média mensal")
    ax.set_title("1. Volume de registros por mês")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Nº de linhas (itens)")
    ax.set_xticks(ax.get_xticks()[::4])
    ax.tick_params(axis="x", rotation=90)
    ax.legend(fontsize=8)

    # ------------------------------------------------------------------
    # 2. Distribuição de itens por compra (tamanho de cesta)
    # ------------------------------------------------------------------
    itens_por_compra = df.groupby("CO_ID").size()
    ax = eixos[0, 1]
    ax.hist(itens_por_compra, bins=30, color="#16a34a", edgecolor="white")
    ax.axvline(itens_por_compra.mean(), color="black", linestyle="--", linewidth=1,
               label=f"Média = {itens_por_compra.mean():.0f}")
    ax.set_title("2. Distribuição do tamanho da cesta")
    ax.set_xlabel("Itens por compra (CO_ID)")
    ax.set_ylabel("Nº de compras")
    ax.legend(fontsize=8)

    # ------------------------------------------------------------------
    # 3. Duplicatas: linhas únicas vs. duplicadas
    # ------------------------------------------------------------------
    duplicadas = df.drop(columns="DATA_dt").duplicated().sum()
    unicas = len(df) - duplicadas
    ax = eixos[0, 2]
    ax.pie(
        [unicas, duplicadas],
        labels=["Linhas únicas", "Linhas duplicadas"],
        autopct="%1.1f%%",
        colors=["#93c5fd", "#f87171"],
        startangle=90,
    )
    ax.set_title("3. Proporção de linhas duplicadas")

    # ------------------------------------------------------------------
    # 4. Número de filhos dos clientes (CL_FHL, nível cliente)
    # ------------------------------------------------------------------
    filhos_por_cliente = df.drop_duplicates(subset="CL_ID")["CL_FHL"].value_counts().sort_index()
    ax = eixos[1, 0]
    ax.bar(filhos_por_cliente.index.astype(str), filhos_por_cliente.values, color="#f59e0b")
    ax.set_title("4. Nº de filhos por cliente (CL_FHL)")
    ax.set_xlabel("Número de filhos")
    ax.set_ylabel("Nº de clientes")

    # ------------------------------------------------------------------
    # 5. Itens vendidos por categoria x gênero
    # ------------------------------------------------------------------
    pivot = pd.pivot_table(
        df, index="PR_CAT", columns="CL_GENERO", values="PR_ID", aggfunc="count", fill_value=0
    ).sort_values("F", ascending=False)
    ax = eixos[1, 1]
    x = range(len(pivot.index))
    largura = 0.35
    ax.bar([i - largura / 2 for i in x], pivot["F"], width=largura, label="F", color="#ec4899")
    ax.bar([i + largura / 2 for i in x], pivot["M"], width=largura, label="M", color="#3b82f6")
    ax.set_xticks(list(x))
    ax.set_xticklabels(pivot.index, rotation=45, ha="right")
    ax.set_title("5. Itens vendidos por categoria x gênero")
    ax.set_ylabel("Nº de itens")
    ax.legend()

    # ------------------------------------------------------------------
    # 6. Registros com produto não identificado (#N/D) ao longo do tempo
    # ------------------------------------------------------------------
    nao_id_mensal = (
        df[df["PR_CAT"] == "#N/D"]["DATA_dt"].dt.to_period("M").value_counts().sort_index()
    )
    ax = eixos[1, 2]
    ax.bar(nao_id_mensal.index.astype(str), nao_id_mensal.values, color="#6b7280")
    ax.set_title("6. Registros '#N/D' por mês")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Nº de registros")
    ax.set_xticks(ax.get_xticks()[::4])
    ax.tick_params(axis="x", rotation=90)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(caminho_saida, dpi=150, bbox_inches="tight")
    print(f"Painel salvo em: {caminho_saida}")
    plt.close(fig)


if __name__ == "__main__":
    df = carregar_base()
    gerar_paineis(df)