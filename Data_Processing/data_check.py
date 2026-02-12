import pandas as pd
import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

# ==========================================
# CONFIGURATION
# ==========================================
FILE_PATH = 'rescued_data_09.csv'  # REPLACE with your actual filename
FS = 1091                         # Your sampling rate
RPM = 3000                        # Motor Speed

def analyze_unbalance():
    print(f"--- ANALYZING: {FILE_PATH} ---")
    
    try:
        # 1. Load specifically columns 1, 2, 3 (X, Y, Z) to avoid Timestamp/Label issues
        # The file has: Timestamp, X, Y, Z, Label
        # Indices:      0,         1, 2, 3, 4
        df = pd.read_csv(FILE_PATH, usecols=[1, 2, 3])
        
        # Ensure clean numbers
        df = df.apply(pd.to_numeric, errors='coerce').dropna()
        
        print(f"Loaded {len(df)} samples.")
        
        if len(df) == 0:
            print("Error: File is empty or could not be read.")
            return

        # 2. Check for Saturation (Clipping)
        max_val = df.max().max()
        min_val = df.min().min()
        print(f"\n[Range Check]")
        print(f"Max Value: {max_val}")
        print(f"Min Value: {min_val}")
        
        if max_val >= 1023 or min_val <= -1024:
            print(">> WARNING: SENSOR SATURATION DETECTED!")
            print(">> The vibration is too strong for the sensor's current range.")
            print(">> This is a PERFECT indicator of a severe fault.")

        # 3. Calculate Energy (RMS) - The "Loudness"
        # Center the data first
        x_centered = df['X'] - df['X'].mean()
        rms_val = np.sqrt(np.mean(x_centered**2))
        
        # 4. Frequency Analysis (FFT) - The "Pitch"
        N = len(df)
        yf = fft(x_centered.values)
        xf = fftfreq(N, 1/FS)[:N//2]
        yf_mag = 2.0/N * np.abs(yf[0:N//2])
        
        # Find 1x RPM Peak (50 Hz)
        target_freq = RPM / 60
        idx = (np.abs(xf - target_freq)).argmin()
        peak_1x = yf_mag[idx]
        
        print(f"\n[Classification Metrics]")
        print(f"1. RMS Energy (Volume):    {rms_val:.2f}")
        print(f"2. 1x RPM Amplitude (50Hz): {peak_1x:.2f}")
        
        # 5. Simple Plot to verify Saturation
        plt.figure(figsize=(10, 4))
        plt.plot(df['X'].iloc[:200], label='X-Axis') # Only plot first 200 samples
        plt.title("First 200 Samples (Look for flat tops/clipping)")
        plt.axhline(1023, color='r', linestyle='--', label='Max Limit')
        plt.axhline(-1024, color='r', linestyle='--', label='Min Limit')
        plt.legend()
        plt.grid(True)
        plt.show()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_unbalance()