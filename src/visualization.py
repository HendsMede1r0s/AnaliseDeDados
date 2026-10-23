"""Funções de visualização usadas nos notebooks do projeto."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def obter_pasta_de_graficos() -> Path:
    """Retorna e cria, se necessário, a pasta de figuras do projeto."""
    pasta_graficos = Path(__file__).resolve().parent.parent / "reports" / "figures"
    pasta_graficos.mkdir(parents=True, exist_ok=True)
    return pasta_graficos


def plotar_distribuicao_nulos(tabela: pd.DataFrame) -> None:
    """Exibe um mapa de calor com a localização dos valores ausentes."""
    plt.figure(figsize=(12, 6))
    sns.heatmap(tabela.isna(), cbar=False, cmap="viridis", yticklabels=False)
    plt.title("Mapa de Calor - Distribuição de Valores Nulos", fontsize=14)
    plt.tight_layout()
    plt.show()


def plotar_matriz_de_correlacao(tabela: pd.DataFrame, nome_da_imagem: str = "matriz_correlacao.png") -> Path:
    """Exibe e salva a matriz de correlação das colunas numéricas."""
    if not isinstance(tabela, pd.DataFrame):
        raise TypeError("tabela deve ser um pandas.DataFrame.")
    correlacao = tabela.corr(numeric_only=True)
    if correlacao.empty:
        raise ValueError("A tabela não possui colunas numéricas para correlacionar.")

    plt.figure(figsize=(14, 10))
    sns.heatmap(correlacao, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Matriz de Correlação entre Variáveis Numéricas", fontsize=14)
    plt.tight_layout()
    caminho = obter_pasta_de_graficos() / nome_da_imagem
    plt.savefig(caminho, bbox_inches="tight", dpi=300)
    plt.show()
    return caminho
