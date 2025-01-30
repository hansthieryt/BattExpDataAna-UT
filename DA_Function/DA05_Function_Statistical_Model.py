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
- Function code for processing the statistical summary of the raw data


Authors: Hans and Matthias

"""

import pandas as pd
import os

#---------------------------------Data Import----------------------------------
def DA05_Function_Statistical(df_main, df_cycle_grouped, file_name, result_folder):
    def generate_statistical_summary(df_cycle_grouped, result_folder, file_name):
        """
        Generates a statistical summary for each cycle and exports it to a CSV file.
    
        Parameters:
        - df_cycle_grouped (pd.DataFrame): Data grouped by 'Cycle ID' from DA01_Function_df_Cycle_Grouping.
        - output_path (str): Directory path to save the CSV file.
        """
        summary_list = []
    
        for cycle_id, df_cyc in df_cycle_grouped:
            # Calculate summary statistics for Voltage, Current, Capacity, dQdV
            stats = df_cyc[['Voltage', 'Current', 'Capacity', 'dQdV']].describe().T
            stats['Cycle_ID'] = cycle_id  # Add cycle ID for reference
            summary_list.append(stats)
    
        # Concatenate all cycle summaries and save to CSV
        summary_df = pd.concat(summary_list, axis=1).reset_index()
        summary_df.to_csv(f'{result_folder}/{file_name}/{file_name}_cycle_statistical_summary.csv', index=False)
        print(f"Cycle-level statistical summary saved to {result_folder}/{file_name}/{file_name}_cycle_statistical_summary.csv")

# Function to calculate voltage, current, and time at specific SOC levels
    def soc_level_summary(df_main, soc_levels, result_folder, file_name):
        """
        Extracts voltage, current, and time at specified SOC levels and exports to CSV.
    
        Parameters:
        - df_main (pd.DataFrame): DataFrame with main data, including 'SOC' and cycle data.
        - soc_levels (list): List of SOC levels to capture (e.g., [0, 25, 50, 75, 100]).
        - output_path (str): Directory path to save the CSV file.
        """
        soc_data = []

        for cycle_id, cycle_data in df_main.groupby('Cycle ID'):
            for soc_level in soc_levels:
                soc_match = cycle_data.loc[cycle_data['SOH'].sub(soc_level).abs().idxmin()]
                soc_entry = {
                    'Cycle_ID': cycle_id,
                    'SOC_Level': soc_level,
                    'Voltage': soc_match['Voltage'],
                    'Current': soc_match['Current'],
                    'Time': soc_match['Time']
                    }
                soc_data.append(soc_entry)
    
        # Convert SOC data to DataFrame and save to CSV
        soc_summary_df = pd.DataFrame(soc_data)
        soc_summary_df.to_csv(f'{result_folder}/{file_name}/{file_name}_soc_level_summary.csv', index=False)
        print(f"SOC-level summary saved to {result_folder}/{file_name}/{file_name}_soc_level_summary.csv")

    # Example usage assuming processed data from DA01_Function_df_Cycle_Grouping
    # output_path = "results_folder"  # Specify the directory to save files
    soc_levels = [0, 25, 50, 75, 100]  # Define SOC levels of interest

    # Generate statistical summary for each cycle
    generate_statistical_summary(df_cycle_grouped, result_folder, file_name)

    # Generate SOC-level summary
    soc_level_summary(df_main, soc_levels, result_folder, file_name)
