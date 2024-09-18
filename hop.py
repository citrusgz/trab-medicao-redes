import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Função para carregar os dados JSON
def load_json_data(filenames):
    data = []
    for filename in filenames:
        with open(filename, 'r') as file:
            for line in file:
                data.append(json.loads(line))
    return data

# Função para processar dados e extrair o número de saltos (hops), agrupando por janelas de 2 horas
def process_data(json_data):
    records = []
    for entry in json_data:
        destination = entry['dst_name']
        country = entry.get('src_addr', 'Unknown')
        continent = entry.get('continent', 'Unknown')  # Ajuste se necessário
        timestamp = pd.to_datetime(entry['timestamp'], unit='s')
        
        # Contar o número de saltos até o destino
        hops_count = len([hop for hop in entry.get('result', []) if 'result' in hop])
        
        records.append([destination, country, continent, timestamp, hops_count])
    
    # Criar o DataFrame
    df = pd.DataFrame(records, columns=['Destination', 'Country', 'Continent', 'Timestamp', 'Hops'])

    # Agrupar as medições em janelas de 2 horas
    df['TimeWindow'] = df['Timestamp'].dt.floor('2h')
    
    return df

# Função para plotar gráfico comparando número de saltos por destino
def plot_hops_by_destination(df):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='TimeWindow', y='Hops', hue='Destination', data=df, estimator='mean')
    plt.title('Variação do Número de Saltos ao longo do Tempo por Destino (Agrupado em 2 horas)')
    plt.xlabel('Tempo (Agrupado em 2 horas)')
    plt.ylabel('Número de Saltos')
    plt.legend(title='Destino')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Função para plotar gráfico comparando número de saltos por país
def plot_hops_by_country(df):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='TimeWindow', y='Hops', hue='Country', data=df, estimator='mean')
    plt.title('Variação do Número de Saltos ao longo do Tempo por País (Agrupado em 2 horas)')
    plt.xlabel('Tempo (Agrupado em 2 horas)')
    plt.ylabel('Número de Saltos')
    plt.legend(title='País')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Função para plotar gráfico comparando número de saltos por continente
def plot_hops_by_continent(df):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='TimeWindow', y='Hops', hue='Continent', data=df, estimator='mean')
    plt.title('Variação do Número de Saltos ao longo do Tempo por Continente (Agrupado em 2 horas)')
    plt.xlabel('Tempo (Agrupado em 2 horas)')
    plt.ylabel('Número de Saltos')
    plt.legend(title='Continente')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Função para plotar gráfico agregando todas as probes por destino
def plot_aggregated_hops(df):
    aggregated_df = df.groupby(['Destination', 'TimeWindow']).mean().reset_index()

    plt.figure(figsize=(10, 6))
    sns.lineplot(x='TimeWindow', y='Hops', hue='Destination', data=aggregated_df)
    plt.title('Número de Saltos Agregado por Destino (Agrupado em 2 horas)')
    plt.xlabel('Tempo (Agrupado em 2 horas)')
    plt.ylabel('Número Médio de Saltos')
    plt.legend(title='Destino')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Carregar os arquivos JSON
filenames = ['unitedK_essential.json', 'chine_essential.json', 'belarus_essential.json']
json_data = load_json_data(filenames)

# Processar os dados
df = process_data(json_data)

# Gerar gráficos
plot_hops_by_destination(df)
plot_hops_by_country(df)
plot_hops_by_continent(df)
plot_aggregated_hops(df)
