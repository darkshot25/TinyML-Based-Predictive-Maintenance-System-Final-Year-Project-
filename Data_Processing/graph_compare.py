import pandas as pd
import matplotlib.pyplot as plt

# LOAD YOUR FILES
FILE_NOMINAL = 'cleaned_data_17.csv'  # The RMS ~450 file
FILE_FAULT = 'cleaned_data_15.csv'        # The RMS ~800 file (Saturated)

# Load data
df_nom = pd.read_csv(FILE_NOMINAL)
df_fault = pd.read_csv(FILE_FAULT)

# Plot Comparison
plt.figure(figsize=(12, 6))

# Plot 200 samples of Nominal
plt.plot(df_nom['X'].iloc[:200], color='green', label='Healthy Data', alpha=0.8)

# Plot 200 samples of Fault
plt.plot(df_fault['X'].iloc[:200], color='red', label='Parasitic Unbalance', alpha=0.8)

plt.title("Class Separation Verification: Nominal vs. Fault", fontsize=18)
plt.xlabel("Sample Count", fontsize=18)
plt.ylabel("Amplitude", fontsize=18)
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()