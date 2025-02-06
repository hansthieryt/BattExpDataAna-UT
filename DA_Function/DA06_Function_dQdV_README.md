# DA06_Function_dQdV

## Description

This Python function `DA06_Function_dQdV` processes battery cycling data to calculate, analyze, and visualize differential capacity (dQ/dV) versus voltage for charge and discharge cycles. The function provides functionalities for data interpolation, smoothing, peak detection, Gaussian fitting, and data visualization.

## Inputs
- `file_name`: Name of the input file (string).
- `df_VQ_grouped`: DataFrame containing voltage and capacity data for cycles.
- `show_on_plot`: A list of strings indicating which data types to plot (e.g., `'data'`, `'ori'`, `'int'`, `'smooth'`, `'peaks-fitting'`).
- `interpolation_points`: Number of points to interpolate data to.
- `window_length`: Window length for Savitzky-Golay smoothing.
- `polyorder`: Polynomial order for Savitzky-Golay smoothing.
- `window_size`: Window size for Gaussian fitting around peaks.
- `min_prominence`: Minimum prominence for peak detection.
- `min_height`: Minimum height for peak detection.
- `max_prominence`: Maximum prominence for peak detection.
- `max_height`: Maximum height for peak detection.
- `prominence_step`: Step to adjust prominence if too many peaks are detected.
- `height_step`: Step to adjust height if too many peaks are detected.
- `max_iterations`: Maximum number of iterations to adjust prominence and height.
- `max_peaks`: Maximum number of peaks to detect per cycle.
- `result_folder`: Directory where results will be saved.

## Processing Steps

### 1. dQ/dV Calculation & Smoothing

- **Interpolation**: Reduces data points for smoother analysis.
- **Smoothing**: Uses the Savitzky-Golay filter to smooth the dQ/dV data.
- **Calculation of dQ/dV**: The derivative of capacity with respect to voltage for both charge and discharge cycles.

### 2. Plotting

- **dQ/dV vs Voltage**: The function generates a plot of differential capacity against voltage, with options to display different versions (original, interpolated, smoothed).
- **Peak Detection and Fitting**: If `show_on_plot` includes `'peaks-fitting'`, the function will detect peaks and fit Gaussian curves to each peak, providing insights into the characteristics of the battery cycles.

### 3. Peak Detection

- **Peak Finding**: Detects peaks in the charge and discharge cycles using `find_peaks` from the `scipy` library.
- **Adjustable Parameters**: The function iteratively adjusts the prominence and height thresholds to find the optimal peaks based on `max_peaks`, `min_prominence`, `min_height`, `prominence_step`, and `height_step`.

### 4. Gaussian Fitting

- **Gaussian Fit**: A Gaussian model is fitted to the detected peaks to estimate their amplitude, mean, and standard deviation.
- **Overvoltage Calculation**: The overvoltage is calculated as the difference between the peak voltage of charge and discharge cycles.

### 5. Data Export

- **CSV Export**: The processed data (including dQ/dV and peaks) is saved to a CSV file in the specified `result_folder`.

### 6. Plotting All Cycles

- A plot displaying all cycles with charge and discharge curves is saved in the `result_folder`.

## Outputs
- dQ/dV plot
- 

## Notes

- The function assumes that the input data follows a specific naming convention for the columns related to each cycle.
- The user must ensure that the input DataFrames (`df_cycle_grouped` and `df_VQ_grouped`) contain the necessary columns for each cycle.
- The function provides flexibility in adjusting the peak detection and fitting parameters for different datasets.
  
## Example Output

The output consists of several files:
1. **dQ/dV Plot for Each Cycle**: Each cycle's dQ/dV plot is saved as an image (`.png` file).
2. **CSV File**: The `df_dQdV_{file_name}_filtered.csv` contains the dQ/dV data for all cycles.

### Example Plot Output

- A plot displaying the charge and discharge cycles' dQ/dV curves.
- Example output filename: `dQdV_{file_name}_Cycle_{cycle_id}.png`.

### Example CSV Output

The resulting CSV contains columns such as:
- `Cycle_1_VChg`, `Cycle_1_dQdVChg_Smooth`
- `Cycle_2_VChg`, `Cycle_2_dQdVChg_Smooth`
- And so on for each cycle.

## Example Usage

```python
DA06_Function_dQdV(
    file_name="battery_data", 
    df_cycle_grouped=df_cycle_grouped, 
    df_VQ_grouped=df_VQ_grouped, 
    show_on_plot=["data", "smooth", "peaks-fitting"], 
    interpolation_points=1000, 
    window_length=11, 
    polyorder=3, 
    window_size=5, 
    min_prominence=0.1, 
    min_height=0.1, 
    max_prominence=1.0, 
    max_height=2.0, 
    prominence_step=0.05, 
    height_step=0.1, 
    max_iterations=10, 
    max_peaks=3, 
    result_folder="results"
)
```

This function will process the battery data, generate dQ/dV plots, detect peaks, and fit Gaussian models to the peaks, saving the results in the specified `result_folder`.
