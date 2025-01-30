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
- Function code for Data Import, Dataframe creation, grouping


Authors: Hans and Matthias

"""

import pandas as pd
import os
import functools

#---------------------------------Data Import----------------------------------

def DA00_Function_Import(data_folder,file_name,rated_capacity):
    # Import multiple Neware txt files, loop until all files found, remove 
    # tab and header using skiprows, remove index and "." as decimal
    df_main = []
    i = 0  # Start counter

    while True:
        # Correctly construct the file path
        file_path = f"{data_folder}/{file_name}/{file_name}__{i}.txt"
        
        # Check if the file exists
        if os.path.exists(file_path):
            # Read the file
            dataraw = pd.read_csv(file_path, sep='\t', skiprows=0, index_col=False, decimal='.')
            df_main.append(dataraw)  # Append dataframe to the list
            i += 1  # Increment counter for the next file
        else:
            print(f"File {file_path} not found. Stopping.")
            break  # Exit loop when the file is not found

    # Create one main dataframe by combining the loop import files
    df_main = pd.concat(df_main, ignore_index=True)

    # change column names
    name_conversion_dict = {'Time(h:min:s.ms)': 'Time', 'Voltage(V)':'Voltage', 'Current(mA)': 'Current', 'Capacity(mAh)': 'Capacity', 'dQ/dV(mAh/V)':'dQdV'}
    df_main = df_main.rename(columns=name_conversion_dict)

    # Convert the 'Realtime' column to pandas datetime format
    df_main['Realtime'] = pd.to_datetime(df_main['Realtime'], format='%m/%d/%Y %H:%M:%S')

    # Convert 'Time' to timedelta (duration) for cumulative addition
    df_main['Time'] = pd.to_timedelta(df_main['Time'].astype(str))
    # df_main['Time'] = pd.to_datetime(df_main['Time'], format='%H:%M:%S.%f')
    
    # Accumulate 'Time' on every cycle to 'Cycle_Time'
    df_main['Cycle_Time'] = df_main.groupby('Cycle ID')['Time'].cumsum()
    
    df_main['SOH'] = df_main['Capacity']/rated_capacity
    
    return df_main
    
#----------------------------Grouping in Dataframe-----------------------------
def DA00_Function_df_Cycle_Grouping(df_main,result_folder,file_name):
    #Make result folder
    os.makedirs(f"{result_folder}/{file_name}", exist_ok=True)  # exist_ok=True avoids errors if the folder already exists
    print(f"Folder '{result_folder}/{file_name}' created!")
    
    # Function to add CC_Chg to CV_Chg capacity (as initial capacity)
    def accumulate_capacity(df, start_capacity):
        df['Accumulated_Capacity'] = df['Capacity'] + start_capacity
        return df

    # Grouping dataframe by Cycle ID, cycle_id = the cycle numbers
    df_cycle_grouped = df_main.groupby('Cycle ID')
    cycle_id = df_cycle_grouped.groups.keys()
    #print(cycle_id)
    
    # Initialize an empty list to store data for each cycle
    df_VQ_grouped_list = []

    # Iterate over each cycle
    for cycle_id, df_cyc in df_cycle_grouped:
        # Group by Step Name within each cycle
        df_step_grouped = df_cyc.groupby('Step Name')
        step_group_name = df_step_grouped.groups.keys()
       
        if 'CC_Chg' and 'CV_Chg' and 'CC_DChg' in step_group_name:
            
            # Extract relevant steps
            cc_chg = df_step_grouped.get_group('CC_Chg') if 'CC_Chg' in df_step_grouped.groups else pd.DataFrame()
            cv_chg = df_step_grouped.get_group('CV_Chg') if 'CV_Chg' in df_step_grouped.groups else pd.DataFrame()
            cc_dchg = df_step_grouped.get_group('CC_DChg') if 'CC_DChg' in df_step_grouped.groups else pd.DataFrame()
            
            # Voltage and Capacity for Charge steps
            vchg = pd.concat([cc_chg['Voltage'], cv_chg['Voltage']]) if not cv_chg.empty else cc_chg['Voltage']
            dqdvchg = pd.concat([cc_chg['dQdV'], cv_chg['dQdV']]) if not cv_chg.empty else cc_chg['dQdV']
            cchg_start = cc_chg['Capacity'].iloc[-1] if not cc_chg.empty else 0
            cchg = pd.concat([cc_chg['Capacity'], 
                              accumulate_capacity(cv_chg, cchg_start)['Accumulated_Capacity']]) if not cv_chg.empty else   cc_chg['Capacity']

            # Voltage and Capacity for Discharge steps
            vdchg = cc_dchg['Voltage'] if not cc_dchg.empty else pd.Series()
            cdchg = cc_dchg['Capacity'] if not cc_dchg.empty else pd.Series()
            dqdvdchg = cc_dchg['dQdV'] if not cc_dchg.empty else pd.Series()
        
            # Combine into a DataFrame for V-Q
            df_VQ = pd.DataFrame({
                f'Cycle_{cycle_id}_VChg': vchg.reset_index(drop=True),
                f'Cycle_{cycle_id}_CapChg': cchg.reset_index(drop=True),
                f'Cycle_{cycle_id}_dQdVChg': dqdvchg.reset_index(drop=True),
                f'Cycle_{cycle_id}_VDChg': vdchg.reset_index(drop=True),
                f'Cycle_{cycle_id}_CapDChg': cdchg.reset_index(drop=True),
                f'Cycle_{cycle_id}_dQdVDChg': dqdvdchg.reset_index(drop=True),
                })
               
            # Combine all the cycles
            df_VQ_grouped_list.append(df_VQ)
        
        else:
            continue
        
    # Concatenate all cycle data horizontally and save the result
    df_VQ_grouped = pd.concat(df_VQ_grouped_list, axis=1)
    df_VQ_grouped.to_csv(f'{result_folder}/{file_name}/df_VQ_grouped_{file_name}.csv', index=False)
    
    df_main_ML = df_main.drop(columns=['Realtime', 'dQdV', 'Time', 'Energy(mWh)', 'Step Name'])
    df_main_ML = df_main_ML[df_main_ML['Record ID'] % 6 == 0]
    # downsampled_df = df[df['RecordID'] % 6 == 0]
    df_main_ML.to_csv(f'{result_folder}/{file_name}/df_main_ML_{file_name}.csv', index=False)
    
    return df_cycle_grouped,df_VQ_grouped    

#------------------------Battery Data Combined Import--------------------------
def DA00_Function_Import_Combined(combined_data_folder, combined_file_name):
    print("\nPerforming Import Data...")
    # @staticmethod
    def DA00_Function_Import_Load(raw_path, gaussian_path, overvoltage_path):
        # Load raw experimental data
        raw_data = pd.read_csv(raw_path)
        
        # Load Gaussian fit results
        gaussian_data = pd.read_csv(gaussian_path)
        
        # Load overvoltage data
        overvoltage_data = pd.read_csv(overvoltage_path)
        
        # Merge datasets on 'Cycle ID'

        combined_data = raw_data.merge(gaussian_data, on="Cycle ID", how='left').merge(overvoltage_data, on="Cycle ID", how='left')
        
        # Drop duplicates and clean data
        combined_data = combined_data.drop_duplicates()
        combined_data = combined_data.dropna()
        
        # Feature Engineering: Adding rate of change for key indicators
        combined_data['Delta_Capacity'] = combined_data['Capacity'].diff()
        combined_data['Delta_Overvoltage'] = combined_data['Overvoltage'].diff()
        # combined_data['SOH'] = combined_data['Capacity'] / combined_data['Capacity'].iloc[0] * 100  # Normalize SOH
        combined_data.dropna(inplace=True)
    
        return combined_data
    
    
    # Aggregate data from multiple batteries
    df_combined_data = []
    for code in combined_file_name:
        raw_path = os.path.join(combined_data_folder, f"df_main_ML_{code}.csv")   
        gaussian_path = os.path.join(combined_data_folder, f"gaussian_fits_{code}.csv")    
        overvoltage_path = os.path.join(combined_data_folder, f"overvoltage_{code}.csv")  
        battery_data = DA00_Function_Import_Load(raw_path, gaussian_path, overvoltage_path)
        battery_data['Battery_code'] = code  # Add a column for battery identification
        df_combined_data.append(battery_data)
        print(f"The data from {code} was completely imported")
        
    # Combine all battery data
    df_combined = pd.concat(df_combined_data, ignore_index=True)
    # Drop the index directly
    df_combined.index = range(len(df_combined))
    print("Aggregated Data:\n", df_combined.head())
    
    return df_combined