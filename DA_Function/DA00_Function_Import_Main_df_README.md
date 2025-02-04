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
