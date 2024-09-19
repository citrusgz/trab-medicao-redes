import json
import matplotlib.pyplot as plt
from collections import defaultdict
from probs import get_country_by_prb_id, get_continent_by_prb_id

# Carregar os dados do arquivo JSON (chine_essential.json)
with open('belarus_essential.json', 'r') as f:
    traceroutes = json.load(f)

# Dicionário para armazenar a relação entre número de hops e latência agrupados por continente
hops_latency_data_continent = defaultdict(lambda: {'latency': [], 'hops': []})
hops_latency_data_country = defaultdict(lambda: {'latency': [], 'hops': []})

# Preencher o dicionário com latências e hops para cada continente
for trace in traceroutes:
    prb_id = trace['prb_id']
    country = get_country_by_prb_id(prb_id)
    continent = get_continent_by_prb_id(prb_id)
    avg_rtt = trace['avg_rtt']
    num_hops = trace['hop_number']

    # Somente armazenar se tanto a latência quanto o número de hops forem válidos
    if continent != "Unknown" and avg_rtt is not None and num_hops is not None:
        hops_latency_data_continent[continent]['latency'].append(avg_rtt)
        hops_latency_data_continent[continent]['hops'].append(num_hops)
        hops_latency_data_country[country]['latency'].append(avg_rtt)
        hops_latency_data_country[country]['hops'].append(num_hops)

# Função para gerar gráficos de relação entre hops e latência por país
def plot_country_hops_latency_graphs(hops_latency_data_country):

    # Iterar sobre os países e gerar um gráfico para cada um
    for country, data in hops_latency_data_country.items():
        latencies = data['latency']
        hops = data['hops']

        # Plotar o gráfico se houver dados válidos
        if latencies and hops:
            plt.figure(figsize=(10, 6))
            plt.scatter(latencies, hops, label=f'{country}', alpha=0.6, edgecolor='k')
            plt.title(f'Relação entre Latência e Número de Hops - {country}')
            plt.xlabel('Latência média (ms)')
            plt.ylabel('Número de Hops')
            plt.tight_layout()

            # Salvar o gráfico como imagem
            plt.savefig(f'hops_latency_{country}.png')
            plt.show()

# Função para gerar um gráfico combinado de todos os países (hops vs latência)
def plot_combined_country_hops_latency_graph(hops_latency_data_country):
    plt.figure(figsize=(12, 8))

    # Iterar sobre os países e adicionar ao gráfico combinado
    for country, data in hops_latency_data_country.items():
        latencies = data['latency']
        hops = data['hops']

        # Plotar os dados se houver latências e hops válidos
        if latencies and hops:
            plt.scatter(latencies, hops, label=f'{country}', alpha=0.6, edgecolor='k')

    # Customizar o gráfico
    plt.title('Relação entre Latência e Número de Hops - Todos os Países')
    plt.xlabel('Latência média (ms)')
    plt.ylabel('Número de Hops')
    plt.legend(title="Países")
    plt.tight_layout()

    # Salvar o gráfico como imagem
    plt.savefig('hops_latency_combined_countries.png')
    plt.show()

# Função para gerar gráficos de relação entre hops e latência por continente
def plot_continent_hops_latency_graphs(hops_latency_data_continent):

    # Iterar sobre os continentes e gerar um gráfico para cada um
    for continent, data in hops_latency_data_continent.items():
        latencies = data['latency']
        hops = data['hops']

        # Plotar o gráfico se houver dados válidos
        if latencies and hops:
            plt.figure(figsize=(10, 6))
            plt.scatter(latencies, hops, label=f'{continent}', alpha=0.6, edgecolor='k')
            plt.title(f'Relação entre Latência e Número de Hops - {continent}')
            plt.xlabel('Latência média (ms)')
            plt.ylabel('Número de Hops')
            plt.tight_layout()

            # Salvar o gráfico como imagem
            plt.savefig(f'hops_latency_{continent}.png')
            plt.show()

# Função para gerar um gráfico combinado de todos os continentes (hops vs latência)
def plot_combined_continent_hops_latency_graph(hops_latency_data_continent):
    plt.figure(figsize=(12, 8))

    # Iterar sobre os continentes e adicionar ao gráfico combinado
    for continent, data in hops_latency_data_continent.items():
        latencies = data['latency']
        hops = data['hops']

        # Plotar os dados se houver latências e hops válidos
        if latencies and hops:
            plt.scatter(latencies, hops, label=f'{continent}', alpha=0.6, edgecolor='k')

    # Customizar o gráfico
    plt.title('Relação entre Latência e Número de Hops - Todos os Continentes')
    plt.xlabel('Latência média (ms)')
    plt.ylabel('Número de Hops')
    plt.legend(title="Continentes")
    plt.tight_layout()

    # Salvar o gráfico como imagem
    plt.savefig('hops_latency_combined_continents.png')
    plt.show()

# Chamar as funções para gerar gráficos
#plot_country_hops_latency_graphs(hops_latency_data_country)
plot_combined_country_hops_latency_graph(hops_latency_data_country)
#plot_continent_hops_latency_graphs(hops_latency_data_continent)  
#plot_combined_continent_hops_latency_graph(hops_latency_data_continent)