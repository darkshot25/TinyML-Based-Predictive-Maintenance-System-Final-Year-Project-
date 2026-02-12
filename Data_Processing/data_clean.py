import pandas as pd
import numpy as np
import scipy.stats as stats
import os

# ==========================================
# CONFIGURATION
# ==========================================
INPUT_FILE = 'simulated_unbalance_data.csv'      # CHANGE THIS to your filename
OUTPUT_FILE = 'simulated_cleaned_unbalance.csv'     # Result will be saved here
Z_THRESHOLD = 3.0                          # Outlier threshold (Standard is 3.0)

def master_pipeline(input_path, output_path):
    print(f"--- STARTING PIPELINE FOR: {input_path} ---")

    # ---------------------------------------------------------
    # STEP 1: SMART LOAD
    # ---------------------------------------------------------
    print("1. Loading Data...")
    if not os.path.exists(input_path):
        print("Error: File not found.")
        return

    try:
        # Try reading with header first
        df = pd.read_csv(input_path, header=0)
        # If columns aren't X,Y,Z, try to find them or assume raw
        if not {'X', 'Y', 'Z'}.issubset(df.columns):
            # Fallback: Read as raw numbers, take last 3 cols
            df = pd.read_csv(input_path, header=None)
            df = df.iloc[:, -3:]
            df.columns = ['X', 'Y', 'Z']
        
        # Keep only X, Y, Z and force numeric
        df = df[['X', 'Y', 'Z']].apply(pd.to_numeric, errors='coerce').dropna()
        print(f"   Loaded {len(df)} samples.")
        
    except Exception as e:
        print(f"   Error loading: {e}")
        return

    # ---------------------------------------------------------
    # STEP 2: CRASH TRIMMING (Garbage Collection)
    # ---------------------------------------------------------
    print("2. Detecting Sensor Crashes...")
    original_len = len(df)
    
    # A. Detect All Zeros (Sensor Reset)
    zero_mask = (df['X'] == 0) & (df['Y'] == 0) & (df['Z'] == 0)
    zero_indices = df.index[zero_mask]
    cutoff_idx = len(df)

    if len(zero_indices) > 0:
        # Check for block of 5 zeros
        for idx in zero_indices:
            if idx + 5 < len(df) and zero_mask.loc[idx:idx+4].all():
                cutoff_idx = idx
                print(f"   -> Trimmed: Sensor reset found at sample {idx}")
                break

    # B. Detect Frozen Values (SPI Bus Crash)
    # Check if value doesn't change for 50 samples
    diffs = df.diff().abs().sum(axis=1)
    is_frozen = diffs.rolling(window=50).sum() == 0
    frozen_indices = df.index[is_frozen]
    
    if len(frozen_indices) > 0:
        freeze_point = frozen_indices[0] - 50
        if freeze_point < cutoff_idx:
            cutoff_idx = max(0, freeze_point)
            print(f"   -> Trimmed: Sensor freeze found at sample {cutoff_idx}")

    # Apply Trim
    df = df.iloc[:cutoff_idx].copy()
    print(f"   Data kept: {len(df)} samples ({len(df)/original_len*100:.1f}%)")

    if len(df) < 100:
        print("   ERROR: Remaining data is too short to process.")
        return

    # ---------------------------------------------------------
    # STEP 3: Z-SCORE FILTER (Noise Removal)
    # ---------------------------------------------------------
    print(f"3. Applying Z-Score Filter (Threshold {Z_THRESHOLD}σ)...")
    
    # Calculate initial stats for comparison
    raw_kurt = df.kurtosis()
    
    # Identify outliers
    z_scores = np.abs(stats.zscore(df))
    outlier_mask = (z_scores > Z_THRESHOLD).any(axis=1)
    num_outliers = outlier_mask.sum()
    
    # Replace outliers with NaN and interpolate
    df_clean = df.copy()
    df_clean[outlier_mask] = np.nan
    df_clean = df_clean.interpolate(method='linear', limit_direction='both')
    
    print(f"   Removed {num_outliers} spikes (electrical noise).")

    # ---------------------------------------------------------
    # STEP 4: VERIFICATION & SAVING
    # ---------------------------------------------------------
    print("4. Final Analysis...")
    
    # Calculate Kurtosis (Pandas does this column-wise automatically)
    clean_kurt = df_clean.kurtosis()
    
    # Calculate RMS Energy (Use Pandas .mean() to ensure column-wise calculation)
    # Formula: Square -> Mean -> Square Root
    clean_rms = ((df_clean - df_clean.mean())**2).mean()**0.5
    
    print("\n   --- METRICS SUMMARY ---")
    # We use .get() to safely grab X even if something weird happens, preventing crashes
    kurt_x = clean_kurt.get('X', 0)
    rms_x = clean_rms.get('X', 0)
    
    print(f"   Kurtosis (X): Raw {raw_kurt.get('X',0):.2f} -> Clean {kurt_x:.2f} (Target ~3.0)")
    print(f"   RMS Energy (X): {rms_x:.2f}")

    # Save
    df_clean.to_csv(output_path, index=False)
    print(f"\nSUCCESS: Clean file saved to '{output_path}'")

if __name__ == "__main__":
    master_pipeline(INPUT_FILE, OUTPUT_FILE)