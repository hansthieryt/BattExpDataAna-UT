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
- Function code for Plot & analysis of Coulombic Efficiency (CE)


Authors: Hans and Matthias

"""

import pandas as pd
import matplotlib.pyplot as plt
import re

#---------------------Processing & Plotting CE over cycles---------------------
def DA03_Function_Coulombic_Efficiency(df_VQ_grouped,file_name,result_folder):   
    ce_cycle = []
    
    # Extract unique cycle numbers from the column names
    cycle_columns = [col for col in df_VQ_grouped.columns if re.match(r'Cycle_\d+_', col)]
    cycle_numbers = sorted({int(re.search(r'Cycle_(\d+)_', col).group(1)) for col in cycle_columns})

    for cycle_id in cycle_numbers:      
        cchg = df_VQ_grouped[f'Cycle_{cycle_id}_CapChg'].dropna()
        cdchg = df_VQ_grouped[f'Cycle_{cycle_id}_CapDChg'].dropna()
        
        # Calculate Coulombic Efficiency (CE)
        total_CapChg = cchg.iloc[-1] if not cchg.empty else 0
        total_CapDChg = cdchg.iloc[-1] if not cdchg.empty else 0
        ce = (total_CapDChg / total_CapChg) * 100 if total_CapChg > 0 else 0
        if ce > 100:
            continue
        
        # Combine into a DataFrame
        ce_cycle.append({
            'Cycle_ID': cycle_id,
            'Discharge_Capacity': total_CapDChg,
            'Charge_Capacity': total_CapChg,
            'Coulombic_Efficiency': ce,
            })
               
    # Create a DataFrame for Coulombic Efficiencies and save the result
    df_ce = pd.DataFrame(ce_cycle)
    df_ce.to_csv(f'{result_folder}/{file_name}/df_CE_{file_name}.csv', index=False)
    pd.set_option('display.max_columns', None)  # Show all columns   
    print('DataFrame df_ce preview: ')
    print(df_ce.head(5))
    
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Cycle ID')
    ax1.set_ylabel('Coulombic Efficiency (%)', color=color)
    ax1.plot(df_ce['Cycle_ID'], df_ce['Coulombic_Efficiency'], color=color, 
             marker='o', label='Coulombic Efficiency')
    ax1.tick_params(axis='y', labelcolor=color)
    plt.ylim((df_ce['Coulombic_Efficiency'].min()*0.97), (df_ce['Coulombic_Efficiency'].max()*1.03))

    ax2 = ax1.twinx()
    ax2.set_ylabel('Capacity (mAh)', color=color)
    ax2.plot(df_ce['Cycle_ID'], df_ce['Charge_Capacity'], color='tab:green', 
             marker='x', linestyle='--', label='Charge Capacity')
    ax2.plot(df_ce['Cycle_ID'], df_ce['Discharge_Capacity'], color='tab:red', 
             marker='x', linestyle='--', label='Discharge Capacity')
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    fig.legend(loc='upper left', bbox_to_anchor=(0.1,0.9))
    plt.title(f'Coulombic Efficiency and Capacity vs Cycle - {file_name}')
    plt.grid(True)
    plt.savefig(f'{result_folder}/{file_name}/CE-cycles_{file_name}.png', dpi=300)
    plt.show()
    
    return df_ce
    
