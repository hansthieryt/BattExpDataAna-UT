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
9. SOH Prediction with Machine Learning

== Part of DA01 ==
- Function code for predicting SOH with machine learning


Authors: Hans and Matthias

"""

import os
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Load and preprocess the data
def DA01_Function_SOH_Prediction_Linear_Regression(result_folder,file_name,df_main):

    # Filter data to focus on cycles and SOH
    df_cycles = df_main.groupby('Cycle ID').agg({'SOH': lambda x: x.tail(1)}).reset_index()
    
    # # Convert 'Cycle_Time' from timedelta to total seconds for linear regression
    # df_cycles['Cycle_Time'] = df_cycles['Cycle_Time'].dt.total_seconds()

    # Extract cycle numbers (X) and SOH (y) for the regression model
    X = df_cycles[['Cycle ID']].values
    y = df_cycles['SOH'].values

    # Initialize and fit linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict future cycles until SOH reaches 0%
    # future_cycle_time = np.arange(X.max(), X.max() + 1000000, 10000)  # Simulate 10,000 steps with intervals
    # future_predictions = model.predict(future_cycle_time.reshape(-1, 1))
    future_cycle_ids = np.arange(X.max() + 1, X.max() + 100000, 1)  # Simulate 100000 future cycles
    future_predictions = model.predict(future_cycle_ids.reshape(-1, 1))

    # # Find the point where SOH reaches 0%
    # zero_soh_cycle = future_cycle_time[future_predictions <= 0][0] if np.any(future_predictions <= 0) else None
    # return print(f"Predicted cycle time when SOH reaches 0%: {zero_soh_cycle}")

    # Find the point where SOH reaches 0%
    zero_soh_cycle_id = future_cycle_ids[future_predictions <= 0][0] if np.any(future_predictions <= 0) else None
    return print(f"Predicted Cycle ID when SOH reaches 0%: {zero_soh_cycle_id}")