import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

# Função para carregar os dados JSON
def load_json_data(filenames):
    data = []
    for filename in filenames:
        with open(filename, 'r') as file:
            for line in file:
                data.append(json.loads(line))
    return data

# Função para processar dados e extrair latências
def process_data(json_data):
    records = []
    for entry in json_data:
        destination = entry['dst_name']
        country = entry.get('src_addr')
        timestamp = entry['timestamp']
        
        latencies = []
        # Percorrer os hops e verificar se existe 'result'
        for hop_result in entry.get('result', []):
            if 'result' in hop_result:
                for hop in hop_result['result']:
                    if 'rtt' in hop:  # Verifica se há 'rtt' no hop
                        latencies.append(hop['rtt'])
        
        # Calcular a latência média, se houver latências
        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            records.append([destination, country, timestamp, avg_latency])
    
    df = pd.DataFrame(records, columns=['Destination', 'Country', 'Timestamp', 'Latency'])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')
    return df

# Função para plotar gráfico comparando latência por destino
def plot_latency_by_destination(df):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='Timestamp', y='Latency', hue='Destination', data=df)
    plt.title('Variação da Latência ao longo do Tempo por Destino')
    plt.xlabel('Tempo')
    plt.ylabel('Latência (ms)')
    plt.legend(title='Destino')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Função para plotar gráfico comparando latência por país
def plot_latency_by_country(df):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='Timestamp', y='Latency', hue='Country', data=df)
    plt.title('Variação da Latência ao longo do Tempo por País')
    plt.xlabel('Tempo')
    plt.ylabel('Latência (ms)')
    plt.legend(title='País')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Carregar os arquivos JSON
filenames = ['unitedK.json', 'chine.json', 'belarus.json']
json_data = load_json_data(filenames)

# Processar os dados
df = process_data(json_data)

# Gerar gráficos
plot_latency_by_destination(df)
plot_latency_by_country(df)
