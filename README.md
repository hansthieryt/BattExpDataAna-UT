# Battery Experiment Data Analysis - University of Twente (BattExpDataAna-UT)
This repository contains Python functions for processing and analyzing battery experiment data. 

## Software Dependencies
- Python
- For python packages see requirements.txt

## Getting Started
### 1. Clone the Repository:
```bash
git clone https://github.com/hansthieryt/BattExpDataAna-UT.git
cd BattExpDataAna-UT
```

### 2. Install Dependencies
Ensure you have Python installed. Install the required Python packages using:
```bash
pip install -r requirements.txt
```

### 3. Prepare Data
Place your experimental data files in the DA_Data folder. Ensure they are in the correct format as expected by the scripts.

### 4. Running the Main Script
Execute the main script to start the data processing and analysis workflow:
```bash
python DA_Main.py
```


## Data Requirements
This package is designed to process multiple TXT files labeled in sequence as input and relies on specific column headers. Refer to the 'DA_Data' directory for example dataset files. The column header for each dataset file should include and appear exactly as follows:
- Cycle ID
- Step ID
- Step Name
- Record ID	Time(h:min:s.ms)
- Voltage(V)
- Current(mA)
- Capacity(mAh)
- Energy(mWh)
- Realtime
- dQ/dV(mAh/V)


## Functions Brief
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

---

## License
This project is licensed under the MIT License.

---
