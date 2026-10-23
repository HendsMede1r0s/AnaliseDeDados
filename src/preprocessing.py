"""Funções reutilizáveis para o pré-processamento do conjunto de dados."""

from collections.abc import Iterable

import pandas as pd
from pandas.api.types import is_numeric_dtype


def _validar_tabela(tabela: pd.DataFrame) -> None:
    if not isinstance(tabela, pd.DataFrame):
        raise TypeError("tabela deve ser um pandas.DataFrame.")


def filtrar_colunas(tabela: pd.DataFrame, lista_de_colunas: Iterable[str]) -> pd.DataFrame:
    """Retorna uma cópia contendo somente as colunas solicitadas."""
    _validar_tabela(tabela)
    colunas = list(lista_de_colunas)
    colunas_ausentes = [coluna for coluna in colunas if coluna not in tabela.columns]
    if colunas_ausentes:
        raise KeyError(f"Colunas não encontradas: {colunas_ausentes}")
    return tabela.loc[:, colunas].copy()


def transformar_categoricas_em_numeros(
    tabela: pd.DataFrame, colunas: Iterable[str] | None = None
) -> pd.DataFrame:
    """Aplica one-hot encoding em todas ou somente nas colunas indicadas."""
    _validar_tabela(tabela)
    if colunas is None:
        return pd.get_dummies(tabela, drop_first=True, dtype=int)

    colunas = list(colunas)
    colunas_ausentes = [coluna for coluna in colunas if coluna not in tabela.columns]
    if colunas_ausentes:
        raise KeyError(f"Colunas não encontradas: {colunas_ausentes}")
    return pd.get_dummies(tabela, columns=colunas, drop_first=True, dtype=int)


def corrigir_valores_invalidos(tabela: pd.DataFrame) -> pd.DataFrame:
    """Corrige o valor inválido ``2`` para ``1`` em ``first_generation``."""
    _validar_tabela(tabela)
    tabela_corrigida = tabela.copy()
    if "first_generation" in tabela_corrigida.columns:
        tabela_corrigida["first_generation"] = tabela_corrigida["first_generation"].replace(2, 1)
    return tabela_corrigida


def tratar_nulos_term_units(tabela: pd.DataFrame, estrategia: str = "media") -> pd.DataFrame:
    """Trata nulos de ``term_units`` por média, mediana, zero ou remoção."""
    _validar_tabela(tabela)
    estrategias_validas = {"media", "mediana", "zero", "remover"}
    if estrategia not in estrategias_validas:
        raise ValueError(f"Estratégia inválida: {estrategia!r}. Use uma de {sorted(estrategias_validas)}.")

    tabela_tratada = tabela.copy()
    if "term_units" not in tabela_tratada.columns:
        return tabela_tratada
    if estrategia == "remover":
        return tabela_tratada.dropna(subset=["term_units"])
    if estrategia == "zero":
        tabela_tratada["term_units"] = tabela_tratada["term_units"].fillna(0)
        return tabela_tratada
    if not is_numeric_dtype(tabela_tratada["term_units"]):
        raise TypeError("A coluna 'term_units' deve ser numérica para usar média ou mediana.")

    valor = tabela_tratada["term_units"].mean() if estrategia == "media" else tabela_tratada["term_units"].median()
    tabela_tratada["term_units"] = tabela_tratada["term_units"].fillna(valor)
    return tabela_tratada
