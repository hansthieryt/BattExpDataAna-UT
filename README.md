# Battery Experiment Data Analysis - University of Twente (BattExpDataAna-UT)
The **Battery Experiment Data Analysis - University of Twente (BattExpDataAna-UT)** repository is a collection of Python functions designed to process and analyze battery experiment data.t provides tools for importing raw battery test data, processing it into structured DataFrames, and performing various analyses to understand battery performance.he repository includes modules for data import, cycle grouping, and voltage vs. capacity plotting, among other functionalities.t also specifies software dependencies and provides instructions for getting started with the analysis.

## Software Dependencies
- Python
- Python packages (see requirements.txt)
  * os (pre-installed)
  * re (pre-installed)
  * functools (pre-installed)
  * pandas
  * matplotlib: pyplot, cm
  * numpy
  * scipy: signal (savgol_filter, find_peaks), interpolate (interp1d), optimize (curve_fit)
  * seaborn (for further development heatmap)
  * scikit-learn (for further development prediction)

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
Place your experimental data files in the DA_Data folder. Ensure they are in the correct format as expected by the scripts. Output from Neware BTSDA software with custom setting could result in the csv files which could be exported into series of TXT files in format "{file_name}_{sequence number}".

### 4. Running the Main Script
Execute the main script to start the data processing and analysis workflow:
```bash
python DA_Main.py
```
To execute certain data file pasted on 'DA_Data', change the input of 'file_name' and several other inputs on 'DA_main.py'.

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
![Data Processing & Analysis Diagram](images/DA_Diagram_WhiteBG.png)

### Data Pre-processing (Import)
#### `DA00_Function_Import`
This function imports raw battery data, compiling it into dataframe, and renaming it accordingly.
#### `DA00_Function_df_Cycle_Grouping`
This function prepares the data on dataframe by grouping and pre-processing by accumulate necessary value, then export to two dataframes.

### Direct Plotting
#### `DA01_Function_VnIvsTime`
This function generates plots of voltage and current variations over time during battery cycling.
#### `DA02_Function_VvsCap`
This function generates voltage vs. capacity plots to evaluate battery performance.

### Data Processing & Plotting
#### `DA01_Function_Power`
This function analyzes power by calculating it through voltage and current data over time during battery cycling.
#### `DA03_Function_Coulombic_Efficiency`
This function calculates Coulombic efficiency, a key indicator of battery charge efficiency, and generates the efficiency vs. cycle plot.
#### `DA04_Function_SOH.py`
This function calculates the State of Health (SOH) of the battery, a key indicator of battery health condition, and generates the SOH percentage vs. cycle plot.

### Data Processing & Analysis
#### `DA06_Function_dQdV`
This function calculates and visualizes the differential capacity (dQ/dV) curves. Following the curves, analysing the peaks detected for electrochemical reaction estimation analysis.


## Organization of the repository
```
|   DA_Main.py
|   LICENSE
|   README.md
|   requirements.txt
|
+---DA_Data
|   +---B1T1
|   |       B1T1_{sequence number: 0-32}
|   |       ....
|   |
|   +---M1C1
|   |       M1C1_0
|   |
|   +---M2C1
|   |       M2C1_0
|   |
|   +---N1T1
|   |       N1T1_{sequence number: 0-61}
|   |       ....
|   |
|
+---DA_Function
|   |   DA00_Function_Import_Main_df.py
|   |   DA00_Function_Import_Main_df_README.md
|   |   DA01_Function_VnIvsTime.py
|   |   DA01_Function_VnIvsTime_README.md
|   |   DA02_Function_VvsCap.py
|   |   DA02_Function_VvsCap_README.md
|   |   DA03_Function_Coulombic_Efficiency.py
|   |   DA03_Function_Coulombic_Efficiency_README.md
|   |   DA04_Function_SOH.py
|   |   DA04_Function_SOH_README.md
|   |   DA05_Function_Statistical_Model.py
|   |   DA06_Function_dQdV.py
|   |   DA06_Function_dQdV_README.md
|   |
|   +---For further development
|   |       ML01_Function_Correlation.py
|   |       ML02_Function_SOH_Prediction.py
|   |
|
+---images
|       DA_Diagram_WhiteBG.png
|
```

