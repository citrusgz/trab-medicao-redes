import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar os dados dos arquivos JSON
continent_data = pd.read_json('china_essential.json') #LEMBRAR DE MUDAR O NOME DO ARQUIVO
probes_data = pd.read_json('probes.json')

# Mesclar os dados do continente com os dados dos probes para informações adicionais
merged_data = continent_data.merge(probes_data.T, left_on='prb_id', right_index=True)

# Converter timestamp para datetime
merged_data['timestamp'] = pd.to_datetime(merged_data['timestamp'], unit='s')

# Reamostrar os dados em intervalos de 2 horas, calculando a média das latências (avg_rtt) e o número de saltos (hop_number) dentro de cada intervalo
numeric_columns = merged_data.select_dtypes(include='number').columns
resampled_data = merged_data.set_index('timestamp').groupby(['dst_name', 'continente', 'nome'])[numeric_columns].resample('2h').mean().reset_index()

# Função para plotar gráfico de correlação entre latência e número de saltos por destino
def plot_correlation_by_destination(data):
    destinations = data['dst_name'].unique()
    for destination in destinations:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='hop_number', y='avg_rtt', data=data[data['dst_name'] == destination])
        plt.title(f'Correlação entre Latência e Número de Saltos - Destino: {destination}')
        plt.xlabel('Número de Saltos')
        plt.ylabel('Latência (ms)')
        plt.tight_layout()
        plt.show()

# Função para plotar gráfico de correlação entre latência e número de saltos por continente
def plot_correlation_by_continent(data):
    continents = data['continente'].unique()
    for continent in continents:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='hop_number', y='avg_rtt', data=data[data['continente'] == continent])
        plt.title(f'Correlação entre Latência e Número de Saltos - Continente: {continent}')
        plt.xlabel('Número de Saltos')
        plt.ylabel('Latência (ms)')
        plt.tight_layout()
        plt.show()

# Função para plotar gráfico de correlação entre latência e número de saltos por país
def plot_correlation_by_country(data):
    countries = data['nome'].unique()
    for country in countries:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='hop_number', y='avg_rtt', data=data[data['nome'] == country])
        plt.title(f'Correlação entre Latência e Número de Saltos - País: {country}')
        plt.xlabel('Número de Saltos')
        plt.ylabel('Latência (ms)')
        plt.tight_layout()
        plt.show()

# Gerar gráficos
plot_correlation_by_destination(resampled_data)
plot_correlation_by_continent(resampled_data)
plot_correlation_by_country(resampled_data)
