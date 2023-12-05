import dash
from dash import dcc, html
import plotly.express as px
from scipy.stats import norm 
import pandas as pd
import numpy as np

data = pd.read_csv('.\dataset-projeto\global-data-on-sustainable-energy (1).csv')

# Filtrar os países de interesse
paises = ["Madagascar","Egypt","Pakistan","China","Papua New Guine","Australia","Haiti","Brazil","Greece","Germany"]
g20 = ["Argentina","Australia","Brazil","Canada","China","France","Germany","India","Indonesia","Italy","Japan","Mexico","Saudi Arabia","South Africa","Turkey","United Kingdom","United States"]

dados_filtrados = data[data['Entity'].isin(paises)]
dados_filtrados_g20 = data[data["Entity"].isin(g20)]

espaco_var = dados_filtrados.groupby('Entity')['Access to electricity (% of population)'].max() - dados_filtrados.groupby('Entity')['Access to electricity (% of population)'].min()

media_acesso_nrg = dados_filtrados.groupby('Entity')['Access to electricity (% of population)'].mean()


dados_filtrados['Renewable-electricity-generating-capacity-per-capita'] = pd.to_numeric(dados_filtrados['Renewable-electricity-generating-capacity-per-capita'], errors='coerce')
capacidade_per_capita = dados_filtrados.groupby('Entity')['Renewable-electricity-generating-capacity-per-capita'].max()


dados_filtrados['Electricity from fossil fuels (TWh)'] = pd.to_numeric(dados_filtrados['Electricity from fossil fuels (TWh)'], errors='coerce')
geracao_combust_fossil = dados_filtrados.groupby('Entity')['Electricity from fossil fuels (TWh)'].sum()

correlacao = dados_filtrados['Access to electricity (% of population)'].corr(dados_filtrados['Value_co2_emissions_kt_by_country'])

dados_filtrados = dados_filtrados.dropna(subset=['Renewable-electricity-generating-capacity-per-capita'])
mean, std = dados_filtrados['Renewable-electricity-generating-capacity-per-capita'].mean(), dados_filtrados['Renewable-electricity-generating-capacity-per-capita'].std()
x = np.linspace(dados_filtrados['Renewable-electricity-generating-capacity-per-capita'].min(), dados_filtrados['Renewable-electricity-generating-capacity-per-capita'].max(), 1000)
pdf = norm.pdf(x, mean, std)

# Inicializar o aplicativo Dash
app = dash.Dash(__name__)
server = app.server

# Layout do Dashboard
app.layout = html.Div(children=[
    html.H1(children='Dashboard de Sustentabilidade'),

    html.Div(children='''
        Análise de dados relacionados à sustentabilidade energética.
    '''),

    dcc.Graph(
        id='graph-espaco-variacao',
        figure=px.bar(x=espaco_var.index, y=espaco_var.values, title='Espaço de Variação no Acesso à Eletricidade por País', labels={'x': 'País', 'y': 'Espaço de Variação'})
    ),

    dcc.Graph(
        id='graph-media-acesso-nrg',
        figure=px.bar(x=media_acesso_nrg.index, y=media_acesso_nrg.values, title='Média dos percentuais de pessoas com acesso à energia elétrica (2000-2020)', labels={'x': 'País', 'y': 'Média de Acesso a Energia Elétrica'})
    ),

    dcc.Graph(
        id='graph-capacidade-per-capita',
        figure=px.bar(x=capacidade_per_capita.index, y=capacidade_per_capita.values, title='Capacidade de Geração de Energia Renovável Per Capita por País', labels={'x': 'País', 'y': 'Capacidade de Geração de Energia Renovável Per Capita (TWh)'})
    ),

    dcc.Graph(
        id='graph-geracao-combust-fossil',
        figure=px.bar(x=geracao_combust_fossil.index, y=geracao_combust_fossil.values, title='Quantidade de Eletricidade Gerada a partir de Combustíveis Fósseis (2000-2020)', labels={'x': 'País', 'y': 'Eletricidade Gerada (TWh)'})
    ),

    # dcc.Graph(
    #     id='graph-correlacao-co2-acesso-nrg',
    #     figure=px.scatter(x=dados_filtrados['Access to electricity (% of population)'], y=dados_filtrados['Value_co2_emissions_kt_by_country'], title=f'Correlação entre Acesso à Eletricidade e Emissões de CO2 (G20)\nCorrelação: {correlacao:.2f}', labels={'x': 'Acesso à Eletricidade (%)', 'y': 'Emissões de CO2 (kt)'}).update_traces(mode='markers', marker=dict(color='red'))
    # ),

    dcc.Graph(
        id='graph-boxplot-acesso-nrg',
        figure=px.box(dados_filtrados, x='Access to electricity (% of population)', y='Entity', title='Comparação do Acesso à Energia Elétrica por País (2000-2020)', labels={'x': 'Percentual de Acesso à Energia Elétrica', 'y': 'País'})
    ),

    dcc.Graph(
        id='graph-boxplot-capacidade-nrg',
        figure=px.box(dados_filtrados, x='Renewable-electricity-generating-capacity-per-capita', y='Entity', title='Capacidade de geração de energia renovável per capita', labels={'x': 'Energia renovável (TWh)', 'y': 'País'})
    ),

    dcc.Graph(
        id='graph-distribuicao-normal',
        figure=px.line(x=x, y=pdf, title='Capacidade de geração de energia renovável per capita (TWh) - Distribuição Normal', labels={'x': 'Capacidade de geração de energia renovável per capita (TWh)', 'y': 'Densidade de Probabilidade'})
    ),
])

# Executar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)
