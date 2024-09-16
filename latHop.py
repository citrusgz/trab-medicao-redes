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
        country = entry.get('src_addr')
        continent = entry.get('continent')  # Ajuste se necessário
        timestamp = pd.to_datetime(entry['timestamp'], unit='s')
        
        # Contar o número de saltos até o destino
        hops_count = len([hop for hop in entry.get('result', []) if 'result' in hop])
        
        records.append([destination, country, continent, timestamp, hops_count])
    
    # Criar o DataFrame
    df = pd.DataFrame(records, columns=['Destination', 'Country', 'Continent', 'Timestamp', 'Hops'])

    # Agrupar as medições em janelas de 2 horas
    df['TimeWindow'] = df['Timestamp'].dt.floor('2h')
    
    return df

# Função para gerar gráficos individuais por destino
def plot_hops_per_destination(df):
    destinations = df['Destination'].unique()
    for destination in destinations:
        plt.figure(figsize=(10, 6))
        df_destination = df[df['Destination'] == destination]
        sns.lineplot(x='TimeWindow', y='Hops', data=df_destination, estimator='mean')
        plt.title(f'Número de Saltos ao longo do Tempo para {destination}')
        plt.xlabel('Tempo (Agrupado em 2 horas)')
        plt.ylabel('Número de Saltos')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

# Função para gerar gráficos individuais por país
def plot_hops_per_country(df):
    countries = df['Country'].unique()
    for country in countries:
        plt.figure(figsize=(10, 6))
        df_country = df[df['Country'] == country]
        sns.lineplot(x='TimeWindow', y='Hops', data=df_country, estimator='mean')
        plt.title(f'Número de Saltos ao longo do Tempo para {country}')
        plt.xlabel('Tempo (Agrupado em 2 horas)')
        plt.ylabel('Número de Saltos')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

# Função para gerar gráficos individuais por continente
def plot_hops_per_continent(df):
    continents = df['Continent'].unique()
    for continent in continents:
        plt.figure(figsize=(10, 6))
        df_continent = df[df['Continent'] == continent]
        sns.lineplot(x='TimeWindow', y='Hops', data=df_continent, estimator='mean')
        plt.title(f'Número de Saltos ao longo do Tempo para o Continente {continent}')
        plt.xlabel('Tempo (Agrupado em 2 horas)')
        plt.ylabel('Número de Saltos')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

# Carregar os arquivos JSON
filenames = ['unitedK.json', 'chine.json', 'belarus.json']
json_data = load_json_data(filenames)

# Processar os dados
df = process_data(json_data)

# Gerar gráficos individuais
plot_hops_per_destination(df)
plot_hops_per_country(df)
plot_hops_per_continent(df)
