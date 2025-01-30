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
- Function code for Analysis of correlation (with heatmap)


Authors: Hans and Matthias

"""

import seaborn as sns
import matplotlib.pyplot as plt

#------------------------------VvsCap All Cycles-------------------------------
# Plot VOltage to Capacity
 
def DA01_Function_Correlation(df_main,file_name,result_folder):   
    # Specify the rated capacity and calculate SOH by dividing existing 
    # capacity by rated capacity   

    #Create heatmap based on correlation between variables and SOH
    correlation_matrix = df_main[['Voltage', 'Current', 'Capacity', 'Time', 'SOH']].corr()

    plt.figure(figsize=(16, 12))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title(f'Correlation Heatmap of Parameters vs SOH - {file_name}')
    plt.grid(True)
    plt.savefig(f'{result_folder}/{file_name}/Heatmap_{file_name}.png', dpi=300)
    plt.close()    
    return 
    
