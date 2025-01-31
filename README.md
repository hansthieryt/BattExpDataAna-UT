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
