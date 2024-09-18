import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_aggregated_hops_by_destination(file1, file2, file3, probes_file):
    # Carregar os dados dos arquivos JSON
    data1 = pd.read_json(file1)
    data2 = pd.read_json(file2)
    data3 = pd.read_json(file3)
    probes_data = pd.read_json(probes_file)

    # Concatenar os dados dos três arquivos
    continent_data = pd.concat([data1, data2, data3])

    # Mesclar os dados do continente com os dados dos probes para informações adicionais
    merged_data = continent_data.merge(probes_data.T, left_on='prb_id', right_index=True)

    # Converter timestamp para datetime
    merged_data['timestamp'] = pd.to_datetime(merged_data['timestamp'], unit='s')

    # Reamostrar os dados em intervalos de 2 horas, calculando a média dos saltos (hops) dentro de cada intervalo
    numeric_columns = merged_data.select_dtypes(include='number').columns
    resampled_data = merged_data.set_index('timestamp').groupby(['dst_name', 'continente', 'nome'])[numeric_columns].resample('2h').mean().reset_index()

    # Agregar os dados por destino e timestamp
    numeric_columns = resampled_data.select_dtypes(include='number').columns
    aggregated_df = resampled_data.groupby(['dst_name', 'timestamp'])[numeric_columns].mean().reset_index()

    # Plotar o gráfico
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='timestamp', y='hop_number', hue='dst_name', data=aggregated_df)
    plt.title('Número de Saltos Agregado por Destino (Agrupado em 2 horas)')
    plt.xlabel('Timestamp')
    plt.ylabel('Número Médio de Saltos')
    plt.legend(title='Destino')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Exemplo de uso
plot_aggregated_hops_by_destination('china_essential.json', 'belarus_essential.json', 'uk_essential.json', 'probes.json')
