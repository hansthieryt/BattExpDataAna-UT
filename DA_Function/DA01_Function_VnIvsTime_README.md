# `DA01_Function_VnIvsTime.py`

This function is part of the **Direct Plotting Module** in the **Battery Experiment Data Analysis - University of Twente (BattExpDataAna-UT)** project. It is responsible for plotting **Voltage and Current vs. Time**, allowing visualization of battery behavior across multiple cycles.

---

## **Function DA01_Function_VnIvsTime**
### **Overview**
This function generates **Voltage and Current vs. Time plots** for each cycle in `df_cycle_grouped`, as well as a combined plot for all cycles.

### **Inputs**
- `result_folder` (str): The folder where processed results and plots will be saved.
- `file_name` (str): The name of the file used for output naming.
- `df_cycle_grouped` (DataFrameGroupBy): Grouped dataframe containing voltage, current, and time data for different cycles.

### **Processing Steps**
1. Iterates through all available cycles and extracts **Voltage and Current vs. Time** data.
2. Uses **matplotlib** to generate **Voltage and Current vs. Time plots** for each cycle.
3. Generates a **combined plot** displaying all cycles in different colors.
4. Saves the plots as image files in `result_folder`.

### **Outputs**
- **Voltage and Current vs. Time plot** for each cycle, saved as `VnCvsTime_{file_name}_Cycle{i}.png`.
- **Combined plot** for all cycles, saved as `VnCvsTime_{file_name}_AllCycles.png`.

### **Example Usage**
```python
from DA_Functions.DA01_Function_VnIvsTime import DA01_Function_VnIvsTime
import pandas as pd

# Load processed battery cycle data
df_cycle_grouped = pd.read_csv("Processed_Results/df_cycle_grouped.csv").groupby("Cycle")

# Define output parameters
result_folder = "Processed_Results"
file_name = "battery_VnI_plot"

# Generate Voltage and Current vs. Time plots
DA01_Function_VnIvsTime(result_folder, file_name, df_cycle_grouped)
```

### **Example Output**
This function will generate:
1. **Voltage and Current vs. Time Plot for Each Cycle**
2. **Voltage and Current vs. Time Combined Plot for All Cycles**

#### **Example Plot Structure:**
- **X-axis:** Cycle Time (s)
- **Left Y-axis:** Voltage (V)
- **Right Y-axis:** Current (mA)
- **Solid lines:** Voltage data
- **Dashed lines:** Current data

A sample plot file will be saved as:  
📂 `Processed_Results/battery_VnI_plot/VnCvsTime_battery_VnI_plot_AllCycles.png`

---

## **Function: DA01_Function_VnIvsTime_Combined**
### **Overview**
This function generates a **Voltage and Current vs. Time plot** for a combined dataset containing multiple cycles.

### **Inputs**
- `combined_result_folder` (str): The folder where the plot will be saved.
- `df_combined` (DataFrame): A dataframe containing cycle time, voltage, and current data for multiple cycles.

### **Outputs**
- A **combined Voltage and Current vs. Time plot**, saved as `VnCvsTime_Combined.png`.

### **Example Usage**
```python
from DA_Functions.DA01_Function_VnIvsTime import DA01_Function_VnIvsTime_Combined
import pandas as pd

# Load combined battery cycle data
df_combined = pd.read_csv("Processed_Results/df_combined.csv")

# Define output parameters
combined_result_folder = "Processed_Results"

# Generate combined Voltage and Current vs. Time plot
DA01_Function_VnIvsTime_Combined(combined_result_folder, df_combined)
```

### **Example Output**
A sample plot file will be saved as:  
📂 `Processed_Results/VnCvsTime_Combined.png`

---

## **3. DA01_Function_Power**
### **Function Overview**
This function generates **Power vs. Time plots** for each cycle and a combined plot for all cycles.

### **Inputs**
- `result_folder` (str): The folder where processed results and plots will be saved.
- `file_name` (str): The name of the file used for output naming.
- `df_cycle_grouped` (DataFrameGroupBy): Grouped dataframe containing cycle time, voltage, and current data for different cycles.

### **Processing Steps**
1. Iterates through all available cycles and calculates **Power (Voltage × Current)**.
2. Uses **matplotlib** to generate **Power vs. Time plots** for each cycle.
3. Generates a **combined plot** displaying all cycles in different colors.
4. Saves the plots as image files in `result_folder`.

### **Outputs**
- **Power vs. Time plot** for each cycle, saved as `PvsTime_{file_name}_Cycle{i}.png`.
- **Combined Power vs. Time plot**, saved as `PvsTime_{file_name}_AllCycles.png`.

### **Example Usage**
```python
from DA_Functions.DA01_Function_VnIvsTime import DA01_Function_Power
import pandas as pd

# Load processed battery cycle data
df_cycle_grouped = pd.read_csv("Processed_Results/df_cycle_grouped.csv").groupby("Cycle")

# Define output parameters
result_folder = "Processed_Results"
file_name = "battery_power_plot"

# Generate Power vs. Time plots
DA01_Function_Power(result_folder, file_name, df_cycle_grouped)
```

### **Example Output**
This function will generate:
1. **Power vs. Time Plot for Each Cycle**
2. **Power vs. Time Combined Plot for All Cycles**

#### **Example Plot Structure:**
- **X-axis:** Cycle Time (s)
- **Y-axis:** Power (kW)

A sample plot file will be saved as:  
📂 `Processed_Results/battery_power_plot/PvsTime_battery_power_plot_AllCycles.png`

---

## **Notes**
- This function helps analyze battery power variations over multiple cycles.
- Ensure `df_cycle_grouped` and `df_combined` contain correctly labeled cycle data before running the functions.
- If any cycle data is missing, respective plots will not be generated.

---
