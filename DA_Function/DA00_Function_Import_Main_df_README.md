# `DA00_Function_Import_Main_df.py`

This function is part of the Data Pre-processing (Import) of Battery Experiment Data Analysis - University of Twente (BattExpDataAna-UT), which responsible for the initial import of raw battery experiment data and the pre-processing phase, such as filtering, sorting, grouping, naming, and preparing it for analysis by converting it into structured dataframes.

---
## DA00_Function_Import
### Input
- data_folder
- file_name
- rated_capacity 

### How It Works
- Reads raw data files from the `DA_Data` folder.
- Cleans missing values and formats the data.
- Returns structured dataframes for further processing.

### Output
- dataframes for further processing & analysis: df_main

### Usage
```python
from DA_Function.DA00_Function_Import_Main_df import import_main_df
df = import_main_df("datafile.csv")
```

---
## DA00_Function_df_Cycle_Grouping
### Input
- df_main
- result_folder
- file_name

### How It Works
- Reads raw data files from the `DA_Data` folder.
- Cleans missing values and formats the data.
- Returns structured dataframes for further processing.

### Output
- dataframes for further processing & analysis: df_cycle_grouped; df_VQ_grouped

### Usage
```python
from DA_Function.DA00_Function_Import_Main_df import import_main_df
df = import_main_df("datafile.csv")
```




### Running the Scripts
To run the main analysis script:
```bash
python DA_Main.py
```

## Functions
---
### Data Pre-processing (Import)

#### 1. `DA00_Function_Import_Main_df.py`
This function imports raw battery data, cleans it, and prepares it for analysis by converting it into structured dataframes.

How It Works
- Reads raw data files from the `DA_Data` folder.
- Cleans missing values and formats the data.
- Returns structured dataframes for further processing.

Usage
```python
from DA_Function.DA00_Function_Import_Main_df import import_main_df
df = import_main_df("datafile.csv")
```

### Direct Plotting
---

#### 2. `DA01_Function_VnIvsTime.py`
This function analyzes and visualizes voltage and current variations over time during battery cycling.

How It Works
- Reads the processed dataframe.
- Plots voltage and current against time.
- Helps analyze battery performance over charge-discharge cycles.

Usage
```python
from DA_Function.DA01_Function_VnIvsTime import plot_v_i_vs_time
plot_v_i_vs_time(df)
```

---

#### 3. `DA02_Function_VvsCap.py`
This function generates voltage vs. capacity plots to evaluate battery performance.

How It Works
- Extracts voltage and capacity data from the dataframe.
- Plots a curve to visualize capacity retention and efficiency.

Usage
```python
from DA_Function.DA02_Function_VvsCap import plot_v_vs_cap
plot_v_vs_cap(df)
```

### Data Processing & Plotting
---

#### 4. `DA03_Function_Coulombic_Efficiency.py`
This function calculates Coulombic efficiency, a key indicator of battery charge efficiency.

How It Works
- Computes Coulombic efficiency as:

  \[ CE = \frac{\text{Discharge Capacity}}{\text{Charge Capacity}} \times 100\% \]

- Returns efficiency percentage.

Usage
```python
from DA_Function.DA03_Function_Coulombic_Efficiency import calculate_ce
ce = calculate_ce(df)
print(f"Coulombic Efficiency: {ce}%")
```

---

#### 5. `DA04_Function_SOH.py`
This function calculates the State of Health (SOH) of the battery.

How It Works
- Compares current capacity to the original capacity.
- Determines battery degradation over time.

Usage
```python
from DA_Function.DA04_Function_SOH import calculate_soh
soh = calculate_soh(df, initial_capacity=100)
print(f"State of Health: {soh}%")
```

---

#### 6. `DA05_Function_Statistical_Model.py`
Applies statistical models to analyze battery performance data.

How It Works
- Performs regression or statistical trend analysis.
- Identifies patterns and predictions in battery performance.

Usage
```python
from DA_Function.DA05_Function_Statistical_Model import apply_stat_model
model_results = apply_stat_model(df)
print(model_results)
```

### Data Processing & Analysis
---

#### 7. `DA06_Function_dQdV.py`
This function calculates and visualizes the differential capacity (dQ/dV) curves.

How It Works
- Computes differential capacity to study electrochemical properties.
- Plots dQ/dV against voltage.

Usage
```python
from DA_Function.DA06_Function_dQdV import plot_dqdv
plot_dqdv(df)
```

