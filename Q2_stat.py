import pandas as pd
import numpy as np
from scipy.stats import pearsonr

# Function to calculate correlation between pairs of indices
def calculate_correlations(index_pairs, index_data):
    correlations = {}
    for pair in index_pairs:
        index1, index2 = pair
        corr, _ = pearsonr(index_data[index1], index_data[index2])
        correlations[f'{index1}-{index2}'] = corr
    return correlations

# Function to calculate spike differentials for each index
def calculate_spike_differentials(premium_data):
    spike_differentials = {}
    for index, premium in premium_data.items():
        baseline_period = premium_data[index].rolling(window=20).mean()  # Use a 20-day rolling average as the baseline
        peak_period = premium_data[index].rolling(window=5).max()  # Use a 5-day window to detect spikes
        spike_differential = ((peak_period - baseline_period) / baseline_period) * 100
        spike_differentials[index] = spike_differential
    return spike_differentials

if __name__ == "__main__":
    # Example index pairs
    index_pairs = [('SENSEX', 'NIFTY'), ('SENSEX', 'FINNIFTY'), ('SENSEX', 'BANKEX'), ('NIFTY', 'FINNIFTY'), ('NIFTY', 'BANKEX'), ('FINNIFTY', 'BANKEX')]
    
    # Example index data (replace with actual data)
    index_data = {
        'SENSEX': pd.Series(np.random.randn(100)),
        'NIFTY': pd.Series(np.random.randn(100)),
        'FINNIFTY': pd.Series(np.random.randn(100)),
        'BANKEX': pd.Series(np.random.randn(100))
    }
    
    # Example premium data (replace with actual data)
    premium_data = {
        'SENSEX': pd.Series(np.random.randn(100)),
        'NIFTY': pd.Series(np.random.randn(100)),
        'FINNIFTY': pd.Series(np.random.randn(100)),
        'BANKEX': pd.Series(np.random.randn(100))
    }
    
    # Calculate correlations between index pairs
    correlations = calculate_correlations(index_pairs, index_data)
    
    # Calculate spike differentials for each index
    spike_differentials = calculate_spike_differentials(premium_data)
    
    # Print correlations
    print("Correlations:")
    for pair, corr in correlations.items():
        print(f"{pair}: {corr}")
    
    # Print spike differentials
    print("\nSpike Differentials:")
    for index, spike_diff in spike_differentials.items():
        print(f"{index}:")
        print(spike_diff)
