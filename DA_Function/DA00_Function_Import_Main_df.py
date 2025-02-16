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
- Function code for Data Import, Dataframe creation, grouping


Authors: Hans and Matthias

"""

import pandas as pd
import os

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
    name_conversion_dict = {'Time(h:min:s.ms)': 'Time', 'Voltage(V)':'Voltage', 'Current(mA)': 'Current', 'Energy(mWh)': 'Energy', 'Capacity(mAh)': 'Capacity', 'dQ/dV(mAh/V)':'dQdV'}
    df_main = df_main.rename(columns=name_conversion_dict)

    # Convert the 'Realtime' column to pandas datetime format
    df_main['Realtime'] = pd.to_datetime(df_main['Realtime'], format='%m/%d/%Y %H:%M:%S')

    # Convert 'Time' to timedelta (duration) for cumulative addition
    df_main['Time'] = pd.to_timedelta(df_main['Time'].astype(str))
    
    # Sort data properly: First by 'Cycle ID', then 'Record ID', then 'Time'
    df_main = df_main.sort_values(by=['Cycle ID', 'Record ID', 'Time']).reset_index(drop=True)

    # Compute Time difference within each cycle
    df_main['Time_Diff'] = df_main.groupby('Cycle ID')['Time'].diff().fillna(pd.Timedelta(seconds=0))

    # Ensure no negative values (set negatives to 0)
    df_main['Time_Diff'] = df_main['Time_Diff'].apply(lambda x: max(x.total_seconds(), 0))  # Convert to milliseconds

    # Compute Cycle_Time as the cumulative sum of Time_Diff within each cycle
    df_main['Cycle_Time'] = df_main.groupby('Cycle ID')['Time_Diff'].cumsum() 
    
    df_main.insert(df_main.columns.get_loc("Capacity") + 1, "Power", df_main["Voltage"] * df_main["Current"])
    
    # pd.set_option('display.max_columns', None)  # Show all columns   
    # print('DataFrame df_main preview: ',df_main.head(5))
   
    return df_main
    
#----------------------------Grouping in Dataframe-----------------------------
def DA00_Function_df_Cycle_Grouping(df_main,result_folder,file_name):
    #Make result folder
    os.makedirs(f"{result_folder}/{file_name}", exist_ok=True)  
    print(f"Folder '{result_folder}/{file_name}' created!")
    
    # Dropping unnecessary columns
    df_cycle_grouped = df_main.drop(columns=['Time','Realtime','Time_Diff'])
    
    # Grouping dataframe by Cycle ID, cycle_id = the cycle numbers
    df_cycle_grouped = df_cycle_grouped.groupby('Cycle ID')
    cycle_id = df_cycle_grouped.groups.keys()
    print("The cycles imported from", file_name, "are:", cycle_id, "and pre-processed.")

    # pd.set_option('display.max_columns', None)  # Show all columns   
    print('DataFrame df_cycle_grouped preview: ')
    pd.set_option('display.max_columns', None)  # Show all columns 
    print(df_cycle_grouped.head(5))
    
    # df_cycle_grouped.to_csv(f'{result_folder}/{file_name}/df_cycle_grouped_{file_name}.csv', index=False)
    
    # Initialize an empty list to store data for each cycle
    df_VQ_grouped_list = []
    
    # Function to add CC_Chg to CV_Chg capacity (as initial capacity)
    def accumulate_capacity(df, start_capacity):
        df['Accumulated_Capacity'] = df['Capacity'] + start_capacity
        return df

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
    
    print('DataFrame df_VQ_grouped preview: ')
    print(df_VQ_grouped.head())
    
    return df_cycle_grouped,df_VQ_grouped