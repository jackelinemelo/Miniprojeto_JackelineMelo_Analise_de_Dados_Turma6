import re
import numpy as np
import pandas as pd
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

    texto = re.sub(r"[^\d,.\-]", "", texto)  
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

    print("\n### SPRINT 2 CONCLUÍDA ####")