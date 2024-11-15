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
2. Data Import, Dataframe creation, grouping
3. Plot & analysis of Voltage and Current to Time
4. Plot & analysis of Coulombic Efficiency
5. Plot & analysis of Voltage to Capacity (Potential Profile)
6. Plot & analysis of dQ/dV to Voltage
7. Plot & analysis SOH over cycles
8. Analysis of correlation (with heatmap)
9. Machine Learning Prediction

== Part of DA01 ==
- Function code for main script


Authors: Hans and Matthias

"""

# import numpy as np
# import pandas as pd
# # import seaborn as sns
# import os
# import matplotlib.pyplot as plt
# from scipy.signal import savgol_filter
# from scipy.interpolate import interp1d

from DA01_Function.DA01_Function_Import_Main_df import DA01_Function_Import
from DA01_Function.DA01_Function_Import_Main_df import DA01_Function_df_Cycle_Grouping
from DA01_Function.DA01_Function_VnIvsTime import DA01_Function_VnIvsTime
from DA01_Function.DA01_Function_Coulombic_Efficiency import DA01_Function_Coulombic_Efficiency
from DA01_Function.DA01_Function_VvsCap import DA01_Function_VvsCap
from DA01_Function.DA01_Function_dQdV import DA01_Function_dQdV
from DA01_Function.DA01_Function_SOH import DA01_Function_SOH
# from DA01_Function.DA01_Function_Correlation import DA01_Function_Correlation
from DA01_Function.DA01_Function_SOH_Prediction import DA01_Function_SOH_Prediction_Linear_Regression
from DA01_Function.DA01_Function_Statistical_Model import DA01_Function_Statistical

#----------------------------------Data input----------------------------------
data_folder = 'DA01_Data'                                                      # <=== Insert folder of the data file(s)
result_folder = 'DA01_Result'                                                  # <=== Insert folder for result
file_name = 'N2T1'                                                             # <=== Insert file name
rated_capacity = 2100                                                          # <=== Insert rated capacity of battery
df_main = DA01_Function_Import(data_folder,file_name,rated_capacity)

#----------------------------Data Grouping by Cycle----------------------------
df_cycle_grouped,df_VQ_grouped = DA01_Function_df_Cycle_Grouping(df_main,
                                                                 result_folder,
                                                                 file_name)

#----------------------------------VnIvsTime-----------------------------------
DA01_Function_VnIvsTime(result_folder,file_name,df_cycle_grouped)

#-----------------------------Coulombic Efficiency-----------------------------
# Grouping based on cycle, combining CC Chg & CV Chg into one Chg data
DA01_Function_Coulombic_Efficiency(df_VQ_grouped,file_name,result_folder)                    

#--------------------------VvsCap (Potential Profile)--------------------------
DA01_Function_VvsCap(df_VQ_grouped,file_name,result_folder)

#------------------------------------dQ/dV-------------------------------------
# Interpolation setup
interpolation_points = 300                                                     # <=== Insert data point numbers for interpolation

# Smoothing setup                   [Setup for Savitzky–Golay filter smoothing]
window_length = 5                                                              # <=== Insert the window length as the smoothing properties
polyorder = 1                                                                  # <=== Insert the polyorder as the smoothing properties

# Finding peaks             [Setup parameter for finding peaks on dQ/dV-V plot]
min_prominence = 50                                                            # <=== Insert the minimum prominence value
min_height = 50                                                                # <=== Insert the minimum height value

max_prominence = 800                                                           # <=== Insert the maximum prominence value
max_height = 800                                                               # <=== Insert the maximum height value

prominence_step = 10                                                           # <=== Insert the prominence value per iteration 
height_step = 10                                                               # <=== Insert the height value per iteration

window_size = 3                                                                # <=== Insert the window size for gaussian fitting                   

max_iterations = 500                                                           # <=== Insert the maximum iteration number

max_peaks = 5                                                                  # <=== Insert the maximum expected peaks

# Selecting parameters shown on plot
show_on_plot = [                                                               # <=== Insert the parameters to be shown on the plot: 
              #'data'                                                          #      - 'data':from neware;
              #'ori',                                                          #      - 'ori':pure calculation; 
              #'int',                                                          #      - 'int':interpolated data; 
              #'smooth',                                                       #      - 'smooth':interpolation,then filtering/smoothing  
                                                                               #         with Savitzky-Golay filter; 
              'peaks-fitting',                                                 #      - 'peaks-fitting':notate peaks and plot Gaussian 
                                                                               #         fitting curve on the plot             
               ]
    
DA01_Function_dQdV(file_name,df_cycle_grouped,df_VQ_grouped,show_on_plot,
                   interpolation_points,window_length,polyorder,window_size,
                   min_prominence,min_height,max_prominence,max_height,
                   prominence_step,height_step,max_iterations,max_peaks,
                   result_folder)

#-------------------------------SOH over cycles--------------------------------
DA01_Function_SOH(df_cycle_grouped,rated_capacity,file_name,result_folder)

DA01_Function_Statistical(df_main, df_cycle_grouped, file_name, result_folder)
#-----------------------------Correation (Heatmap)-----------------------------
# DA01_Function_Correlation(df_main,file_name,result_folder)

#-------------------------Machine Learning (Prediction)------------------------
DA01_Function_SOH_Prediction_Linear_Regression(result_folder,file_name,df_main)