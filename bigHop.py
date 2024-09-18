import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar os dados dos arquivos JSON
continent_data = pd.read_json('uk_essential.json') #LEMBRAR DE MUDAR O NOME DO ARQUIVO
probes_data = pd.read_json('probes.json')

# Mesclar os dados do continente com os dados dos probes para informações adicionais
merged_data = continent_data.merge(probes_data.T, left_on='prb_id', right_index=True)

# Converter timestamp para datetime
merged_data['timestamp'] = pd.to_datetime(merged_data['timestamp'], unit='s')

# Reamostrar os dados em intervalos de 2 horas, calculando a média dos saltos (hops) dentro de cada intervalo
numeric_columns = merged_data.select_dtypes(include='number').columns
resampled_data = merged_data.set_index('timestamp').groupby(['dst_name', 'continente', 'nome'])[numeric_columns].resample('2h').mean().reset_index()

# Remover valores discrepantes (outliers)
q_low = resampled_data['hop_number'].quantile(0.01)
q_high = resampled_data['hop_number'].quantile(0.99)
filtered_data = resampled_data[(resampled_data['hop_number'] >= q_low) & (resampled_data['hop_number'] <= q_high)]

# Função para plotar gráfico comparando a quantidade de saltos por continente
def plot_hops_by_continent(data):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='timestamp', y='hop_number', hue='continente', data=data)
    plt.title('Número de Saltos ao longo do tempo por Continente')
    plt.xlabel('Timestamp')
    plt.ylabel('Número de Saltos')
    plt.legend(title='Continente')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Função para plotar gráfico comparando a quantidade de saltos por país
def plot_hops_by_country(data):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='timestamp', y='hop_number', hue='nome', data=data)
    plt.title('Número de Saltos ao longo do tempo por País')
    plt.xlabel('Timestamp')
    plt.ylabel('Número de Saltos')
    plt.legend(title='País')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Gerar gráficos
plot_hops_by_continent(filtered_data)
plot_hops_by_country(filtered_data)