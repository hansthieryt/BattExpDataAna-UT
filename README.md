DA_Data_processing_and_Analysis (DA) - Ver. 1.0

Table of content
- DA_Data: folder containing datasets, likely experimental data.
- DA_Function: folder contains Python scripts for various processing and analysis functions:
	- DA00_Function_Import_Main_df.py: Likely imports and prepares the main dataframes.
	- DA01_Function_VnIvsTime.py: Analyzes voltage and current over time.
	- DA02_Function_VvsCap.py: Processes voltage versus capacity data.
	- DA03_Function_Coulombic_Efficiency.py: Calculates Coulombic efficiency.
	- DA04_Function_SOH.py: Computes State of Health (SOH).
	- DA05_Function_Statistical_Model.py: Implements statistical modeling.
	- DA06_Function_dQdV.py: Processes dQ/dV data.
	- ML01_Function_Correlation.py: Performs correlation analysis.
	- ML02_Function_SOH_Prediction.py: Conducts SOH prediction.
- DA_Result: folder dedicated to contain the results from running the scripts.
- DA_Main.py: Python file for input and to execute functions

The input parameters of data should include:
- Cycle ID	
- Step ID	
- Step Name	
- Record ID	
- Time(h:min:s.ms)	
- Voltage(V)	
- Current(mA)	
- Capacity(mAh)	
- Energy(mWh)	
- Realtime	
- dQ/dV(mAh/V)

  
# Battery Circularity Research - University of Twente

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

##Battery Circularity Research - University of Twente

Overview

This repository contains data processing and analysis tools developed for battery circularity research at the University of Twente. The tools are designed to process experimental data, perform various analyses, and support machine learning applications related to battery performance and health assessment.

#Repository Structure
	•	DA_Data: This folder contains datasets, likely experimental data, used for analysis.
	•	DA_Function: This folder contains Python scripts for various processing and analysis functions:
	•	DA00_Function_Import_Main_df.py: Imports and prepares the main dataframes for analysis.
	•	DA01_Function_VnIvsTime.py: Analyzes voltage and current over time to assess battery performance during cycling.
	•	DA02_Function_VvsCap.py: Processes voltage versus capacity data to evaluate battery capacity and energy efficiency.
	•	DA03_Function_Coulombic_Efficiency.py: Calculates Coulombic efficiency to determine the charge efficiency of the battery.
	•	DA04_Function_SOH.py: Computes the State of Health (SOH) to assess battery degradation and remaining useful life.
	•	DA05_Function_Statistical_Model.py: Implements statistical modeling for data analysis and prediction.
	•	DA06_Function_dQdV.py: Processes differential capacity (dQ/dV) data to analyze electrochemical properties.
	•	ML01_Function_Correlation.py: Performs correlation analysis to identify relationships between variables.
	•	ML02_Function_SOH_Prediction.py: Conducts State of Health prediction using machine learning techniques.
	•	DA_Main.py: The main script that orchestrates the data processing and analysis workflow by utilizing functions from the DA_Function folder.
	•	User Manual.md: A manual providing detailed instructions on how to use the scripts and tools in this repository.

#Getting Started
	1.	Clone the Repository:

git clone https://github.com/hansthieryt/Battery-Circularity-Research-University-of-Twente.git
cd Battery-Circularity-Research-University-of-Twente


	2.	Install Dependencies:
Ensure you have Python installed. Install the required Python packages using:

pip install -r requirements.txt


	3.	Prepare Data:
Place your experimental data files in the DA_Data folder. Ensure they are in the correct format as expected by the scripts.
	4.	Run the Main Script:
Execute the main script to start the data processing and analysis workflow:

python DA_Main.py

This script will call the necessary functions from the DA_Function folder to process the data and generate results.

#Function Descriptions
	•	DA00_Function_Import_Main_df.py:
Imports raw data files, cleans, and structures them into main dataframes for subsequent analysis.
	•	DA01_Function_VnIvsTime.py:
Plots and analyzes voltage and current profiles over time to monitor battery performance during charge-discharge cycles.
	•	DA02_Function_VvsCap.py:
Generates voltage versus capacity plots to evaluate the energy efficiency and capacity retention of the battery.
	•	DA03_Function_Coulombic_Efficiency.py:
Calculates the Coulombic efficiency by comparing the charge input to the discharge output, indicating the energy efficiency of the battery.
	•	DA04_Function_SOH.py:
Assesses the State of Health by analyzing capacity fade and internal resistance increase, providing insights into battery aging.
	•	DA05_Function_Statistical_Model.py:
Applies statistical models to the data to identify trends, correlations, and make predictions about battery performance.
	•	DA06_Function_dQdV.py:
Processes differential capacity (dQ/dV) curves to study phase transitions and electrochemical reactions within the battery.
	•	ML01_Function_Correlation.py:
Performs correlation analysis to identify significant relationships between different battery parameters.
	•	ML02_Function_SOH_Prediction.py:
Utilizes machine learning algorithms to predict the State of Health based on historical data and identified features.

# User Manual 

For detailed instructions on how to use each function and script, please refer to the User Manual.md file included in this repository.

# License

This project is licensed under the MIT License. See the LICENSE file for details.

# Acknowledgments

This research is conducted at the University of Twente, contributing to advancements in battery circularity and sustainability.

This README provides an overview of the repository’s structure, the purpose of each script, and instructions on how to get started with the analysis tools.
