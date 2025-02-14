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
- Function code for main script


Authors: Hans and Matthias

"""

from DA_Function.DA00_Function_Import_Main_df import (DA00_Function_Import, 
                                                      DA00_Function_df_Cycle_Grouping)
from DA_Function.DA01_Function_VnIvsTime import (DA01_Function_VnIvsTime,
                                                 DA01_Function_Power)
from DA_Function.DA02_Function_VvsCap import (DA02_Function_VvsCap)
from DA_Function.DA03_Function_Coulombic_Efficiency import (DA03_Function_Coulombic_Efficiency)
from DA_Function.DA04_Function_SOH import (DA04_Function_SOH)
from DA_Function.DA06_Function_dQdV import (DA06_Function_dQdV)

#----------------------------------Data input----------------------------------
data_folder = 'DA_Data'                                                        # <=== Insert folder of the data file(s)
result_folder = 'DA_Result'                                                    # <=== Insert folder for result
file_names = ['N1T1', 'N2T2']                                                  # <=== Insert file name
rated_capacity = 2100                                                          # <=== Insert rated capacity of battery


for file_name in file_names:
    print(f"Processing file: {file_name}")
#---------------------------------Data Import----------------------------------
    df_main = DA00_Function_Import(data_folder,file_name,rated_capacity)

# ----------------------------Data Grouping by Cycle----------------------------
    # Grouping based on cycle, combining CC Chg & CV Chg into one Chg data
    df_cycle_grouped,df_VQ_grouped = DA00_Function_df_Cycle_Grouping(df_main,
                                                                   result_folder,
                                                                   file_name)

#-------------------------Direct Plotting: VnIvsTime---------------------------
    DA01_Function_VnIvsTime(result_folder,file_name,df_cycle_grouped)     

#---------------------------Direct Plotting: Power-----------------------------
    DA01_Function_Power(result_folder,file_name,df_cycle_grouped)           

#------------------Direct Plotting: VvsCap (Potential Profile)-----------------
    DA02_Function_VvsCap(df_VQ_grouped,file_name,result_folder,rated_capacity)

#-----------------Calculation & Plotting: Coulombic Efficiency-----------------
    df_ce = DA03_Function_Coulombic_Efficiency(df_VQ_grouped,file_name,result_folder)  

#----------------Calculation & Plotting: State of Health (SOH)-----------------
    df_SOH = DA04_Function_SOH(df_VQ_grouped,rated_capacity,file_name,result_folder)

#------------------------------------dQ/dV-------------------------------------
    # Interpolation setup
    interpolation_points = 300                                               # <=== Insert data point numbers for interpolation

    # Smoothing setup             [Setup for Savitzky–Golay filter smoothing]
    window_length = 5                                                        # <=== Insert the window length as the smoothing properties
    polyorder = 1                                                            # <=== Insert the polyorder as the smoothing properties

    # Finding peaks             [Setup parameter for finding peaks on dQ/dV-V plot]
    min_prominence = 50                       #[Do not change if not necessary] <=== Insert the minimum prominence value
    min_height = 50                           #[Do not change if not necessary] <=== Insert the minimum height value
    max_prominence = 10000                    #[Do not change if not necessary] <=== Insert the maximum prominence value
    max_height = 10000                        #[Do not change if not necessary] <=== Insert the maximum height value
    prominence_step = 10                      #[Do not change if not necessary] <=== Insert the prominence value per iteration 
    height_step = 10                          #[Do not change if not necessary] <=== Insert the height value per iteration            
    max_iterations = 1000                     #[Do not change if not necessary] <=== Insert the maximum iteration number
    max_peaks = 2                             #[Do not change if not necessary] <=== Insert the maximum expected peaks
    
    window_size = 3                               #[Do not change if not necessary] <=== Insert the window size for gaussian fitting       

    # Selecting parameters shown on plot
    show_on_plot = [                                                           # <=== Insert the parameters to be shown on the plot: 
                    # 'data'                                                    #      - 'data':from neware;
                    'ori',                                                     #      - 'ori':pure calculation; 
                    'int',                                                     #      - 'int':interpolated data; 
                    'smooth',                                                  #      - 'smooth':interpolation,then filtering/smoothing  
                                                                               #         with Savitzky-Golay filter; 
                    'peaks-fitting'                                            #      - 'peaks-fitting':notate peaks and plot Gaussian 
                                                                               #         fitting curve on the plot             
                    ]
    
    df_dqdv,df_peaks,df_fitting = DA06_Function_dQdV(file_name,df_VQ_grouped,
                                                     show_on_plot,
                                                     interpolation_points,
                                                     window_length,polyorder,
                                                     window_size,min_prominence,
                                                     min_height,max_prominence,
                                                     max_height,prominence_step,
                                                     height_step,max_iterations,
                                                     max_peaks,result_folder)