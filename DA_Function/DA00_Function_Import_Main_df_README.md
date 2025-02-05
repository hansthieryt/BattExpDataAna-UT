# `DA00_Function_Import_Main_df.py`

This function is part of the Data Pre-processing (Import) Module in the Battery Experiment Data Analysis - University of Twente (BattExpDataAna-UT), which responsible for the initial importing task of raw battery experiment data and the pre-processing tasks, such as filtering, sorting, grouping, and renaming. Overall, preparing it for analysis by converting it into structured dataframes.

---
## DA00_Function_Import
### Function Overview
This function imports raw battery cycling data, processes it into structured formats, and prepares it for further analysis.

### Input
- data_folder (str): The folder containing the raw battery data files.
- file_name (str): The name of the file to be imported.
- rated_capacity (float): The nominal capacity of the battery cell (Ah), used for normalization.

### Processing Steps
- Reads raw data files from the `DA_Data` folder.
- Cleans missing or inconsistent values and applies necessary formatting.
- Filters and organizes the data based on experimental parameters.
- Converts the cleaned data into structured pandas DataFrames.
- Returns structured dataframes for further processing.

### Outputs
- df_main (DataFrame): A structured dataframe containing pre-processed battery cycling data for further analysis.

### Example Usage
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
