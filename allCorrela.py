import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_merge_data(files, probes_file):
    # Carregar os dados dos arquivos JSON
    data_frames = [pd.read_json(file) for file in files]
    probes_data = pd.read_json(probes_file)

    # Concatenar os dados dos arquivos
    continent_data = pd.concat(data_frames)

    # Mesclar os dados do continente com os dados dos probes para informações adicionais
    merged_data = continent_data.merge(probes_data.T, left_on='prb_id', right_index=True)

    # Converter timestamp para datetime
    merged_data['timestamp'] = pd.to_datetime(merged_data['timestamp'], unit='s')

    # Reamostrar os dados em intervalos de 2 horas, calculando a média das latências (avg_rtt) e o número de saltos (hop_number) dentro de cada intervalo
    numeric_columns = merged_data.select_dtypes(include='number').columns
    resampled_data = merged_data.set_index('timestamp').groupby(['dst_name', 'continente', 'nome'])[numeric_columns].resample('2h').mean().reset_index()

    return resampled_data

# Função para plotar gráfico de correlação entre latência e número de saltos por destino
def plot_correlation_by_destination(data):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='hop_number', y='avg_rtt', hue='dst_name', data=data)
    plt.title('Correlação entre Latência e Número de Saltos por Destino')
    plt.xlabel('Número de Saltos')
    plt.ylabel('Latência (ms)')
    plt.legend(title='Destino')
    plt.tight_layout()
    plt.show()

# Função para plotar gráfico de correlação entre latência e número de saltos por continente
def plot_correlation_by_continent(data):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='hop_number', y='avg_rtt', hue='continente', data=data)
    plt.title('Correlação entre Latência e Número de Saltos por Continente')
    plt.xlabel('Número de Saltos')
    plt.ylabel('Latência (ms)')
    plt.legend(title='Continente')
    plt.tight_layout()
    plt.show()

# Função para plotar gráfico de correlação entre latência e número de saltos por país
def plot_correlation_by_country(data):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='hop_number', y='avg_rtt', hue='nome', data=data)
    plt.title('Correlação entre Latência e Número de Saltos por País')
    plt.xlabel('Número de Saltos')
    plt.ylabel('Latência (ms)')
    plt.legend(title='País')
    plt.tight_layout()
    plt.show()

# Exemplo de uso
files = ['belarus_essential.json', 'china_essential.json', 'uk_essential.json']
probes_file = 'probes.json'
resampled_data = load_and_merge_data(files, probes_file)

# Gerar gráficos combinados
plot_correlation_by_destination(resampled_data)
plot_correlation_by_continent(resampled_data)
plot_correlation_by_country(resampled_data)
