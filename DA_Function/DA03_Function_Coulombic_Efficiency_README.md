# `DA03_Function_Coulombic_Efficiency.py`

This function is part of the **Data Processing & Plotting Module** in the **Battery Experiment Data Analysis - University of Twente (BattExpDataAna-UT)** repository. It is responsible for calculating and plotting **Coulombic Efficiency (CE)** along with charge and discharge capacities over multiple battery cycles.

---

## **Function: DA03_Function_Coulombic_Efficiency**
### **Overview**
This function calculates the **Coulombic Efficiency (CE)** for each cycle, which is the ratio of discharge capacity to charge capacity. It also plots the CE and capacity values over the cycles.

### **Inputs**
- `df_VQ_grouped` (DataFrame): A structured dataframe containing voltage and capacity data for different cycles.
- `file_name` (str): The name of the file used for output naming.
- `result_folder` (str): The folder where processed results and plots will be saved.

### **Processing Steps**
1. Identifies cycle-related columns in `df_VQ_grouped`.
2. Extracts **charge** and **discharge** capacities for each cycle.
3. Calculates the **Coulombic Efficiency (CE)** for each cycle as `(Discharge Capacity / Charge Capacity) * 100`.
4. Creates a DataFrame of **Coulombic Efficiency**, **Charge Capacity**, and **Discharge Capacity** over cycles.
5. Plots **Coulombic Efficiency** against cycle number and saves the plot as an image file.
6. Saves the Coulombic Efficiency data as a CSV file.

### **Outputs**
- A **Coulombic Efficiency vs. Cycle plot** saved as `CE-cycles_{file_name}.png`.
- A CSV file containing **Coulombic Efficiency**, **Charge Capacity**, and **Discharge Capacity** for each cycle, saved as `df_CE_{file_name}.csv`.

### **Example Usage**
```python
from DA_Functions.DA03_Function_Coulombic_Efficiency import DA03_Function_Coulombic_Efficiency
import pandas as pd

# Load processed battery voltage-capacity data
df_VQ_grouped = pd.read_csv("Processed_Results/df_VQ_grouped.csv")

# Define output parameters
result_folder = "Processed_Results"
file_name = "battery_CE_plot"

# Generate Coulombic Efficiency plots
DA03_Function_Coulombic_Efficiency(df_VQ_grouped, file_name, result_folder)
```

### **Example Output**
This function will generate:
1. **Coulombic Efficiency vs. Cycle Plot**
2. **CSV file** containing Coulombic Efficiency and capacities for each cycle

#### **Example Plot Structure:**
- **X-axis:** Cycle ID
- **Y-axis:** Coulombic Efficiency (%)
- **Line 1:** Coulombic Efficiency (in blue)
- **Line 2:** Charge Capacity (in green)
- **Line 3:** Discharge Capacity (in red)

A sample plot file will be saved as:  
📂 `Processed_Results/battery_CE_plot/CE-cycles_battery_CE_plot.png`

---

## **Notes**
- The Coulombic Efficiency (CE) is calculated as the ratio of the discharge capacity to the charge capacity for each cycle.
- Ensure `df_VQ_grouped` contains the necessary columns for **Charge** and **Discharge** capacities before running the function.
- Missing data for any cycle will result in no plot for that cycle.

---
