# -*- coding: utf-8 -*-
"""
Code for automated data preprocessing
Import
Sorting data
    - Group by cycle
    - 1. VvsCap / CC-Ch and CV-Ch combined and separeted from CC-Dch
    - 2. CapvsCyc incl. CE
    - 3. dqdVvsV 
    - 4. Curvst in CV steps
Export


Code Structure:
1. Main
2. DA00: Data Import, Dataframe creation, grouping
3. DA01: Plot & analysis of Voltage and Current to Time
4. DA02: Plot & analysis of Voltage to Capacity (Potential Profile)
5. DA03: Plot & analysis of Coulombic Efficiency
    6. DA04: Plot & analysis SOH over cycles
7. DA05: Analysis of Statistical Summary
8. DA06: Plot & analysis of dQ/dV to Voltage

== Part of DA ==
- Function code for Plot & analysis of SOH


Authors: Hans and Matthias

"""

import pandas as pd
import matplotlib.pyplot as plt

#-------------------------------SOH over cycles--------------------------------
# Plot SOH estimation along the cycles
 
def DA04_Function_SOH(df_cycle_grouped,rated_capacity,file_name,result_folder):
    SOH_data_combined = []
    
    cycles = df_cycle_grouped['Cycle ID'].unique()
    max_capacity_per_cycle = df_cycle_grouped['Capacity'].max()
    
    soh = (max_capacity_per_cycle / rated_capacity) * 100
    
    SOH_data = pd.DataFrame({
        'Cycle': cycles,
        'Capacity': max_capacity_per_cycle,
        'SOH': soh
    })    
    
    SOH_data_combined.append(SOH_data)
    
    plt.figure(figsize=(10,6))
    plt.plot(cycles, soh, marker='o')
    plt.xlabel('Cycle Number')
    plt.ylabel('State of Health (%)')
    plt.title(f'State of Health (SOH) Over Cycles - {file_name}')
    plt.grid(True)
    plt.savefig(f'{result_folder}/{file_name}/SoH Plot_{file_name}.png', dpi=300)
    plt.close()
    
    df_SOH = pd.concat(SOH_data_combined)
    df_SOH.to_csv(f'{result_folder}/{file_name}/df_SOH_{file_name}.csv', index=False)
    
    return 

def DA04_Function_SOH_Combined(combined_result_folder,rated_capacity,df_combined):
    # SOH_data_combined = []
    df_cycles = df_combined.groupby('Cycle ID')
    cycles = df_cycles['Cycle ID'].unique()
    max_capacity_per_cycle = df_cycles['Capacity'].max()
    
    soh = (max_capacity_per_cycle / rated_capacity) * 100
    
    # SOH_data = pd.DataFrame({
    #     'Cycle': cycles,
    #     'Capacity': max_capacity_per_cycle,
    #     'SOH': soh
    # })    
    
    # SOH_data_combined.append(SOH_data)
    
    plt.figure(figsize=(10,6))
    
    for code in ['B1T1', 'B2T1', 'B3T1', 'B4T1', 'N1T1', 'N2T1']:
        
        if code == df_cycles['Battery_code']:
            plt.plot(cycles, soh, marker='o')
    
    
    plt.xlabel('Cycle Number')
    plt.ylabel('State of Health (%)')
    plt.title('State of Health (SOH) - Combined')
    plt.grid(True)
    plt.savefig(f'{combined_result_folder}/SOH Plot_Combined.png', dpi=300)
    plt.close()
    
    # df_SOH = pd.concat(SOH_data_combined)
    # df_SOH.to_csv(f'{result_folder}/{file_name}/df_SOH_{file_name}.csv', index=False)
    
    return    