## Example execution

Example of the execution presented with the dataset on 'DA_Data' directory, with file_name: N1T1 and the battery properties, such as rated capacity 2100 mAh. The following is the example input on 'DA_Main.py'.
```bash
#----------------------------------Data input----------------------------------
data_folder = 'DA_Data'                                                        # <=== Insert folder of the data file(s)
result_folder = 'DA_Result'                                                    # <=== Insert folder for result
file_name = 'N1T1'                                                             # <=== Insert file name
rated_capacity = 2100                                                          # <=== Insert rated capacity of battery
df_main = DA00_Function_Import(data_folder,file_name,rated_capacity)

#----------------------------Data Grouping by Cycle----------------------------
df_cycle_grouped,df_VQ_grouped = DA00_Function_df_Cycle_Grouping(df_main,
                                                                  result_folder,
                                                                  file_name)

#----------------------------------VnIvsTime-----------------------------------
DA01_Function_VnIvsTime(result_folder,file_name,df_cycle_grouped)          

#------------------------------------Power-------------------------------------
DA01_Function_Power(result_folder,file_name,df_cycle_grouped)          

#--------------------------VvsCap (Potential Profile)--------------------------
DA02_Function_VvsCap(df_VQ_grouped,file_name,result_folder)

#-----------------------------Coulombic Efficiency-----------------------------
# Grouping based on cycle, combining CC Chg & CV Chg into one Chg data
DA03_Function_Coulombic_Efficiency(df_VQ_grouped,file_name,result_folder)  

#-------------------------------SOH over cycles--------------------------------
DA04_Function_SOH(df_cycle_grouped,rated_capacity,file_name,result_folder)

#-----------------------------Statistical Summary------------------------------
DA05_Function_Statistical(df_main, df_cycle_grouped, file_name, result_folder)

#------------------------------------dQ/dV-------------------------------------
# Interpolation setup
interpolation_points = 300                                                     # <=== Insert data point numbers for interpolation

# Smoothing setup                   [Setup for Savitzky–Golay filter smoothing]
window_length = 5                                                              # <=== Insert the window length as the smoothing properties
polyorder = 1                                                                  # <=== Insert the polyorder as the smoothing properties

# Finding peaks             [Setup parameter for finding peaks on dQ/dV-V plot]
min_prominence = 50                           #[Do not change if not necessary] <=== Insert the minimum prominence value
min_height = 50                               #[Do not change if not necessary] <=== Insert the minimum height value
max_prominence = 10000                        #[Do not change if not necessary] <=== Insert the maximum prominence value
max_height = 10000                            #[Do not change if not necessary] <=== Insert the maximum height value
prominence_step = 10                          #[Do not change if not necessary] <=== Insert the prominence value per iteration 
height_step = 10                              #[Do not change if not necessary] <=== Insert the height value per iteration            
max_iterations = 1000                         #[Do not change if not necessary] <=== Insert the maximum iteration number
max_peaks = 2                                 #[Do not change if not necessary] <=== Insert the maximum expected peaks

window_size = 3                               #[Do not change if not necessary] <=== Insert the window size for gaussian fitting       

# Selecting parameters shown on plot
show_on_plot = [                                                               # <=== Insert the parameters to be shown on the plot: 
              #'data'                                                          #      - 'data':from neware;
              #'ori',                                                          #      - 'ori':pure calculation; 
              #'int',                                                          #      - 'int':interpolated data; 
              'smooth',                                                        #      - 'smooth':interpolation,then filtering/smoothing  
                                                                               #         with Savitzky-Golay filter; 
              'peaks-fitting'                                                  #      - 'peaks-fitting':notate peaks and plot Gaussian 
                                                                               #         fitting curve on the plot             
                ]
    
DA06_Function_dQdV(file_name,df_VQ_grouped,show_on_plot,interpolation_points,
                   window_length,polyorder,window_size,min_prominence,
                   min_height,max_prominence,max_height,prominence_step,
                   height_step,max_iterations,max_peaks,result_folder)
```
