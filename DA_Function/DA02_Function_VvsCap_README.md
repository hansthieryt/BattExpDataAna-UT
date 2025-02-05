# `DA02_Function_VvsCap.py`

This function is part of the **Direct Plotting Module** in the **Battery Experiment Data Analysis - University of Twente (BattExpDataAna-UT)** repository. It is responsible for plotting voltage vs. capacity (V-Q) across multiple battery cycles, providing insights into charge and discharge behavior over time.

---

## **Function: DA02_Function_VvsCap**
### **Function Overview**
This function generates **Voltage vs. Capacity (V-Q) plots** for all battery cycles recorded in `df_VQ_grouped`.

### **Inputs**
- `df_VQ_grouped` (DataFrame): A structured dataframe containing voltage and capacity data for different cycles.
- `file_name` (str): The name of the file used for output naming.
- `result_folder` (str): The folder where processed results and plots will be saved.

### **Processing Steps**
1. Identifies cycle-related columns in `df_VQ_grouped`.
2. Iterates through all available cycles and extracts **charge** and **discharge** data.
3. Uses **matplotlib** to generate **Voltage vs. Capacity plots** for all cycles.
4. Saves the plot as an image file in `result_folder`.

### **Outputs**
- A **V-Q plot for all cycles** saved as `All_Cycles_V-Q_{file_name}.png`.

### **Example Usage**
```python
from DA_Functions.DA02_Function_VvsCap import DA02_Function_VvsCap
import pandas as pd

# Load processed battery voltage-capacity data
df_VQ_grouped = pd.read_csv("Processed_Results/df_VQ_grouped.csv")

# Define output parameters
result_folder = "Processed_Results"
file_name = "battery_VQ_plot"

# Generate Voltage vs. Capacity plots
DA02_Function_VvsCap(df_VQ_grouped, file_name, result_folder)
```

### **Example Output**
This function will generate:
1. **Voltage vs. Capacity (V-Q) Plot for All Cycles**
2. **Voltage vs. Capacity (V-Q) Plot for Cycle 5**

#### **Example Plot Structure:**
- **X-axis:** Capacity (mAh)
- **Y-axis:** Voltage (V)
- **Solid lines:** Charge cycles
- **Dashed lines:** Discharge cycles

A sample plot file will be saved as:  
📂 `Processed_Results/battery_VQ_plot/All_Cycles_V-Q_battery_VQ_plot.png`

---

## **Notes**
- This function helps analyze battery capacity degradation over multiple cycles.
- Ensure `df_VQ_grouped` contains correctly labeled cycle data before running the function.
- If certain cycle data is missing, that cycle plot will not be generated.

---
