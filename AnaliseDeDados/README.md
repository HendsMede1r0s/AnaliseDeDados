# Análise de Sono e Desempenho Acadêmico

Este projeto explora a relação entre hábitos de sono e desempenho acadêmico de estudantes universitários. O fluxo cobre análise exploratória, tratamento dos dados e a criação de bases específicas para análises de regressão e classificação.

O conjunto original possui 634 observações e 22 variáveis. Após a limpeza, a base principal contém 626 observações e 18 variáveis.

## Objetivos

- Examinar qualidade, valores ausentes e possíveis outliers no conjunto de dados.
- Preparar uma base analítica com dados numéricos, categóricos codificados e variáveis padronizadas.
- Gerar bases menores para investigar o GPA do período em regressão e a categoria de desempenho em classificação.
- Comparar os grupos de GPA alto e baixo com testes t de Student para variáveis selecionadas.

## Estrutura do projeto

```text
.
├── data/
│   ├── raw/college_sleep_and_gpa.csv
│   └── processed/
│       ├── dataset_clean.csv
│       ├── dataset_regression.csv
│       └── dataset_classification.csv
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_regression_analysis.ipynb
│   └── 04_classification_analysis.ipynb
├── reports/figures/
├── src/
│   ├── data_loader.py
│   ├── eda.py
│   ├── preprocessing.py
│   └── visualization.py
├── requirements.txt
└── README.md
```

## Dados

O arquivo bruto é `data/raw/college_sleep_and_gpa.csv` e contém 634 linhas e 22 colunas. Entre as variáveis estão medidas de sono (`avg_sleep_hours`, `daytime_sleep_minutes`, `sleep_midpoint_minutes` e `bedtime_variability`), características demográficas, universidade e indicadores de desempenho (`prior_gpa`, `term_gpa` e `gpa_change`).

Os valores ausentes identificados na base bruta são:

| Coluna | Valores ausentes |
| --- | ---: |
| `term_units` | 147 |
| `term_load_z` | 147 |
| `first_generation` | 4 |
| `gender` | 3 |
| `underrepresented` | 1 |

Também foi identificado um valor `2` em `first_generation`; no pré-processamento ele é corrigido para `1`.

## Fluxo de análise

Execute os notebooks nesta ordem:

1. `01_eda.ipynb` — inspeciona o conjunto bruto, corrige o valor inválido de `first_generation`, resume nulos e identifica outliers por IQR e escore-z.
2. `02_preprocessing.ipynb` — limpa, transforma e codifica os dados; gera `dataset_clean.csv`.
3. `03_regression_analysis.ipynb` — cria `dataset_regression.csv` e salva a matriz de correlação usada na análise de regressão.
4. `04_classification_analysis.ipynb` — realiza testes t entre grupos de GPA e cria `dataset_classification.csv`; também salva sua matriz de correlação.

Os gráficos gerados são salvos em `reports/figures/`.

| Figura | Origem |
| --- | --- |
| `distribuicao_nulos.png` | Mapa de calor dos ausentes no EDA |
| `quantidade_valores_ausentes.png` | Barras com a quantidade de ausentes |
| `boxplot_*.png` | Boxplots das variáveis investigadas como outliers |
| `matriz_correlacao_regressao.png` | Matriz do notebook de regressão |
| `matriz_correlacao_classificacao.png` | Matriz do notebook de classificação |

## Pré-processamento aplicado

O notebook de pré-processamento executa as seguintes decisões:

- Remove colunas não usadas na análise: `avg_sleep_minutes`, `term_units`, `student_id`, `sleep_midpoint_clock`, `cohort_code`, `study` e `semester`.
- Remove linhas com nulos em `gender`, `first_generation` e `underrepresented`.
- Preenche nulos de `term_load_z` pela mediana.
- Aplica `log1p` em `bedtime_variability` e `daytime_sleep_minutes`.
- Aplica winsorização superior de 3% a `sleep_midpoint_minutes`; inferior de 5% a `prior_gpa` e `term_gpa`; e de 3% em ambas as extremidades a `term_load_z`.
- Cria `gpa_category`: `Alto` para GPA do período maior ou igual à mediana e `Baixo` nos demais casos.
- Codifica `sleep_bracket`, `gpa_category`, `gender` e `university`.
- Padroniza com `StandardScaler` as variáveis contínuas selecionadas.

O resultado é `data/processed/dataset_clean.csv`, com 626 linhas e 18 colunas. A divisão da variável `gpa_category` é de 318 observações em `Alto` e 308 em `Baixo`; a mediana de `term_gpa` usada no corte é 3,556.

## Bases geradas

| Arquivo | Linhas × colunas | Uso | Variável-alvo/informação principal |
| --- | ---: | --- | --- |
| `dataset_clean.csv` | 626 × 18 | Base processada completa | Inclui `term_gpa` e `gpa_category` |
| `dataset_regression.csv` | 626 × 6 | Análise de regressão | `term_gpa` |
| `dataset_classification.csv` | 626 × 6 | Análise de classificação | `gpa_category_encoded` |

As colunas de preditores mantidas nas duas bases reduzidas são `avg_sleep_hours`, `sleep_midpoint_minutes`, `prior_gpa`, `underrepresented` e `first_generation`.

## Principais achados exploratórios

Estes resultados descrevem associações na base processada; não estabelecem causalidade.

- A maior correlação positiva com `term_gpa` é `prior_gpa` (r = 0,657).
- `avg_sleep_hours` possui correlação positiva moderada-baixa com `term_gpa` (r = 0,181).
- `sleep_midpoint_minutes` apresenta correlação negativa moderada-baixa com `term_gpa` (r = -0,186).
- `under_6h_sleep` também possui associação negativa com `term_gpa` (r = -0,177).
- No teste t entre os grupos `Alto` e `Baixo`, as variáveis avaliadas foram significativas a 5%: `avg_sleep_hours` (p = 0,0162), `sleep_midpoint_minutes` (p = 0,0010), `prior_gpa` (p < 0,001), `underrepresented` (p = 0,0005) e `first_generation` (p < 0,001).

## Cuidados metodológicos

- `gpa_category` e `gpa_category_encoded` são criadas diretamente a partir de `term_gpa`. Portanto, elas não devem ser usadas como preditores de `term_gpa`, nem `term_gpa` deve entrar como preditor de `gpa_category`; isso causaria vazamento de alvo (*target leakage*).
- `gpa_change` é calculada a partir de informações de GPA e deve ser examinada cuidadosamente antes de qualquer modelo cujo alvo seja `term_gpa`.
- As correlações e os testes t mostram associações entre variáveis, não efeitos causais do sono sobre o desempenho.
- A winsorização, transformação logarítmica e padronização devem ser ajustadas somente no conjunto de treino caso o projeto avance para validação de modelos preditivos.

## Como executar

Recomenda-se Python 3.10 ou superior.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install jupyter
cd notebooks
jupyter notebook
```

Abra e execute os notebooks na ordem indicada na seção [Fluxo de análise](#fluxo-de-análise). Os notebooks usam caminhos relativos a partir da pasta `notebooks/`.

## Funções reutilizáveis em `src`

- `data_loader.py`: carregamento e salvamento de arquivos CSV do projeto.
- `eda.py`: resumo de valores ausentes e identificação de outliers por IQR.
- `preprocessing.py`: filtro de colunas, correção de `first_generation`, encoding e tratamento opcional de `term_units`.
- `visualization.py`: localização da pasta de figuras, mapa de nulos e matriz de correlação.

## Dependências

As dependências principais estão em `requirements.txt`:

- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- scipy
