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
- Function code for main script


Authors: Hans and Matthias

"""

# import numpy as np
# import pandas as pd
# import seaborn as sns
# import os
# import matplotlib.pyplot as plt
# from scipy.signal import savgol_filter
# from scipy.interpolate import interp1d

from DA_Function.DA00_Function_Import_Main_df import (DA00_Function_Import, 
                                                      DA00_Function_df_Cycle_Grouping, 
                                                      DA00_Function_Import_Combined)
from DA_Function.DA01_Function_VnIvsTime import (DA01_Function_VnIvsTime, 
                                                 DA01_Function_VnIvsTime_Combined, 
                                                 DA01_Function_Power)
from DA_Function.DA02_Function_VvsCap import (DA02_Function_VvsCap, DA02_Function_VvsCap_Combined)
from DA_Function.DA03_Function_Coulombic_Efficiency import DA03_Function_Coulombic_Efficiency
from DA_Function.DA04_Function_SOH import (DA04_Function_SOH, DA04_Function_SOH_Combined)
from DA_Function.DA05_Function_Statistical_Model import DA05_Function_Statistical
from DA_Function.DA06_Function_dQdV import (DA06_Function_dQdV, DA06_Function_dQdV_Combined)

#----------------------------------Data input----------------------------------
data_folder = 'DA_Data'                                                        # <=== Insert folder of the data file(s)
result_folder = 'DA_Result'                                                    # <=== Insert folder for result
file_name = 'M2C3'                                                             # <=== Insert file name
rated_capacity = 2100                                                          # <=== Insert rated capacity of battery
df_main = DA00_Function_Import(data_folder,file_name,rated_capacity)

#----------------------------Data Grouping by Cycle----------------------------
df_cycle_grouped,df_VQ_grouped = DA00_Function_df_Cycle_Grouping(df_main,
                                                                  result_folder,
                                                                  file_name)

#----------------------------------VnIvsTime-----------------------------------
DA01_Function_VnIvsTime(result_folder,file_name,df_cycle_grouped)          

#------------------------------------Power-------------------------------------
DA01_Function_Power(result_folder,file_name,df_cycle_grouped)          

#--------------------------VvsCap (Potential Profile)--------------------------
DA02_Function_VvsCap(df_VQ_grouped,file_name,result_folder)

#-----------------------------Coulombic Efficiency-----------------------------
# Grouping based on cycle, combining CC Chg & CV Chg into one Chg data
DA03_Function_Coulombic_Efficiency(df_VQ_grouped,file_name,result_folder)  

#-------------------------------SOH over cycles--------------------------------
DA04_Function_SOH(df_cycle_grouped,rated_capacity,file_name,result_folder)

#-----------------------------Statistical Summary------------------------------
DA05_Function_Statistical(df_main, df_cycle_grouped, file_name, result_folder)

#------------------------------------dQ/dV-------------------------------------
# Interpolation setup
interpolation_points = 300                                                     # <=== Insert data point numbers for interpolation

# Smoothing setup                   [Setup for Savitzky–Golay filter smoothing]
window_length = 5                                                              # <=== Insert the window length as the smoothing properties
polyorder = 1                                                                  # <=== Insert the polyorder as the smoothing properties

# Finding peaks             [Setup parameter for finding peaks on dQ/dV-V plot]
min_prominence = 50                           #[Do not change if not necessary] <=== Insert the minimum prominence value
min_height = 50                               #[Do not change if not necessary] <=== Insert the minimum height value
max_prominence = 10000                        #[Do not change if not necessary] <=== Insert the maximum prominence value
max_height = 10000                            #[Do not change if not necessary] <=== Insert the maximum height value
prominence_step = 10                          #[Do not change if not necessary] <=== Insert the prominence value per iteration 
height_step = 10                              #[Do not change if not necessary] <=== Insert the height value per iteration            
max_iterations = 1000                         #[Do not change if not necessary] <=== Insert the maximum iteration number
max_peaks = 2                                 #[Do not change if not necessary] <=== Insert the maximum expected peaks

window_size = 3                               #[Do not change if not necessary] <=== Insert the window size for gaussian fitting       

# Selecting parameters shown on plot
show_on_plot = [                                                               # <=== Insert the parameters to be shown on the plot: 
              #'data'                                                          #      - 'data':from neware;
              #'ori',                                                          #      - 'ori':pure calculation; 
              #'int',                                                          #      - 'int':interpolated data; 
              'smooth',                                                        #      - 'smooth':interpolation,then filtering/smoothing  
                                                                               #         with Savitzky-Golay filter; 
              'peaks-fitting'                                                  #      - 'peaks-fitting':notate peaks and plot Gaussian 
                                                                               #         fitting curve on the plot             
                ]
    
DA06_Function_dQdV(file_name,df_cycle_grouped,df_VQ_grouped,show_on_plot,
                    interpolation_points,window_length,polyorder,window_size,
                    min_prominence,min_height,max_prominence,max_height,
                    prominence_step,height_step,max_iterations,max_peaks,
                    result_folder)

#-------------------------Combined Battery Plotting----------------------------

# #----------------------------Data Grouping by Cycle----------------------------
# combined_data_folder = 'DA_Data/Combined'
# combined_result_folder = 'DA_Result/Combined'
# combined_file_name = ['B1T1', 'B2T1', 'B3T1', 'B4T1', 'N1T1', 'N2T1']
# rated_capacity = 2100                                                          # <=== Insert rated capacity of battery
# df_combined = DA00_Function_Import_Combined(combined_data_folder, combined_file_name)

#----------------------------------VnIvsTime-----------------------------------
# DA01_Function_VnIvsTime_Combined(combined_result_folder,df_combined)                  

#--------------------------VvsCap (Potential Profile)--------------------------
# DA02_Function_VvsCap_Combined(combined_result_folder,df_combined)

#-------------------------------SOH over cycles--------------------------------
# DA04_Function_SOH_Combined(combined_result_folder,rated_capacity,df_combined)

# #------------------------------------dQ/dV-------------------------------------
# # Interpolation setup
# interpolation_points = 300                                                     # <=== Insert data point numbers for interpolation

# # Smoothing setup                   [Setup for Savitzky–Golay filter smoothing]
# window_length = 5                                                              # <=== Insert the window length as the smoothing properties
# polyorder = 1                                                                  # <=== Insert the polyorder as the smoothing properties
   
# DA06_Function_dQdV_Combined(combined_result_folder,df_combined,
#                             interpolation_points,window_length,polyorder)