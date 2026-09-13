import pandas as pd

df = pd.read_csv('Base Varejo.csv', sep=';', encoding='utf-8')


print(f"Número de registros (linhas): {df.shape[0]}")
print(f"Número de colunas: {df.shape[1]}")
print("\nTipos de dados por coluna:")
print(df.dtypes)