# Avaliação Comparativa de Modelos de ML: Especialista, Árvores e Ensembles

**Aluno:** Henderson Emanuel Bernardo de Medeiros  
**Matrícula:** [20250031156]  
**Dataset:** https://www.kaggle.com/datasets/kylefengkfeng209/sleep-vs-gpa-in-college  

## Descrição
Este projeto realiza a comparação entre um Sistema Especialista (baseado em regras), uma Árvore de Decisão e Ensemble Learning (Random Forest e Gradient Boosting) para classificação do desempenho acadêmico (GPA) de estudantes universitários. A avaliação segue as diretrizes da disciplina, analisando métricas de desempenho (Accuracy, Precision, Recall, F1-Score), generalização (Gap Treino-Teste e K-Fold) e eficiência computacional (tempo, memória RAM e pegada de carbono CO2).

## Estrutura do projeto

```text
.
├── data/
│   ├── raw/college_sleep_and_gpa.csv
│   └── processed/
│       ├── dataset_clean.csv
│       ├── dataset_regression.csv
│       └── dataset_classification.csv
│       ├── X_train_clf.csv
│       ├── X_test_clf.csv
│       ├── y_train_clf.csv
│       └── y_test_clf.csv
├── notebooks/
│   ├── 01_eda.ipynb 
│   ├── 02_preprocessing.ipynb 
│   ├── 03_expert_system.ipynb 
│   ├── 04_decision_tree.ipynb 
│   ├── 05_ensemble.ipynb 
│   ├── 06_evaluation_metrics.ipynb 
│   ├── 07_generalization.ipynb 
│   └── 08_computational_efficiency.ipynb 
├── rules/
│   └── regras_classificacao.txt 
├── logs/
│   └── cronometro_regras.csv 
├── reports/
│   ├── figures/ 
│   └── tables/ 
├── src/
├── requirements.txt
└── README.md

```
# Como Executar

## Recomenda-se Python 3.10 ou superior.

1. Clone o repositório.

2. Crie e ative o ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute os notebooks na ordem numérica (de 01 a 08) dentro da pasta notebooks/



# Principais Resultados e Conclusão
* Classificação (Desempenho): A Árvore de Decisão obteve a melhor generalização e métricas de avaliação, superando os Ensembles que apresentaram sinais de overfitting (especialmente o Gradient Boosting) e o Sistema Especialista que apresentou underfitting.

* Eficiência Computacional e Sustentabilidade: A Tabela Comparativa Final demonstrou que a Árvore de Decisão é o modelo mais viável para implantação em dispositivos de borda (Edge AI) devido ao seu consumo ínfimo de memória (0.0111 MB) e menor pegada de carbono.

## Tabela Comparativa de Eficiência


| Modelo | Tempo Elaboração/Treino | Vazão (amostras/s) | Pico Memória (MB) | Energia (kWh) | CO2 (mg) |
| :--- | :---: | ---: | ---: | ---: | ---: |
| Sistema Especialista | 2h (Humano) | 16645.0 | 0.0100 | 3.15e-08 | 0.0014 |
| Árvore de Decisão | 0.0023s (Comp.) | 113242.0 | 0.0111 | 4.64e-09 | 0.0002 |
| Random Forest | 0.0823s (Comp.) | 4320.0 | 0.2382 | 1.22e-07 | 0.0056 |
| Gradient Boosting | 0.2595s (Comp.) | 59453.0 | 0.0136 | 8.83e-09 | 0.0004 |
