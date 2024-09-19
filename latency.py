import json
import matplotlib.pyplot as plt
import datetime
from collections import defaultdict
from data_processor import get_country_by_prb_id, get_continent_by_prb_id # Importa a função de mapeamento do data_processor.py

# Carregar os dados do arquivo JSON (chine_essential.json)
with open('uk_essential.json', 'r') as f:
    traceroutes = json.load(f)

# Dicionário para armazenar latências agrupadas por país e intervalos de 2 horas
latency_data_country = defaultdict(lambda: defaultdict(list))

# Dicionário para armazenar latências agrupadas por continente e intervalos de 2 horas
latency_data_continent = defaultdict(lambda: defaultdict(list))

# Agrupar os dados e intervalos de 2 horas
for trace in traceroutes:
    prb_id = trace['prb_id']
    country = get_country_by_prb_id(prb_id)  # Obter o país baseado no prb_id
    continent = get_continent_by_prb_id(prb_id)  # Obter o continente baseado no prb_id
    timestamp = trace['timestamp']
    avg_rtt = trace['avg_rtt']

    # Agrupar o tempo em intervalos de 2 horas
    time = datetime.datetime.utcfromtimestamp(timestamp)
    time_2_hour_interval = time.replace(minute=0, second=0, microsecond=0, hour=(time.hour // 2) * 2)

    if country != "Unknown" and avg_rtt is not None:  # Ignorar valores de latência que sejam None
        latency_data_country[country][time_2_hour_interval].append(avg_rtt)
    
    if continent != "Unknown" and avg_rtt is not None:  # Ignorar valores de latência que sejam None
        latency_data_continent[continent][time_2_hour_interval].append(avg_rtt)

def plot_country_latency_graphs(latency_data_country):
    # Iterar sobre os países e gerar um gráfico para cada um
    for country, times_data in latency_data_country.items():
        times = []
        avg_rtts = []

        # Calcular a média da latência para cada intervalo de 2 horas
        for time, latencies in sorted(times_data.items()):
            valid_rtts = [rtt for rtt in latencies if rtt is not None]  # Filtrar os valores None
            if valid_rtts:  # Apenas calcular a média se houver valores válidos
                avg_rtt_for_time = sum(valid_rtts) / len(valid_rtts)
                times.append(time)
                avg_rtts.append(avg_rtt_for_time)

        # Plotar o gráfico se houver dados válidos
        if times and avg_rtts:
            plt.figure(figsize=(10, 6))
            plt.plot(times, avg_rtts, marker='o', label=f'{country}')
            plt.title(f'Latência média ao longo do tempo - {country}')
            plt.xlabel('Tempo (Intervalos de 2 horas)')
            plt.ylabel('Latência média (ms)')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            # Salvar o gráfico como imagem
            plt.savefig(f'latency_{country}.png')
            plt.show()

# Função para gerar um gráfico combinado com todos os países
def plot_combined_graph(latency_data):
    plt.figure(figsize=(12, 8))

    # Iterar sobre os países e gerar as linhas no mesmo gráfico
    for country, times_data in latency_data.items():
        times = []
        avg_rtts = []

        # Calcular a média das latências para cada intervalo de 2 horas
        for time, rtts in sorted(times_data.items()):
            valid_rtts = [rtt for rtt in rtts if rtt is not None]  # Filtrar os valores None
            if valid_rtts:  # Apenas calcular a média se houver valores válidos
                avg_rtt_for_time = sum(valid_rtts) / len(valid_rtts)
                times.append(time)
                avg_rtts.append(avg_rtt_for_time)

        # Plotar os dados se houver latências válidas para o país
        if times and avg_rtts:
            plt.plot(times, avg_rtts, marker='o', label=f'{country}')


    # Customizar o gráfico
    plt.title('Latência média ao longo do tempo - Todos os Países')
    plt.xlabel('Tempo (Intervalos de 2 horas)')
    plt.ylabel('Latência média (ms)')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title="Países")
    plt.tight_layout()

    # Salvar o gráfico como imagem
    plt.savefig('latency_combined.png')
    plt.show()

def plot_combined_country_latency_graph(latency_data_country):
    plt.figure(figsize=(12, 8))

    # Iterar sobre os países e adicionar ao gráfico combinado
    for country, times_data in latency_data_country.items():
        times = []
        avg_rtts = []

        # Calcular a média da latência para cada intervalo de 2 horas
        for time, latencies in sorted(times_data.items()):
            valid_rtts = [rtt for rtt in latencies if rtt is not None]
            if valid_rtts:
                avg_rtt_for_time = sum(valid_rtts) / len(valid_rtts)
                times.append(time)
                avg_rtts.append(avg_rtt_for_time)

        # Plotar os dados se houver latências válidas
        if times and avg_rtts:
            plt.plot(times, avg_rtts, marker='o', label=f'{country}')

    # Customizar o gráfico
    plt.title('Latência média ao longo do tempo - Todos os Países')
    plt.xlabel('Tempo (Intervalos de 2 horas)')
    plt.ylabel('Latência média (ms)')
    plt.legend(title="Países")
    plt.tight_layout()

    # Salvar o gráfico como imagem
    plt.savefig('latency_combined_countries.png')
    plt.show()


def plot_continent_graphs(latency_data_continent):
    # Iterar sobre os continentes e gerar um gráfico para cada um
    for continent, times_data in latency_data_continent.items():
        times = []
        avg_rtts = []

        # Calcular a média das latências para cada intervalo de 2 horas
        for time, rtts in sorted(times_data.items()):
            valid_rtts = [rtt for rtt in rtts if rtt is not None]  # Filtrar os valores None
            if valid_rtts:  # Apenas calcular a média se houver valores válidos
                avg_rtt_for_time = sum(valid_rtts) / len(valid_rtts)
                times.append(time)
                avg_rtts.append(avg_rtt_for_time)

        # Plotar o gráfico se houver dados válidos
        if times and avg_rtts:
            plt.figure(figsize=(10, 6))
            plt.plot(times, avg_rtts, marker='o', label=f'{continent}')
            plt.title(f'Latência média ao longo do tempo - {continent}')
            plt.xlabel('Tempo (Intervalos de 2 horas)')
            plt.ylabel('Latência média (ms)')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            # Salvar o gráfico como imagem
            plt.savefig(f'latency_{continent}.png')
            plt.show()

# Função para gerar um gráfico combinado de todos os continentes
def plot_combined_continent_graph(latency_data_continent):
    plt.figure(figsize=(12, 8))

    # Iterar sobre os continentes e adicionar ao gráfico combinado
    for continent, times_data in latency_data_continent.items():
        times = []
        avg_rtts = []

        # Calcular a média das latências para cada intervalo de 2 horas
        for time, rtts in sorted(times_data.items()):
            valid_rtts = [rtt for rtt in rtts if rtt is not None]
            if valid_rtts:
                avg_rtt_for_time = sum(valid_rtts) / len(valid_rtts)
                times.append(time)
                avg_rtts.append(avg_rtt_for_time)

        # Plotar os dados se houver latências válidas
        if times and avg_rtts:
            plt.plot(times, avg_rtts, marker='o', label=f'{continent}')

    # Customizar o gráfico
    plt.title('Latência média ao longo do tempo - Todos os Continentes')
    plt.xlabel('Tempo (Intervalos de 2 horas)')
    plt.ylabel('Latência média (ms)')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title="Continentes")
    plt.tight_layout()

    # Salvar o gráfico como imagem
    plt.savefig('latency_combined_continents.png')
    plt.show()

# Chamar as funções para gerar gráficos
plot_country_latency_graphs(latency_data_country)  # Gráficos separados por país
plot_combined_country_latency_graph(latency_data_country)  # Gráfico combinado de todos os países
plot_continent_graphs(latency_data_continent)  # Gráficos separados por continente
plot_combined_continent_graph(latency_data_continent)  # Gráfico combinado de todos os continentes