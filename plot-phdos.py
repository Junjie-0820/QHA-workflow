#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import os

def get_total_dos(file_path):
    data = np.loadtxt(file_path, skiprows=1)
    freq = data[:, 0]
    total_dos = np.sum(data[:, 1:], axis=1)
    return freq, total_dos

def main():
    scal_fac = ["0.99", "1.000", "1.01", "1.02", "1.03", "1.04"]
#     scal_fac = ["1", "2", "3", "4", "5", "6"]
    
    cold_color = np.array([0, 0, 1])  # blue
    warm_color = np.array([1, 0, 0])  # red
    n = len(scal_fac)
    
    plt.figure(figsize=(8,6))
    
    for idx, sf in enumerate(scal_fac):
        folder = f"{sf}"
        file_path = os.path.join(folder, "total_dos.dat")
        if not os.path.exists(file_path):
            print(f"Warning: {file_path} does not exist, skipping.")
            continue
        
        freq, total_dos = get_total_dos(file_path)
        
        frac = idx / (n - 1) if n > 1 else 0
        color = (1 - frac) * cold_color + frac * warm_color
        
        plt.plot(freq, total_dos, linestyle='-', linewidth=2, color=color, label=f"scal_fac = {sf}")
    
    plt.xlabel("Frequency(THz)")
    plt.ylabel("PhDOS(THz^-1)")
#    plt.title("")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("ph_tdos.png")
#    plt.show()

if __name__ == "__main__":
    main()

