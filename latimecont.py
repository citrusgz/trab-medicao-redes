import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados dos arquivos JSON
continent_data = pd.read_json('belarus_essential.json')
probes_data = pd.read_json('probes.json')

# Mesclar os dados do continente com os dados dos probes para informações adicionais
merged_data = continent_data.merge(probes_data.T, left_on='prb_id', right_index=True)

# Converter timestamp para datetime
merged_data['timestamp'] = pd.to_datetime(merged_data['timestamp'], unit='s')

# Reamostrar os dados em intervalos de 2 horas, calculando a média das latências (avg_rtt) dentro de cada intervalo
numeric_columns = merged_data.select_dtypes(include='number').columns
resampled_data = merged_data.set_index('timestamp').groupby(['dst_name', 'continente'])[numeric_columns].resample('2h').mean().reset_index()

# Criar função para plotar a latência ao longo do tempo para cada probe
def plot_latency_by_probe(data, title, xlabel, ylabel, hue, dst_filter=None):
    plt.figure(figsize=(10, 6))
    for probe in data[hue].unique():
        probe_data = data[data[hue] == probe]
        if dst_filter:
            probe_data = probe_data[probe_data['dst_name'] == dst_filter]
        plt.plot(probe_data['timestamp'], probe_data['avg_rtt'], label=f"{probe}")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc='best')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Gerar os gráficos
plot_latency_by_probe(resampled_data, 
                      "Latência ao longo do tempo para cada continente - Destino: belarus.by", 
                      "Timestamp", "Latência (ms)", 
                      "continente", dst_filter="belarus.by")