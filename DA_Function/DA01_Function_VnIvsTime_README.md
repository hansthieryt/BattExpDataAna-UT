# `DA01_Function_VnIvsTime.py`

This function is part of the **Direct Plotting Module** in the **Battery Experiment Data Analysis - University of Twente (BattExpDataAna-UT)** project. It is responsible for importing raw battery experiment data and analyzing voltage and current behavior over time. The function processes the data and generates structured outputs for visualization and further analysis.

---

## **Function: DA01_Function_VnIvsTime**
### **Overview**
This function extracts voltage and current data over time from raw battery cycling experiments and visualizes trends.

### **Inputs**
- `data_folder` (str): The folder containing the raw battery data files.
- `file_name` (str): The name of the file to be imported.
- `rated_capacity` (float): The nominal capacity of the battery cell (Ah), used for normalization.

### **Processing Steps**
1. Reads raw data files from the specified `data_folder`.
2. Cleans missing or inconsistent values and applies necessary formatting.
3. Extracts voltage (`V`) and current (`I`) values over time.
4. Generates a visualization of voltage and current against time.

### **Outputs**
- A **plot of voltage and current vs. time**, useful for identifying battery charge/discharge behavior.

### **Example Usage**
```python
from DA_Functions.DA01_Function_VnIvsTime import plot_VnI_vs_time

# Define input parameters
data_folder = "DA_Data"
file_name = "battery_test_data.csv"
rated_capacity = 2.5  # in Ah

# Generate voltage and current vs. time plot
plot_VnI_vs_time(data_folder, file_name, rated_capacity)
```

### **Example Output**
This function will generate a **plot** displaying:
- **Voltage (V) vs. Time**
- **Current (I) vs. Time**  
This plot helps visualize charge and discharge cycles.

---

## **2. DA01_Function_Power**
### **Function Overview**
This function calculates and analyzes power behavior during battery cycling tests.

### **Inputs**
- `df_main` (DataFrame): The pre-processed dataframe obtained from `import_main_df`.
- `result_folder` (str): The folder where processed results will be saved.
- `file_name` (str): The name of the file used for naming output files.

### **Processing Steps**
1. Extracts voltage (`V`) and current (`I`) data from `df_main`.
2. Computes **power** using the formula:  
   \[
   P = V \times I
   \]
3. Structures the power data for further analysis.
4. Saves the processed power data in `result_folder`.

### **Outputs**
- `df_power` (DataFrame): A structured dataframe containing calculated power values over time.
- A CSV file containing power calculations saved in `result_folder`.

### **Example Usage**
```python
from DA_Functions.DA01_Function_Power import calculate_power
import pandas as pd

# Load processed battery cycling data
df_main = pd.read_csv("Processed_Results/df_main.csv")

# Define output parameters
result_folder = "Processed_Results"
file_name = "battery_power_data"

# Compute power
df_power = calculate_power(df_main, result_folder, file_name)

# Display first few rows of the power dataframe
print(df_power.head())
```

### **Example Output**
The function will generate a dataframe (`df_power`) with the following structure:

| Time (s) | Voltage (V) | Current (A) | Power (W) |
|----------|------------|------------|------------|
| 0        | 3.80       | 1.50       | 5.70       |
| 1        | 3.82       | 1.48       | 5.65       |
| 2        | 3.84       | 1.46       | 5.61       |
| ...      | ...        | ...        | ...        |

Additionally, a CSV file will be saved in `Processed_Results/battery_power_data.csv`.

---

## **Notes**
- The **voltage and current vs. time plot** is useful for identifying anomalies and trends in battery cycling behavior.
- The **power calculation function** helps assess **energy efficiency** and **performance**.
- Ensure that the `data_folder` contains properly formatted raw data before running these functions.

---
