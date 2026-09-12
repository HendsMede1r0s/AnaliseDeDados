"""Funções reutilizáveis para a análise exploratória dos dados."""

from collections.abc import Iterable

import pandas as pd
from pandas.api.types import is_numeric_dtype


def _validar_tabela(tabela: pd.DataFrame) -> None:
    if not isinstance(tabela, pd.DataFrame):
        raise TypeError("tabela deve ser um pandas.DataFrame.")


def resumir_valores_ausentes(tabela: pd.DataFrame) -> pd.DataFrame:
    """Retorna quantidade e porcentagem de valores ausentes por coluna."""
    _validar_tabela(tabela)
    contagem_nulos = tabela.isna().sum()
    percentual_nulos = contagem_nulos.div(len(tabela)).mul(100) if len(tabela) else contagem_nulos.astype(float)
    resumo = pd.DataFrame({"Valores Ausentes": contagem_nulos, "Porcentagem (%)": percentual_nulos})
    return resumo.loc[resumo["Valores Ausentes"] > 0].sort_values(by="Porcentagem (%)", ascending=False)


def identificar_outliers_iqr(tabela: pd.DataFrame, colunas: Iterable[str]) -> dict[str, list[object]]:
    """Identifica, por coluna, os índices de outliers pelo método IQR.

    Colunas ausentes ou não numéricas são ignoradas, pois não permitem o
    cálculo do IQR.
    """
    _validar_tabela(tabela)
    if isinstance(colunas, str):
        colunas = [colunas]

    outliers_por_coluna: dict[str, list[object]] = {}
    for coluna in colunas:
        if coluna not in tabela.columns or not is_numeric_dtype(tabela[coluna]):
            continue
        serie = tabela[coluna].dropna()
        if serie.empty:
            outliers_por_coluna[coluna] = []
            continue
        primeiro_quartil, terceiro_quartil = serie.quantile([0.25, 0.75])
        iqr = terceiro_quartil - primeiro_quartil
        limite_inferior = primeiro_quartil - 1.5 * iqr
        limite_superior = terceiro_quartil + 1.5 * iqr
        mascara = (tabela[coluna] < limite_inferior) | (tabela[coluna] > limite_superior)
        outliers_por_coluna[coluna] = tabela.index[mascara].tolist()
    return outliers_por_coluna
