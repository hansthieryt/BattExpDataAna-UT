# -*- coding: utf-8 -*-
"""
Code for automated data preprocessing

Code Structure:
1. Main
2. DA00: Data Import, Dataframe creation, grouping
3. DA01: Plot & analysis of Voltage, Current, Power to Time
    4. DA02: Plot & analysis of Voltage to Capacity (Potential Profile)
5. DA03: Plot & analysis of Coulombic Efficiency
6. DA04: Plot & analysis SOH over cycles
7. DA05: Analysis of Statistical Summary
8. DA06: Plot & analysis of dQ/dV to Voltage

== Part of DA ==
- Function code for Plot & analysis of Voltage to Capacity (Potential Profile)


Authors: Hans and Matthias

"""
import numpy as np
import matplotlib.pyplot as plt
import re

#--------------------Plotting Voltage to Capacity (VvsCap)---------------------
def DA02_Function_VvsCap(df_VQ_grouped,file_name,result_folder,rated_capacity):  
    cycle_columns = [col for col in df_VQ_grouped.columns if re.match(r'Cycle_\d+_', col)]
    cycle_numbers = sorted({int(re.search(r'Cycle_(\d+)_', col).group(1)) for col in cycle_columns})
    
    #----------------------------Plot Every Cycles-----------------------------
    plt.figure(figsize=(14, 8))

    for idx, cycle_id in enumerate(cycle_numbers):

        # Plot Charge V-Q
        if f'Cycle_{cycle_id}_VChg' in df_VQ_grouped and f'Cycle_{cycle_id}_CapChg' in df_VQ_grouped:
            plt.plot(df_VQ_grouped[f'Cycle_{cycle_id}_CapChg'], 
                     df_VQ_grouped[f'Cycle_{cycle_id}_VChg'], 
                     label=f'Cycle {cycle_id} Charge')

        # Plot Discharge V-Q
        if f'Cycle_{cycle_id}_VDChg' in df_VQ_grouped and f'Cycle_{cycle_id}_CapDChg' in df_VQ_grouped:
            plt.plot(df_VQ_grouped[f'Cycle_{cycle_id}_CapDChg'],
            df_VQ_grouped[f'Cycle_{cycle_id}_VDChg'], linestyle='--', 
            label=f'Cycle {cycle_id} Discharge')
        
        plt.xlabel('Capacity (mAh)')
        plt.ylabel('Voltage (V)')
        plt.xlim(0, rated_capacity)
        plt.title(f'Voltage vs Capacity for Cycle {cycle_id} - {file_name}')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'{result_folder}/{file_name}/V-Q_Cycle_{cycle_id}_{file_name}.png')
        plt.show()
        
    #-----------------------------Plot All Cycles------------------------------
    # Plot V-Q for all cycles in one graph with different colors
    plt.figure(figsize=(14, 8))

    # Define a color map
    colors = plt.cm.jet(np.linspace(0, 1, len(cycle_numbers)))

    for idx, cycle_id in enumerate(cycle_numbers):
        color = colors[idx]

        # Plot Charge V-Q
        if f'Cycle_{cycle_id}_VChg' in df_VQ_grouped and f'Cycle_{cycle_id}_CapChg' in df_VQ_grouped:
            plt.plot(df_VQ_grouped[f'Cycle_{cycle_id}_CapChg'], 
                     df_VQ_grouped[f'Cycle_{cycle_id}_VChg'], 
                     label=f'Cycle {cycle_id} Charge', 
                     color=color)

        # Plot Discharge V-Q
        if f'Cycle_{cycle_id}_VDChg' in df_VQ_grouped and f'Cycle_{cycle_id}_CapDChg' in df_VQ_grouped:
            plt.plot(df_VQ_grouped[f'Cycle_{cycle_id}_CapDChg'],
            df_VQ_grouped[f'Cycle_{cycle_id}_VDChg'], linestyle='--', 
            label=f'Cycle {cycle_id} Discharge', 
            color=color)

    plt.xlabel('Capacity (mAh)')
    plt.ylabel('Voltage (V)')
    plt.xlim(0, rated_capacity)
    plt.title(f'Voltage vs Capacity for All Cycles - {file_name}')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'{result_folder}/{file_name}/V-Q_All_Cycles_{file_name}.png')   
    plt.show()
    
    return