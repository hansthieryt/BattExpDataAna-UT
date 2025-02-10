# DA00_Function_Import_Main_df

This function is part of the **Data Import Module** in the **Battery Experiment Data Analysis - University of Twente (BattExpDataAna-UT)** repository. It is responsible for importing raw battery test data from multiple files, processing it into a structured DataFrame, and grouping data for further analysis.

---

## **Function: DA00_Function_Import**
### **Overview**
This function imports multiple raw battery test files, processes them by renaming columns, formatting timestamps, and calculating **State of Health (SOH)** for each data point.

### **Inputs**
- **data_folder (str):** Path to the folder containing battery test files.
- **file_name (str):** Name of the battery test file (excluding index and extension).
- **rated_capacity (float):** The nominal capacity of the battery cell, used for SOH calculation.

### **Processing Steps**
1. Iterates through all available Neware `.txt` files within the specified folder.
2. Reads data while removing headers and ensuring proper decimal formatting.
3. Renames relevant columns for consistency:
   - `Time(h:min:s.ms)` → `Time`
   - `Voltage(V)` → `Voltage`
   - `Current(mA)` → `Current`
   - `Capacity(mAh)` → `Capacity`
   - `dQ/dV(mAh/V)` → `dQdV`
4. Converts `Realtime` to pandas datetime format.
5. Converts `Time` into a timedelta format for cycle-wise accumulation.

### **Outputs**
- A **structured DataFrame** (`df_main`) with imported and processed battery data.

---

## **Function: DA00_Function_df_Cycle_Grouping**
### **Overview**
This function groups battery test data by **Cycle ID** and organizes charge/discharge data for further analysis.

### **Inputs**
- **df_main (DataFrame):** The structured battery data imported using `DA00_Function_Import`.
- **result_folder (str):** Folder path for saving processed results.
- **file_name (str):** Name used for output files.

### **Processing Steps**
1. Creates a result folder if it does not exist.
2. Groups the DataFrame by `Cycle ID` into `df_cycle_grouped` DataFrame
4. Accumulates charge capacity value phases (`CC_Chg`, `CV_Chg`)
5. Extracts Voltage and Capacity values per cycle in columns (axis=1) into DataFrame `df_VQ_grouped`.
6. Saves the DataFrame into `df_VQ_grouped.csv`.

### **Outputs**
- **df_cycle_grouped:** A grouped DataFrame by cycle ID.
- **df_VQ_grouped.csv:** Processed charge/discharge data per cycle.

---

## **Notes**
- Ensure all `.txt` files are correctly formatted before running the import function.
- The function stops reading when a missing file is detected in the sequence.
- Grouped cycle data enables further analysis, such as **Voltage vs. Capacity (V-Q) plotting**.

---
