#!/usr/bin/env python3
"""
Quick proof visualization: Is SincNet learning?
This script analyzes the saved CSV data and creates a clear proof visualization.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load the data
csv_path = Path('sincnet_epoch_bands.csv')
if not csv_path.exists():
    print(f"❌ File not found: {csv_path}")
    exit(1)

df = pd.read_csv(csv_path)
print(f"Loaded {len(df)} epochs of SincNet data\n")

# Get initial and final states
n_filters = 8
n_epochs = len(df) - 1  # Exclude epoch 0

# Calculate changes for each filter
changes_center = []
changes_bandwidth = []

for f in range(n_filters):
    center_col = f'center_hz_F{f}'
    bw_col = f'bandwidth_hz_F{f}'
    
    center_init = df.loc[0, center_col]
    center_final = df.loc[n_epochs, center_col]
    center_change = abs(center_final - center_init)
    
    bw_init = df.loc[0, bw_col]
    bw_final = df.loc[n_epochs, bw_col]
    bw_change = abs(bw_final - bw_init)
    
    changes_center.append(center_change)
    changes_bandwidth.append(bw_change)

changes_center = np.array(changes_center)
changes_bandwidth = np.array(changes_bandwidth)

# Create proof visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('SincNet Layer Learning Proof', fontsize=16, fontweight='bold')

# Plot 1: Center frequency changes per filter
ax = axes[0, 0]
colors = ['green' if x > 0.01 else 'red' for x in changes_center]
ax.bar(range(n_filters), changes_center, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
ax.set_title('Center Frequency Change (Hz)', fontweight='bold', fontsize=12)
ax.set_xlabel('Filter')
ax.set_ylabel('Δ Center (Hz)')
ax.grid(True, alpha=0.3, axis='y')
ax.axhline(y=0.01, color='orange', linestyle='--', label='Threshold (0.01 Hz)', alpha=0.5)
ax.legend()

# Plot 2: Bandwidth changes per filter
ax = axes[0, 1]
colors = ['green' if x > 0.01 else 'red' for x in changes_bandwidth]
ax.bar(range(n_filters), changes_bandwidth, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
ax.set_title('Bandwidth Change (Hz)', fontweight='bold', fontsize=12)
ax.set_xlabel('Filter')
ax.set_ylabel('Δ Bandwidth (Hz)')
ax.grid(True, alpha=0.3, axis='y')
ax.axhline(y=0.01, color='orange', linestyle='--', label='Threshold (0.01 Hz)', alpha=0.5)
ax.legend()

# Plot 3: Summary statistics
ax = axes[1, 0]
ax.axis('off')

max_center_change = np.max(changes_center)
max_bw_change = np.max(changes_bandwidth)
mean_center_change = np.mean(changes_center)
mean_bw_change = np.mean(changes_bandwidth)

summary_text = f"""
LEARNING PROOF SUMMARY

Training: {n_epochs} epochs

Center Frequency Changes:
  Max change: {max_center_change:.4f} Hz
  Mean change: {mean_center_change:.4f} Hz
  
Bandwidth Changes:
  Max change: {max_bw_change:.4f} Hz
  Mean change: {mean_bw_change:.4f} Hz

VERDICT:
"""

ax.text(0.05, 0.95, summary_text, transform=ax.transAxes, 
        fontsize=11, verticalalignment='top', fontfamily='monospace',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Plot 4: Learning verdict
ax = axes[1, 1]
ax.axis('off')

if max_center_change > 0.1 or max_bw_change > 0.1:
    verdict = "✅ YES, SincNet IS LEARNING"
    color = 'lightgreen'
    explanation = "Frequency bands changed significantly\nModel adapted to dataset"
elif max_center_change > 0.01 or max_bw_change > 0.01:
    verdict = "⚠️  SLOW LEARNING"
    color = 'lightyellow'
    explanation = "Small changes detected\nLearning rate may need adjustment"
else:
    verdict = "❌ NO, SincNet NOT LEARNING"
    color = 'lightcoral'
    explanation = "Frequency bands are frozen\nParameters not updating"

ax.text(0.5, 0.6, verdict, transform=ax.transAxes, 
        fontsize=16, fontweight='bold', ha='center', va='center',
        bbox=dict(boxstyle='round,pad=1', facecolor=color, edgecolor='black', linewidth=2))

ax.text(0.5, 0.25, explanation, transform=ax.transAxes, 
        fontsize=11, ha='center', va='center', style='italic')

plt.tight_layout()
plt.savefig('sincnet_learning_proof.png', dpi=150, bbox_inches='tight')
print("\n" + "="*70)
print(summary_text + verdict)
print("="*70)
print(f"\nVisualization saved to: sincnet_learning_proof.png")
plt.show()
