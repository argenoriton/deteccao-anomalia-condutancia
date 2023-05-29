import pandas as pd


def find_spike(spike_threshold, conductance_data, start_time=None, end_time=None):

    conductance_data['conductance'] = conductance_data['conductance'].str.replace(
        ' uS/cm', '').astype(float)
    conductance_data['Time'] = pd.to_datetime(
        conductance_data['Time'], format="%d/%m/%Y %H:%M")

    if start_time is None:
        start_time = conductance_data['Time'].iloc[0] if not conductance_data.empty else None

    if end_time is None:
        end_time = conductance_data['Time'].iloc[-1] if not conductance_data.empty else None

    conductance_data_filtered = filter_values_by_time(
        conductance_data, start_time, end_time)

    if conductance_data_filtered.empty:
        print("Datas inválidas.")
        return []

    spike_list = []

    print("* Periodo Testado:")
    for _, data in conductance_data_filtered.iterrows():
        time = data['Time']
        conductance = data['conductance']
        print(f"Time: {time}, Conductance: {conductance}")

    for i in range(1, len(conductance_data_filtered)):
        current_data = conductance_data_filtered.iloc[i]
        previous_data = conductance_data_filtered.iloc[i-1]
        conductance_diff = current_data['conductance'] - \
            previous_data['conductance']
        if conductance_diff >= spike_threshold:
            spike_list.append({
                'Time': current_data['Time'],
                'conductance': current_data['conductance']
            })

    return spike_list


def filter_values_by_time(conductance_data, start_time=None, end_time=None):

    if start_time > end_time:
        return pd.DataFrame()

    conductance_data_filtered = conductance_data[
        (conductance_data['Time'] >= start_time) & (
            conductance_data['Time'] <= end_time)
    ]

    return conductance_data_filtered


conductance_data = pd.read_csv(
    'Conductance/Conductance-data-2023-05-16 17 31 24.csv', sep=';')

# Definir data inicial e data final

start_time = None
# datetime.datetime.strptime("16/04/2023 17:57", "%d/%m/%Y %H:%M")
end_time = None
# datetime.datetime.strptime("16/04/2023 19:26", "%d/%m/%Y %H:%M")

# Definir parametro para pico
spike_threshold = 40

# Chamar a função para encontrar os valores de condutância entre as datas
spikes = find_spike(spike_threshold, conductance_data, start_time, end_time)

# Exibir os valores encontrados
print("* Picos: ")
print(spikes)
