# Battery Experiment Data Analysis - University of Twente (BattExpDataAna)

## Overview

This repository contains Python functions for processing and analyzing battery data. Below is a description of each function, including its purpose and how to use it.

---

## 1. `DA00_Function_Import_Main_df.py`

### Description
This function imports raw battery data, cleans it, and prepares it for analysis by converting it into structured dataframes.

### How It Works
- Reads raw data files from the `DA_Data` folder.
- Cleans missing values and formats the data.
- Returns structured dataframes for further processing.

### Usage
```python
from DA_Function.DA00_Function_Import_Main_df import import_main_df
df = import_main_df("datafile.csv")
```

---

## 2. `DA01_Function_VnIvsTime.py`

### Description
This function analyzes and visualizes voltage and current variations over time during battery cycling.

### How It Works
- Reads the processed dataframe.
- Plots voltage and current against time.
- Helps analyze battery performance over charge-discharge cycles.

### Usage
```python
from DA_Function.DA01_Function_VnIvsTime import plot_v_i_vs_time
plot_v_i_vs_time(df)
```

---

## 3. `DA02_Function_VvsCap.py`

### Description
This function generates voltage vs. capacity plots to evaluate battery performance.

### How It Works
- Extracts voltage and capacity data from the dataframe.
- Plots a curve to visualize capacity retention and efficiency.

### Usage
```python
from DA_Function.DA02_Function_VvsCap import plot_v_vs_cap
plot_v_vs_cap(df)
```

---

## 4. `DA03_Function_Coulombic_Efficiency.py`

### Description
This function calculates Coulombic efficiency, a key indicator of battery charge efficiency.

### How It Works
- Computes Coulombic efficiency as:

  \[ CE = \frac{\text{Discharge Capacity}}{\text{Charge Capacity}} \times 100\% \]

- Returns efficiency percentage.

### Usage
```python
from DA_Function.DA03_Function_Coulombic_Efficiency import calculate_ce
ce = calculate_ce(df)
print(f"Coulombic Efficiency: {ce}%")
```

---

## 5. `DA04_Function_SOH.py`

### Description
This function calculates the State of Health (SOH) of the battery.

### How It Works
- Compares current capacity to the original capacity.
- Determines battery degradation over time.

### Usage
```python
from DA_Function.DA04_Function_SOH import calculate_soh
soh = calculate_soh(df, initial_capacity=100)
print(f"State of Health: {soh}%")
```

---

## 6. `DA05_Function_Statistical_Model.py`

### Description
Applies statistical models to analyze battery performance data.

### How It Works
- Performs regression or statistical trend analysis.
- Identifies patterns and predictions in battery performance.

### Usage
```python
from DA_Function.DA05_Function_Statistical_Model import apply_stat_model
model_results = apply_stat_model(df)
print(model_results)
```

---

## 7. `DA06_Function_dQdV.py`

### Description
This function calculates and visualizes the differential capacity (dQ/dV) curves.

### How It Works
- Computes differential capacity to study electrochemical properties.
- Plots dQ/dV against voltage.

### Usage
```python
from DA_Function.DA06_Function_dQdV import plot_dqdv
plot_dqdv(df)
```

---

## 8. `ML01_Function_Correlation.py`

### Description
Performs correlation analysis between different battery parameters.

### How It Works
- Computes correlation matrix.
- Identifies key factors affecting battery performance.

### Usage
```python
from DA_Function.ML01_Function_Correlation import compute_correlation
correlation_matrix = compute_correlation(df)
print(correlation_matrix)
```

---

## 9. `ML02_Function_SOH_Prediction.py`

### Description
This function uses machine learning to predict battery State of Health (SOH).

### How It Works
- Trains a predictive model using historical SOH data.
- Predicts future SOH values based on input features.

### Usage
```python
from DA_Function.ML02_Function_SOH_Prediction import train_soh_model, predict_soh

model = train_soh_model(df)
predicted_soh = predict_soh(model, new_data)
print(f"Predicted SOH: {predicted_soh}%")
```

---

## Getting Started

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Running the Scripts
To run the main analysis script:
```bash
python DA_Main.py
```

---

## License
This project is licensed under the MIT License.

---

This `README.md` provides descriptions and usage examples for each function. Let me know if you need any modifications!
