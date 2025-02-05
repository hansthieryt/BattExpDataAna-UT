# `DA02_Function_VvsCap.py`

This function is part of the **Direct Plotting Module** in the **Battery Experiment Data Analysis - University of Twente (BattExpDataAna-UT)** project. It is responsible for the initial import of raw battery experiment data and the pre-processing phase, such as filtering, sorting, grouping, naming, and preparing it for analysis by converting it into structured dataframes.

---

## **1. DA02_Function_VvsCap**
### **Function Overview**
This function analyzes the relationship between **voltage (V) and capacity (Ah)** during charge and discharge cycles of a battery.

### **Inputs**
- `data_folder` (str): The folder containing the raw battery data files.
- `file_name` (str): The name of the file to be imported.
- `rated_capacity` (float): The nominal capacity of the battery cell (Ah), used for normalization.

### **Processing Steps**
1. Reads raw data files from the specified `data_folder`.
2. Cleans missing or inconsistent values and applies necessary formatting.
3. Extracts voltage (`V`) and capacity (`Q`) values.
4. Structures the data into a processed dataframe for further analysis.

### **Outputs**
- `df_main` (DataFrame): A structured dataframe containing voltage vs. capacity data.

### **Example Usage**
```python
from DA_Functions.DA00_Function_Import_Main_df import import_main_df

# Define input parameters
data_folder = "DA_Data"
file_name = "battery_test_data.csv"
rated_capacity = 2.5  # in Ah

# Import battery data
df_main = import_main_df(data_folder, file_name, rated_capacity)
```

---

## **2. dQ/dV Analysis**
### **Function Overview**
This function plots the **differential capacity (dQ/dV) vs. voltage (V)**, which is useful for analyzing electrochemical behavior.

### **Inputs**
- `df_main` (DataFrame): The pre-processed dataframe containing voltage and capacity data.

### **Processing Steps**
1. Computes the differential capacity (dQ/dV) from capacity (`Q`) and voltage (`V`).
2. Plots **dQ/dV vs. Voltage** to highlight peaks corresponding to electrochemical phase transitions.

### **Outputs**
- A **plot of dQ/dV vs. V**, used for analyzing battery degradation and phase transitions.

### **Example Usage**
```python
from DA_Functions.DA06_Function_dQdV import plot_dqdv

# Generate dQ/dV vs. Voltage plot
plot_dqdv(df_main)
```

---

## **Notes**
- The **voltage vs. capacity** data is critical for assessing charge-discharge efficiency and battery aging.
- The **dQ/dV plot** is a key diagnostic tool for identifying battery degradation mechanisms.
- Ensure that the `data_folder` contains properly formatted raw data before running these functions.

---
