import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1. Carregar os dados do arquivo CSV
# Cada linha = um paciente, cada coluna = um atributo médico
df = pd.read_csv("medical_examination.csv")

# 2. Criar a coluna "overweight"
# Cálculo do IMC = peso / (altura em metros ^ 2)
# Se IMC > 25 → 1 (acima do peso), senão → 0 (normal) -> para aplicar essa condição usei apply()
df['overweight'] = (df['weight'] / ((df['height'] / 100) ** 2)).apply(lambda x: 1 if x > 25 else 0)

# 3. Normalizar colesterol e glicose
# Transformação: 0 = bom (valor 1), 1 = ruim (valores 2 e 3) -> utilizei where() do numpy em vez de apply()

df['cholesterol'] = np.where(df['cholesterol'] == 1, 0, 1)
df['gluc'] = np.where(df['gluc'] == 1, 0, 1)

# 4. Função para criar gráfico categórico (catplot)
# Objetivo: comparar a distribuição de hábitos/condições ruins entre pessoas COM e SEM doença cardíaca (coluna "cardio")
def draw_cat_plot():
    # 5. "Derreter" o dataframe (pd.melt)
    # Transforma várias colunas (cholesterol, gluc, etc) em duas colunas: 'variable' (nome) e 'value' (0/1)
    df_cat = pd.melt(df, id_vars= ['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])


    # 6. Agrupar os dados e contar ocorrências
    # Agrupamento por (cardio, variável, valor) → total
    df_cat = df_cat.groupby(['cardio','variable','value'], as_index = False).size().rename(columns = {'size':'total'})


    # 7 e 8. Criar gráfico de barras categórico
    # - x = variável analisada
    # - y = total de pacientes
    # - hue = valor (0 ou 1 → bom/ruim)
    # - col = cardio (gera 2 gráficos: com e sem doença)
    
    fig = sns.catplot(x = 'variable', hue = 'value', col = 'cardio', y = 'total', kind = 'bar', data = df_cat).set_axis_labels("variable", "total").fig

    # 0. Salvar figura como png
    fig.savefig('catplot.png')
    return fig


# 10. Função para criar mapa de calor de correlação (heatmap)
# Objetivo: mostrar correlações entre variáveis numéricas
def draw_heat_map():
    # 11. Limpeza dos dados
    # - Remove registros inválidos (pressão diastólica > sistólica)
    # - Remove outliers de altura e peso (apenas entre 2,5% e 97,5%)

    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & 
    (df['height'] >= df['height'].quantile(0.025)) & 
    (df['height'] <= df['height'].quantile(0.975)) & 
    (df['weight'] >= df['weight'].quantile(0.025)) & 
    (df['weight'] <= df['weight'].quantile(0.975))]

    # 12. Calcular matriz de correlação
    # Cada valor varia entre -1 (correlação negativa) e +1 (correlação positiva)
    corr = df_heat.corr()

    # 13. Criar máscara para mostrar apenas metade superior da matriz (evita duplicidade visual)
    mask = np.triu(np.ones_like(corr, dtype=bool))



    # 14. Criar figura e eixos
    fig, ax = plt.subplots(figsize=(10, 8))

    # 15.  Criar heatmap
    # - cmap: escala de cores
    # - vmax: valor máximo mostrado
    # - annot=True → escreve valores dentro das células
    # - ax=ax -> os eixos são iguais aos definidos anteriormente
    
    sns.heatmap(
    corr, mask=mask, cmap='coolwarm', vmax=.3, center=0,
    square=True, linewidths=.5, cbar_kws={"shrink": .5},
    annot=True, fmt=".1f", ax=ax
    )



    # 16. Salvar figura como png
    fig.savefig('heatmap.png')
    return fig
