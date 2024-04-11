import requests
import datetime
from prettytable import PrettyTable

addresses = ['address',
             ]

data_list = []

for address in addresses:
    url = 'https://www.heurist.ai/api/mining_data'
    params = {'address': address}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        total_llama_points = round(float(data['data']['totalLlamaPoints']), 2)
        total_waifu_points = round(float(data['data']['totalWaifuPoints']), 2)
        inference_history = data['data']['inferenceHistory']
        
        # Find the maximum timestamp for Llama and Waifu models
        if any('openhermes' in x['model_id'] for x in inference_history):
            llama_max_timestamp = max([float(x['timestamp']) for x in inference_history if 'openhermes' in x['model_id']])
            llama_datetime = datetime.datetime.fromtimestamp(llama_max_timestamp / 1000)
            llama_minutes = round((datetime.datetime.now() - llama_datetime).total_seconds() / 60, 2)
            waifu_max_timestamps = [float(x['timestamp']) for x in inference_history if 'openhermes' not in x['model_id']]
            if waifu_max_timestamps:
                waifu_max_timestamp = max(waifu_max_timestamps)
                waifu_datetime = datetime.datetime.fromtimestamp(waifu_max_timestamp / 1000)
                waifu_minutes = round((datetime.datetime.now() - waifu_datetime).total_seconds() / 60, 2)
            else:
                waifu_max_timestamp = 'null'
                waifu_minutes = 'N/A'
        else:
            llama_max_timestamp = 'null'
            llama_minutes = 'N/A'
            waifu_max_timestamps = [float(x['timestamp']) for x in inference_history]
            if waifu_max_timestamps:
                waifu_max_timestamp = max(waifu_max_timestamps)
                waifu_datetime = datetime.datetime.fromtimestamp(waifu_max_timestamp / 1000)
                waifu_minutes = round((datetime.datetime.now() - waifu_datetime).total_seconds() / 60, 2)
            else:
                waifu_max_timestamp = 'null'
                waifu_minutes = 'N/A'
        
        # Append the data to the list
        data_list.append([params['address'][-4:], total_llama_points, total_waifu_points, waifu_minutes, llama_minutes])
    else:
        print('Failed to retrieve data for address', address)

# Create a table and add the data
table = PrettyTable()
table.field_names = ["Address", "Total Llama Points", "Total Waifu Points", "Waifu minutes since max timestamp", "Llama minutes since max timestamp"]

for data in data_list:
    table.add_row(data)

# Print the table
print(table)