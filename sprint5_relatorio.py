import re
import pandas as pd
import matplotlib.pyplot as plt

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