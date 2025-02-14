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
- Function code for Plot & analysis of Voltage and Current to Time


Authors: Hans and Matthias

"""
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

#-----------------------------------VnIvsTime----------------------------------

def DA01_Function_VnIvsTime(result_folder,file_name,df_cycle_grouped):
    cycle_id = df_cycle_grouped.groups.keys()
    
    i = 0
    for i in cycle_id:    
        cycle_data = df_cycle_grouped.get_group(i)
        fig, host = plt.subplots()
        par1 = host.twinx()

        # Insert the data for overview plot
        p1, = host.plot(cycle_data['Cycle_Time'], cycle_data['Voltage'], "b-")
        p2, = par1.plot(cycle_data['Cycle_Time'], cycle_data['Current'], "r-")
        host.set_ylabel('Voltage (V)')
        par1.set_ylabel('Current (mA)')
        plt.title(f'Voltage and Current vs. Time - {file_name} - Cycle{i}')
        plt.savefig(f'{result_folder}/{file_name}/VnCvsTime_{file_name}_Cycle{i}.png', dpi=300, bbox_inches='tight')
        i += 1
        
    #-----------------------------------All cycles-----------------------------    
    fig, host = plt.subplots()
    par1 = host.twinx()  # Create the second y-axis

    # Get a colormap with enough colors for all cycles
    colors = cm.rainbow(np.linspace(0, 1, len(cycle_id)))

    for i, cycle in enumerate(cycle_id):
        cycle_data = df_cycle_grouped.get_group(cycle)
        
        # Plot each cycle with a different color
        p1, = host.plot(cycle_data['Cycle_Time'], cycle_data['Voltage'], color=colors[i])#, label=f'Cycle {cycle} Voltage')
        p2, = par1.plot(cycle_data['Cycle_Time'], cycle_data['Current'], color=colors[i], linestyle='--')#, label=f'Cycle {cycle} Current')
    
    # Set labels and titles
    host.set_xlabel('Cycle Time (s)')
    host.set_ylabel('Voltage (V)')
    par1.set_ylabel('Current (mA)')
    plt.title(f'Voltage and Current vs. Cycle Time - All Cycles - {file_name}')

    # Create a legend that combines both axes
    host.legend(loc='upper left')
    par1.legend(loc='upper right')

    # Save the combined plot
    plt.savefig(f"{result_folder}/{file_name}/VnCvsTime_{file_name}_AllCycles.png", dpi=300, bbox_inches='tight')
    plt.show()

    return

#-----------------------------------Power----------------------------------

def DA01_Function_Power(result_folder,file_name,df_cycle_grouped):
    cycle_id = df_cycle_grouped.groups.keys()
    
    plt.figure(figsize=(10, 6))
    i = 0
    for i in cycle_id:    
        cycle_data = df_cycle_grouped.get_group(i)

        # Insert the data for overview plot
        plt.plot(cycle_data['Cycle_Time'], cycle_data['Voltage']*cycle_data['Current'])
        plt.ylabel('Voltage (V)')
        plt.ylabel('Power (kW)')
        plt.title(f'Power vs. Time - {file_name} - Cycle{i}')
        plt.savefig(f'{result_folder}/{file_name}/PvsTime_{file_name}_Cycle{i}.png', dpi=300, bbox_inches='tight')
        plt.show()
        i += 1
        
    #-----------------------------------All cycles-----------------------------    
    # Get a colormap with enough colors for all cycles
    colors = cm.rainbow(np.linspace(0, 1, len(cycle_id)))

    for i, cycle in enumerate(cycle_id):
        cycle_data = df_cycle_grouped.get_group(cycle)
        
        # Plot each cycle with a different color
        plt.plot(cycle_data['Cycle_Time'], cycle_data['Voltage']*cycle_data['Current'], color=colors[i])
    
    # Set labels and titles
    plt.xlabel('Cycle Time (s)')
    plt.ylabel('Power (kW)')
    plt.title(f'Power vs. Cycle Time - All Cycles - {file_name}')
    plt.savefig(f"{result_folder}/{file_name}/PvsTime_{file_name}_AllCycles.png", dpi=300, bbox_inches='tight')
    plt.show()

    return