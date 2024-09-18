import pandas as pd
import matplotlib.pyplot as plt


# Load the data from the JSON files
country_data = pd.read_json('unitedK_essential.json') #LEMBRAR DE MUDAR O NOME DO ARQUIVO
probes_data = pd.read_json('probes.json')

# Merge the belarus data with probes data for additional information
merged_data = country_data.merge(probes_data.T, left_on='prb_id', right_index=True)

# Convert timestamp to datetime
merged_data['timestamp'] = pd.to_datetime(merged_data['timestamp'], unit='s')

# Resample data to 2-hour intervals by averaging the latencies (avg_rtt) within each interval
numeric_columns = merged_data.select_dtypes(include='number').columns
resampled_data = merged_data.set_index('timestamp').groupby(['dst_name', 'nome'])[numeric_columns].resample('2h').mean().reset_index()

# Create function for plotting latency over time for each probe
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

# Generate the plots
plot_latency_by_probe(resampled_data, 
                      "Latência ao longo do tempo para cada país - Destino: gov.uk", 
                      "Timestamp", "Latência (ms)", 
                      "nome", dst_filter="gov.uk") #LEMBRAR DE MUDAR O DESTINO

