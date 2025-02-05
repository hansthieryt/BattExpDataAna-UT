# `DA04_Function_SOH.py`

This function is part of the **Data Processing & Plotting Module** in the **Battery Experiment Data Analysis - University of Twente (BattExpDataAna-UT)** repository. It is responsible for calculating and plotting **State of Health (SOH)** over battery cycles, providing insights into the health of the battery during its usage.

---

## **Function: DA04_Function_SOH**
### **Overview**
This function calculates the **State of Health (SOH)** for each cycle based on the maximum capacity of each cycle and the rated capacity of the battery. It then plots the SOH over the cycles.

### **Inputs**
- `df_cycle_grouped` (DataFrame): A structured dataframe containing cycle data with cycle IDs and capacity values.
- `rated_capacity` (float): The rated capacity of the battery, used to calculate the SOH.
- `file_name` (str): The name of the file used for output naming.
- `result_folder` (str): The folder where processed results and plots will be saved.

### **Processing Steps**
1. Extracts the unique cycle IDs and the maximum capacity per cycle from `df_cycle_grouped`.
2. Calculates **State of Health (SOH)** as `(Max Capacity per Cycle / Rated Capacity) * 100`.
3. Creates a DataFrame containing **Cycle**, **Capacity**, and **SOH**.
4. Plots **State of Health (SOH)** against the cycle number and saves the plot as an image file.
5. Saves the SOH data as a CSV file.

### **Outputs**
- A **State of Health (SOH) vs. Cycle plot** saved as `SoH Plot_{file_name}.png`.
- A CSV file containing **Cycle**, **Capacity**, and **SOH** for each cycle, saved as `df_SOH_{file_name}.csv`.

### **Example Usage**
```python
from DA_Functions.DA04_Function_SOH import DA04_Function_SOH
import pandas as pd

# Load processed battery cycle data
df_cycle_grouped = pd.read_csv("Processed_Results/df_cycle_grouped.csv")

# Define rated capacity of the battery
rated_capacity = 2500  # Example rated capacity in mAh

# Define output parameters
result_folder = "Processed_Results"
file_name = "battery_SOH_plot"

# Generate SOH plots
DA04_Function_SOH(df_cycle_grouped, rated_capacity, file_name, result_folder)
```

### **Example Output**
This function will generate:
1. **State of Health (SOH) vs. Cycle Plot**
2. **CSV file** containing Cycle, Capacity, and SOH for each cycle

#### **Example Plot Structure:**
- **X-axis:** Cycle Number
- **Y-axis:** State of Health (SOH) (%)
- **Line:** SOH (in blue)

A sample plot file will be saved as:  
📂 `Processed_Results/battery_SOH_plot/SoH Plot_battery_SOH_plot.png`

---

## **Notes**
- The **State of Health (SOH)** is calculated as the ratio of the maximum capacity for each cycle to the rated capacity of the battery, expressed as a percentage.
- Ensure `df_cycle_grouped` contains the necessary columns for **Cycle ID** and **Capacity** before running the function.
- Missing data for any cycle will result in no plot for that cycle.

---
