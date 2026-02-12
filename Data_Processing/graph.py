import pandas as pd
import matplotlib.pyplot as plt

# Load the CLEAN file you just generated
FILE_PATH = 'simulated_contamination_data.csv' 

df = pd.read_csv(FILE_PATH)

plt.figure(figsize=(12, 6))
# Plot only first 1000 samples so we can see the wave shape clearly
plt.plot(df['X'].iloc[:1000], label='Cleaned X', color='red')
plt.plot(df['Y'].iloc[:1000], label='Cleaned Y', color='green')
plt.plot(df['Z'].iloc[:1000], label='Cleaned Z', color='blue')

plt.title("Zoomed View of Cleaned Data (First 1000 samples)")
plt.ylabel("Acceleration")
plt.xlabel("Sample Count")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()