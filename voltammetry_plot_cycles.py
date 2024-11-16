'''

You need to change the pH variable (!)

It has a smoothing filter option commented out

You can also plot only the cathodic scan, see section with cathodic_end_idx = None

'''


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib as mpl
from matplotlib.ticker import ScalarFormatter
from matplotlib.cm import get_cmap
from scipy.signal import savgol_filter

mpl.use('SVG')
mpl.rcParams['svg.fonttype'] = 'none'  # Do not convert fonts to paths

csv_directory = r"..."
output_folder = os.path.join(csv_directory, "Voltammograms plotted")
os.makedirs(output_folder, exist_ok=True)

cmap = get_cmap('magma')

diameter = 7  # mm
area = (np.pi * ((diameter / 1000) / 2) ** 2)  # pi * (d/2)^2 in m^2
scan_rate = 10 / 1000  # 10 mV/s converted to V/s

pH = 6.5
conversion_factor_RHE = 0.197 + 0.059 * pH  # V

for filename in os.listdir(csv_directory):
    if filename.endswith(".csv"):
        csv_file_path = os.path.join(csv_directory, filename)
        try:
            df = pd.read_csv(csv_file_path, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(csv_file_path, encoding='latin-1')

        script_file_name = os.path.splitext(filename)[0]

        df = df.iloc[1:, :]
        
        # Smooth the current columns (odd-numbered)
#        for col in df.columns[1::2]:
#            df[col] = savgol_filter(df[col].astype(float), window_length=5, polyorder=2)  # Apply Savitzky-Golay filter

        plt.figure()
        plt.figure()
        plt.figure()
        
        num_cycles = df.shape[1] // 2
        min_voltage_AgAgCl = float('inf')
        max_voltage_AgAgCl = float('-inf')
        min_voltage_RHE = float('inf')
        max_voltage_RHE = float('-inf')

        for i in range(num_cycles):
            voltage_column = df.columns[2 * i]
            current_column = df.columns[2 * i + 1]

            voltage_AgAgCl = df[voltage_column].astype(float)
            voltage_RHE = voltage_AgAgCl + conversion_factor_RHE  # Convert to RHE
            current = df[current_column].astype(float)
            current_density = (current / 1000000) / area  # Convert µA to A and then to A/m^2
            capacitance = current_density / scan_rate  # Calculate capacitance

            # Detect the end of the cathodic scan
            cathodic_end_idx = None
            for j in range(1, len(voltage_RHE) - 1):
                if voltage_RHE.iloc[j - 1] > voltage_RHE.iloc[j] < voltage_RHE.iloc[j + 1]:
                    cathodic_end_idx = j
                    break
            
            # Plot only the cathodic scan (up to cathodic_end_idx)
            if cathodic_end_idx:
                voltage_AgAgCl_cathodic = voltage_AgAgCl[:cathodic_end_idx]
                voltage_RHE_cathodic = voltage_RHE[:cathodic_end_idx]
                current_density_cathodic = current_density[:cathodic_end_idx]
                capacitance_cathodic = capacitance[:cathodic_end_idx]

                color = cmap(i / num_cycles)
                plt.figure(1)
                plt.plot(voltage_AgAgCl_cathodic, current_density_cathodic, label=f'Cycle {i + 1}', color=color)
                plt.figure(2)
                plt.plot(voltage_AgAgCl_cathodic, capacitance_cathodic, label=f'Cycle {i + 1}', color=color)

        # Plot for current density (Cathodic)
        plt.figure(1)
        plt.xlabel('Voltage (V) vs Ag/AgCl')
        plt.ylabel('Current Density (A/m^2)')
        plt.title(f'{script_file_name} - Cathodic Scans')
        plt.gca().get_yaxis().set_major_formatter(ScalarFormatter(useMathText=False))
        plt.legend()
        file_name = os.path.join(output_folder, f"{script_file_name}_cathodic_density_AgAgCl")
        plt.savefig(file_name + ".png", dpi=300)
        plt.savefig(file_name + ".svg")
        plt.close()

        # Plot for capacitance (Cathodic)
        plt.figure(2)
        plt.xlabel('Voltage (V) vs Ag/AgCl')
        plt.ylabel('Capacitance (F/m^2)')
        plt.title(f'{script_file_name} - Cathodic Scans')
        plt.gca().get_yaxis().set_major_formatter(ScalarFormatter(useMathText=False))
        plt.legend()
        file_name = os.path.join(output_folder, f"{script_file_name}_cathodic_capacitance_AgAgCl")
        plt.savefig(file_name + ".png", dpi=300)
        plt.savefig(file_name + ".svg")
        plt.close()

        # RHE plots (Cathodic)
        plt.figure()
        plt.figure()
        plt.figure()

        for i in range(num_cycles):
            voltage_column = df.columns[2 * i]
            current_column = df.columns[2 * i + 1]

            voltage_AgAgCl = df[voltage_column].astype(float)
            voltage_RHE = voltage_AgAgCl + conversion_factor_RHE  # Convert to RHE
            current = df[current_column].astype(float)
            current_density = (current / 1000000) / area  # Convert µA to A and then to A/m^2
            capacitance = current_density / scan_rate  # Calculate capacitance

            # Detect the end of the cathodic scan
            cathodic_end_idx = None
            for j in range(1, len(voltage_RHE) - 1):
                if voltage_RHE.iloc[j - 1] > voltage_RHE.iloc[j] < voltage_RHE.iloc[j + 1]:
                    cathodic_end_idx = j
                    break
            
            # Plot only the cathodic scan (up to cathodic_end_idx)
            if cathodic_end_idx:
                voltage_RHE_cathodic = voltage_RHE[:cathodic_end_idx]
                current_density_cathodic = current_density[:cathodic_end_idx]
                capacitance_cathodic = capacitance[:cathodic_end_idx]

                color = cmap(i / num_cycles)
                plt.figure(1)
                plt.plot(voltage_RHE_cathodic, current_density_cathodic, label=f'Cycle {i + 1}', color=color)
                plt.figure(2)
                plt.plot(voltage_RHE_cathodic, capacitance_cathodic, label=f'Cycle {i + 1}', color=color)

        # Plot for current density (Cathodic)
        plt.figure(1)
        plt.xlabel('Voltage vs RHE (V)')
        plt.ylabel('Current (µA)')
        plt.title(f'{script_file_name} - Cathodic Scans (RHE)')
        plt.gca().get_yaxis().set_major_formatter(ScalarFormatter(useMathText=False))
        plt.legend()
        file_name = os.path.join(output_folder, f"{script_file_name}_cathodic_density_RHE")
        plt.savefig(file_name + ".png", dpi=300)
        plt.savefig(file_name + ".svg")
        plt.close()

        # Plot for capacitance (Cathodic)
        plt.figure(2)
        plt.xlabel('Voltage vs RHE (V)')
        plt.ylabel('Capacitance (F/m^2)')
        plt.title(f'{script_file_name} - Cathodic Scans (RHE)')
        plt.gca().get_yaxis().set_major_formatter(ScalarFormatter(useMathText=False))
        plt.legend()
        file_name = os.path.join(output_folder, f"{script_file_name}_cathodic_capacitance_RHE")
        plt.savefig(file_name + ".png", dpi=300)
        plt.savefig(file_name + ".svg")
        plt.close()
