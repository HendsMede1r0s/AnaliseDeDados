from pathlib import Path
import pandas as pd

def obter_raiz_do_projeto() -> Path:
    """Retorna o caminho da pasta principal do projeto."""
    return Path(__file__).resolve().parent.parent

def carregar_dados_brutos(nome_do_arquivo: str | Path) -> pd.DataFrame:
    """Carrega um CSV pelo nome ou por caminho relativo/absoluto.

    Também aceita o formato usado nos notebooks, como
    ``"../data/raw/college_sleep_and_gpa.csv"``.
    """
    raiz = obter_raiz_do_projeto()
    caminho_informado = Path(nome_do_arquivo)
    candidatos = [caminho_informado] if caminho_informado.is_absolute() else [
        Path.cwd() / caminho_informado,
        raiz / caminho_informado,
        raiz / 'data' / 'raw' / caminho_informado.name,
    ]
    for caminho in candidatos:
        if caminho.is_file():
            return pd.read_csv(caminho)
    raise FileNotFoundError(f"Arquivo bruto não encontrado: {nome_do_arquivo}")

def carregar_dados_processados(nome_do_arquivo: str) -> pd.DataFrame:
    """Carrega um arquivo CSV da pasta data/processed/."""
    raiz = obter_raiz_do_projeto()
    caminho_do_arquivo = raiz / 'data' / 'processed' / nome_do_arquivo
    return pd.read_csv(caminho_do_arquivo)

def salvar_dados_processados(tabela: pd.DataFrame, nome_do_arquivo: str) -> None:
    """Salva a sua tabela (DataFrame) na pasta data/processed/."""
    raiz = obter_raiz_do_projeto()
    pasta_de_destino = raiz / 'data' / 'processed'
    pasta_de_destino.mkdir(parents=True, exist_ok=True)

    tabela.to_csv(pasta_de_destino / nome_do_arquivo, index=False)
