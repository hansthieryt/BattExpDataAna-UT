# -*- coding: utf-8 -*-
"""
Code for automated data preprocessing

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

import re
import pandas as pd
import matplotlib.pyplot as plt

#--------------------Processing & Plotting SOH over cycles---------------------
def DA04_Function_SOH(df_VQ_grouped,rated_capacity,file_name,result_folder):
    SOH_data = []
    
    # Extract unique cycle numbers from the column names
    cycle_columns = [col for col in df_VQ_grouped.columns if re.match(r'Cycle_\d+_', col)]
    cycle_numbers = sorted({int(re.search(r'Cycle_(\d+)_', col).group(1)) for col in cycle_columns})

    for cycle_id in cycle_numbers:
        cchg = df_VQ_grouped[f'Cycle_{cycle_id}_CapChg'].dropna()
        cdchg = df_VQ_grouped[f'Cycle_{cycle_id}_CapDChg'].dropna()
        
        # Calculate SOH
        if cchg.max() > cdchg.max():
            max_capacity_per_cycle = cchg.max()
        else:
            max_capacity_per_cycle = cdchg.max()
            
        soh = (max_capacity_per_cycle / rated_capacity) * 100
        
        # Combine into a DataFrame
        SOH_data.append({
            'Cycle_ID': cycle_id,
            'Maximum_Capacity': max_capacity_per_cycle,
            'SOH': soh
            })
    
    df_SOH = pd.DataFrame(SOH_data)
    df_SOH.to_csv(f'{result_folder}/{file_name}/df_SOH_{file_name}.csv', index=False)
    pd.set_option('display.max_columns', None)  # Show all columns   
    print('DataFrame df_SOH preview: ')
    print(df_SOH.head(5))
    
    plt.figure(figsize=(10,6))
    plt.plot(df_SOH['Cycle_ID'], df_SOH['SOH'], marker='o')
    plt.xlabel('Cycle Number')
    plt.ylabel('State of Health (%)')
    plt.ylim((df_SOH['SOH'].min()*0.97), (df_SOH['SOH'].max()*1.03))
    plt.title(f'State of Health (SOH) Over Cycles - {file_name}')
    plt.grid(True)
    plt.savefig(f'{result_folder}/{file_name}/SOH Plot_{file_name}.png', dpi=300)
    plt.show()
        
    return  df_SOH