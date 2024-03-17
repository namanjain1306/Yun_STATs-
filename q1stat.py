import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Function to retrieve historical straddle theta decay data
def get_straddle_data(index_name, expiry_date):
    api_url = f"https://example.com/api/history/decay?index={index_name}&expiry={expiry_date}&dte="
    straddle_data = []
    for dte in range(4, -1, -1):
        response = requests.get(api_url + str(dte))
        if response.status_code == 200:
            data = response.json()
            straddle_data.extend(data)
    return straddle_data

# Function to calculate straddle price
def calculate_straddle_price(call_price, put_price):
    return call_price + put_price

# Function to calculate correlation between pairs of indices
def calculate_correlation(index1_data, index2_data):
    return np.corrcoef(index1_data, index2_data)[0, 1]

# Function to quantify spike differentials
def quantify_spike_differentials(data):
    spike_differentials = []
    for i in range(1, len(data)):
        spike = data[i] - data[i-1]
        spike_differentials.append(spike)
    return spike_differentials

# Main function
if __name__ == "__main__":
    # List of indices
    indices = ['NIFTY', 'SENSEX', 'FINNIFTY', 'BANKEX']
    
    # Get expiry dates for FINNIFTY
    expiry_response = requests.get("https://example.com/api/history/expiries?index=FINNIFTY")
    if expiry_response.status_code == 200:
        expiry_dates = expiry_response.json()
        # Choose the latest expiry date
        latest_expiry = expiry_dates[0]
        
        # Fetch straddle data for each index
        straddle_data = {}
        for index in indices:
            straddle_data[index] = get_straddle_data(index, latest_expiry)
        
        # Calculate straddle prices for each index
        for index, data in straddle_data.items():
            for entry in data:
                entry['straddle_price'] = calculate_straddle_price(entry['callPrice'], entry['putPrice'])
        
        # Calculate correlation between pairs of indices
        correlation_matrix = pd.DataFrame(index=indices, columns=indices)
        for index1 in indices:
            for index2 in indices:
                correlation = calculate_correlation([entry['straddle_price'] for entry in straddle_data[index1]],
                                                    [entry['straddle_price'] for entry in straddle_data[index2]])
                correlation_matrix.loc[index1, index2] = correlation
        
        print("Correlation Matrix:")
        print(correlation_matrix)
        
        # Quantify spike differentials for an index
        index_name = 'NIFTY'  # Example index
        spike_differentials = quantify_spike_differentials([entry['straddle_price'] for entry in straddle_data[index_name]])
        print(f"Spike Differentials for {index_name}:")
        print(spike_differentials)
    else:
        print("Failed to retrieve expiry dates.")
