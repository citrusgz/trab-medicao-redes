import json
import matplotlib.pyplot as plt
import datetime
from collections import defaultdict
from probs import get_country_by_prb_id, get_continent_by_prb_id

# Carregar os dados do arquivo JSON (chine_essential.json)
with open('belarus_essential.json', 'r') as f:
    traceroutes = json.load(f)

# Dicionário para armazenar número de hops agrupados por continente e intervalos de 2 horas
hops_data_continent = defaultdict(lambda: defaultdict(list))

# Dicionário para armazenar número de hops agrupados por país e intervalos de 2 horas
hops_data_country = defaultdict(lambda: defaultdict(list))

# Agrupar os dados e intervalos de 2 horas
for trace in traceroutes:
    prb_id = trace['prb_id']
    country = get_country_by_prb_id(prb_id) 
    continent = get_continent_by_prb_id(prb_id)
    timestamp = trace['timestamp']
    num_hops = trace['hop_number']

    # Agrupar o tempo em intervalos de 2 horas
    time = datetime.datetime.utcfromtimestamp(timestamp)
    time_2_hour_interval = time.replace(minute=0, second=0, microsecond=0, hour=(time.hour // 2) * 2)

    if continent != "Unknown" and num_hops is not None:  
        hops_data_continent[continent][time_2_hour_interval].append(num_hops)
    
    if country != "Unknown" and num_hops is not None:
        hops_data_country[country][time_2_hour_interval].append(num_hops)
def plot_country_hops_graphs(hops_data_country):

    # Iterar sobre os países e gerar um gráfico para cada um
    for country, times_data in hops_data_country.items():
        times = []
        avg_hops = []

        # Calcular a média do número de hops para cada intervalo de 2 horas
        for time, hops in sorted(times_data.items()):
            valid_hops = [hop for hop in hops if hop is not None]  # Filtrar os valores None
            if valid_hops:  # Apenas calcular a média se houver valores válidos
                avg_hops_for_time = sum(valid_hops) / len(valid_hops)
                times.append(time)
                avg_hops.append(avg_hops_for_time)

        # Plotar o gráfico se houver dados válidos
        if times and avg_hops:
            plt.figure(figsize=(10, 6))
            plt.plot(times, avg_hops, marker='o', label=f'{country}')
            plt.title(f'Número médio de hops ao longo do tempo - {country}')
            plt.xlabel('Tempo (Intervalos de 2 horas)')
            plt.ylabel('Número médio de Hops')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            # Salvar o gráfico como imagem
            plt.savefig(f'hops_{country}.png')
            plt.show()

# Função para gerar um gráfico combinado de todos os países (hops ao longo do tempo)
def plot_combined_country_hops_graph(hops_data_country):
    plt.figure(figsize=(12, 8))

    # Iterar sobre os países e adicionar ao gráfico combinado
    for country, times_data in hops_data_country.items():
        times = []
        avg_hops = []

        # Calcular a média do número de hops para cada intervalo de 2 horas
        for time, hops in sorted(times_data.items()):
            valid_hops = [hop for hop in hops if hop is not None]
            if valid_hops:
                avg_hops_for_time = sum(valid_hops) / len(valid_hops)
                times.append(time)
                avg_hops.append(avg_hops_for_time)

        # Plotar os dados se houver hops válidos
        if times and avg_hops:
            plt.plot(times, avg_hops, marker='o', label=f'{country}')

    # Customizar o gráfico
    plt.title('Número médio de hops ao longo do tempo - Todos os Países')
    plt.xlabel('Tempo (Intervalos de 2 horas)')
    plt.ylabel('Número médio de Hops')
    plt.legend(title="Países")
    plt.tight_layout()

    # Salvar o gráfico como imagem
    plt.savefig('hops_combined_countries.png')
    plt.show()

# Função para gerar gráficos de número de hops por continente
def plot_continent_hops_graphs(hops_data_continent):

    # Iterar sobre os continentes e gerar um gráfico para cada um
    for continent, times_data in hops_data_continent.items():
        times = []
        avg_hops = []

        # Calcular a média do número de hops para cada intervalo de 2 horas
        for time, hops in sorted(times_data.items()):
            valid_hops = [hop for hop in hops if hop is not None]
            if valid_hops:
                avg_hops_for_time = sum(valid_hops) / len(valid_hops)
                times.append(time)
                avg_hops.append(avg_hops_for_time)

        # Plotar o gráfico se houver dados válidos
        if times and avg_hops:
            plt.figure(figsize=(10, 6))
            plt.plot(times, avg_hops, marker='o', label=f'{continent}')
            plt.title(f'Número médio de hops ao longo do tempo - {continent}')
            plt.xlabel('Tempo (Intervalos de 2 horas)')
            plt.ylabel('Número médio de hops')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            # Salvar o gráfico como imagem
            plt.savefig(f'hops_{continent}.png')
            plt.show()

# Função para gerar um gráfico combinado de todos os continentes (número de hops)
def plot_combined_continent_hops_graph(hops_data_continent):
    plt.figure(figsize=(12, 8))

    # Iterar sobre os continentes e adicionar ao gráfico combinado
    for continent, times_data in hops_data_continent.items():
        times = []
        avg_hops = []

        # Calcular a média do número de hops para cada intervalo de 2 horas
        for time, hops in sorted(times_data.items()):
            valid_hops = [hop for hop in hops if hop is not None]
            if valid_hops:
                avg_hops_for_time = sum(valid_hops) / len(valid_hops)
                times.append(time)
                avg_hops.append(avg_hops_for_time)

        # Plotar os dados se houver hops válidos
        if times and avg_hops:
            plt.plot(times, avg_hops, marker='o', label=f'{continent}')

    # Customizar o gráfico
    plt.title('Número médio de hops ao longo do tempo - Todos os Continentes')
    plt.xlabel('Tempo (Intervalos de 2 horas)')
    plt.ylabel('Número médio de hops')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title="Continentes")
    plt.tight_layout()

    # Salvar o gráfico como imagem
    plt.savefig('hops_combined_continents.png')
    plt.show()

# Chamar as funções para gerar gráficos
plot_country_hops_graphs(hops_data_country)
plot_combined_country_hops_graph(hops_data_country)
plot_continent_hops_graphs(hops_data_continent)
plot_combined_continent_hops_graph(hops_data_continent)
