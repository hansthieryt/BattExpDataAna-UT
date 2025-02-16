# -*- coding: utf-8 -*-
"""
Code for automated data preprocessing

Code Structure:
1. Main
2. DA00: Data Import, Dataframe creation, grouping
3. DA01: Plot & analysis of Voltage, Current, Power to Time
4. DA02: Plot & analysis of Voltage to Capacity (Potential Profile)
5. DA03: Plot & analysis of Coulombic Efficiency
6. DA04: Plot & analysis SOH over cycles
7. DA05: Analysis of Statistical Summary
    8. DA06: Plot & analysis of dQ/dV to Voltage

== Part of DA ==
- Function code for Plot & analysis of dQ/dV to Voltage


Authors: Hans and Matthias

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.interpolate import interp1d
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
import re

def DA06_Function_dQdV(file_name,df_VQ_grouped,show_on_plot,
                       interpolation_points,window_length,polyorder,
                       window_size,min_prominence,min_height,max_prominence,
                       max_height,prominence_step,height_step,max_iterations,
                       max_peaks,result_folder):

#----------------------------------Functions-----------------------------------
    # Function of interpolation to reduce data points
    def interpolate_data(x, y, num_points):
        if len(x) < 2 or len(y) < 2:
            return x, y  # No interpolation possible
        interpolation_func = interp1d(x, y, kind='linear')
        new_x = np.linspace(np.min(x), np.max(x), num_points)
        new_y = interpolation_func(new_x)
        return new_x, new_y

    # Function to smooth data using Savitzky-Golay filter
    def smooth_data(y,window_length,polyorder):
        if len(y) < 3:
            return y  # Not enough data to smooth
        return savgol_filter(y,window_length,polyorder)

    # Function for fitting
    def gaussian(x, amp, mean, sigma):
        # Convert inputs to float to avoid type mismatch errors
        amp, mean, sigma = map(float, (amp, mean, sigma))  # Convert parameters to float only
        return amp * np.exp(-(x - mean)**2 / (2 * sigma**2))  # Array-safe operation

#-----------------Initiation: create DataFrame & call Cycle ID-----------------   
    # Create DataFrames
    dqdv_data = []
    df_dqdv_data = []
    df_peaks_data = []
    gaussian_results = []

    # Extract unique cycle numbers from the column names
    cycle_columns = [col for col in df_VQ_grouped.columns if re.match(r'Cycle_\d+_', col)]
    cycle_numbers = sorted({int(re.search(r'Cycle_(\d+)_', col).group(1)) for col in cycle_columns})

#---------------Calculating & Smoothing dQ/dV, Plotting per Cycle--------------
    for cycle_id in cycle_numbers:

    #-------------------------------On Charging--------------------------------
        if f'Cycle_{cycle_id}_CapChg' in df_VQ_grouped and f'Cycle_{cycle_id}_VChg' in df_VQ_grouped and f'Cycle_{cycle_id}_dQdVChg' in df_VQ_grouped:
            capchg = df_VQ_grouped[f'Cycle_{cycle_id}_CapChg'].dropna()
            vchg = df_VQ_grouped[f'Cycle_{cycle_id}_VChg'].dropna()
            dqdvchg = df_VQ_grouped[f'Cycle_{cycle_id}_dQdVChg'].dropna()
            
            # Interpolate data
            vchg_interp, capchg_interp = interpolate_data(vchg,capchg,interpolation_points)
            
            # Calculate dQ/dV
            dQdV_chg_ori = np.diff(capchg) / np.diff(vchg)
            dQdV_chg_int = np.diff(capchg_interp) / np.diff(vchg_interp)
            dQdV_chg_smooth = smooth_data(dQdV_chg_int,window_length,polyorder)
           
            # Combine those data into dataframe
            dqdv_data = pd.DataFrame({
                f'Cycle_{cycle_id}_VChg': vchg_interp[:-1],
                # f'Cycle_{cycle_id}_dQdVChg_int': dQdV_chg_int,
                f'Cycle_{cycle_id}_dQdVChg_Smooth': dQdV_chg_smooth
            })
            df_dqdv_data.append(dqdv_data)
            
    #-----------------------------On Discharging-------------------------------
        if f'Cycle_{cycle_id}_CapDChg' in df_VQ_grouped and f'Cycle_{cycle_id}_VDChg' in df_VQ_grouped and f'Cycle_{cycle_id}_dQdVDChg' in df_VQ_grouped:
            capdchg = df_VQ_grouped[f'Cycle_{cycle_id}_CapDChg'].dropna()
            vdchg = df_VQ_grouped[f'Cycle_{cycle_id}_VDChg'].dropna()
            dqdvdchg = df_VQ_grouped[f'Cycle_{cycle_id}_dQdVDChg'].dropna()
            
            # Interpolate data
            vdchg_interp, capdchg_interp = interpolate_data(vdchg,capdchg,interpolation_points)
            
            # Calculate dQ/dV on interpolated data
            dQdV_dchg_ori = np.diff(capdchg) / np.diff(vdchg)
            dQdV_dchg_int = np.diff(capdchg_interp) / np.diff(vdchg_interp)
            dQdV_dchg_smooth = smooth_data(dQdV_dchg_int,window_length,polyorder)
            
            # Combine those data into dataframe
            dqdv_data = pd.DataFrame({
                f'Cycle_{cycle_id}_VDChg': vdchg_interp[:-1],
                # f'Cycle_{cycle_id}_dQdVDChg_int': dQdV_dchg_int,
                f'Cycle_{cycle_id}_dQdVDChg_Smooth': dQdV_dchg_smooth
            })
            df_dqdv_data.append(dqdv_data)

    #----------------------------Plotting per cycle----------------------------
        # Plotting dQ/dV vs Voltage
        if 'data' or 'ori' or 'int' or 'smooth' in show_on_plot:
            plt.figure(figsize=(10, 6))
     
            # Plot dQ/dV data from Neware
            if 'data' in show_on_plot:
                plt.plot(vchg, dqdvchg, label='Charge data', linestyle='--', color='purple')
                plt.plot(vdchg, dqdvdchg, label='Discharge data', linestyle='--', color='orange')
                
            # Plot calculated dQ/dV 
            if 'ori' in show_on_plot:
                plt.scatter(vchg[:-1], dQdV_chg_ori, label='Charge ori', color='purple')
                plt.scatter(vdchg[:-1], dQdV_dchg_ori, label='Discharge ori', color='orange')
                     
            # Plot interpolated dQ/dV
            if 'int' in show_on_plot:
                plt.plot(vchg_interp[:-1], dQdV_chg_int, label='Charge int', linestyle='--', color='cyan')
                plt.plot(vdchg_interp[:-1], dQdV_dchg_int, label='Discharge int', linestyle='--', color='yellow')
                
            # Plot smoothed dQ/dV
            if 'smooth' in show_on_plot:
                plt.plot(vchg_interp[:-1], dQdV_chg_smooth, label='Charge smooth', color='blue')
                plt.plot(vdchg_interp[:-1], dQdV_dchg_smooth, label='Discharge smooth', color='red')
        
            plt.xlabel('Voltage (V)')
            plt.ylabel('dQ/dV (mAh/V)')
            plt.ylim((dQdV_dchg_int.min()*1.05), (dQdV_chg_int.max()*1.05))
            plt.title(f'dQ/dV Curve of {file_name} Cycle {cycle_id}')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f'{result_folder}/{file_name}/dQdV_{file_name}_Cycle_{cycle_id}.png', dpi=300)
            plt.show()
            
        else:
            continue
     
    # Export the dQ/dV data to a CSV
    df_dqdv = pd.concat(df_dqdv_data, axis=1)
    df_dqdv.to_csv(f'{result_folder}/{file_name}/df_dQdV_{file_name}.csv', index=False)
    print("dQ/dV data saved successfully to",f'{result_folder}/{file_name}/df_dQdV_{file_name}.csv')
    pd.set_option('display.max_columns', None)  # Show all columns   
    print('DataFrame df_dqdv preview: ')
    print(df_dqdv.head(5))

#-----------------------------Plot all cycles----------------------------------       
    # Create the plot with a rainbow color map, all cycles
    colors = plt.cm.rainbow(np.linspace(0, 1, len(cycle_numbers)))
    plt.figure(figsize=(10, 6))
    
    for idx, cycle_id in enumerate(cycle_numbers):
        color = colors[idx]
        if cycle_id == 1:
            cycle_id = 2
            idx = 2
        else :
            #---------------------------On Charging----------------------------
            if f'Cycle_{cycle_id}_VChg' in df_dqdv and f'Cycle_{cycle_id}_dQdVChg_Smooth' in df_dqdv:
                plt.plot(df_dqdv[f'Cycle_{cycle_id}_VChg'], 
                         df_dqdv[f'Cycle_{cycle_id}_dQdVChg_Smooth'],  
                         color=color)

            #--------------------------On Discharging--------------------------
            if f'Cycle_{cycle_id}_VDChg' in df_dqdv and f'Cycle_{cycle_id}_dQdVDChg_Smooth' in df_dqdv:
                plt.plot(df_dqdv[f'Cycle_{cycle_id}_VDChg'],
                         df_dqdv[f'Cycle_{cycle_id}_dQdVDChg_Smooth'], 
                         linestyle='--', color=color)

    plt.xlabel('Voltage (V)')
    plt.ylabel('Diffential Capacity (dQ/dV)')
    plt.ylim(-8000, 8000)
    plt.title(f'Voltage vs dQ/dV for All Cycles - {file_name}')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'{result_folder}/{file_name}/All_Cycles_dQdV_{file_name}.png')
    plt.show()
      
#-----------------------Peaks finding & Gaussian Fitting-----------------------
    # Plot Charge dQ/dV with significant peaks
    if 'peaks-fitting' in show_on_plot:
        for cycle_id in cycle_numbers:                       
        #-----------------------------Peak Finding-----------------------------
            #---------------------------On Charging----------------------------
            height_range = min_height
            prominence_range = min_prominence
            Chg_peak_indices = []
            iterations = 0
            dqdv_chg_smooth = df_dqdv[f'Cycle_{cycle_id}_dQdVChg_Smooth']
            print(dqdv_chg_smooth)
            v_chg_smooth = df_dqdv[f'Cycle_{cycle_id}_VChg']
            
            # Looping height and prominence from minimum value for flexibility
            while (len(Chg_peak_indices) > max_peaks or len(Chg_peak_indices) == 0) and iterations < max_iterations:
                print(f"Iteration {iterations}: len(Chg_peak_indices) = {len(Chg_peak_indices)}, height_range = {height_range}, prominence_range = {prominence_range}")
    
                # Detect peaks
                Chg_peak_indices, _ = find_peaks(dqdv_chg_smooth, height=height_range, prominence=prominence_range)
    
                # Adjust height and prominence based on the number of detected peaks
                if len(Chg_peak_indices) > max_peaks:
                    print("Detected more than 2 peaks; increasing thresholds")
                    height_range = min(height_range + height_step, max_height)
                    prominence_range = min(prominence_range + prominence_step, max_prominence)
                elif len(Chg_peak_indices) == 0:
                    print("No peaks detected; decreasing thresholds")
                    height_range = max(height_range - height_step, min_height)
                    prominence_range = max(prominence_range - prominence_step, min_prominence)
    
                iterations += 1     # Increment iteration count
            
            # Final peak detection after exiting the loop
            Chg_peak_indices, _ = find_peaks(dqdv_chg_smooth, height=height_range, prominence=prominence_range)
            Chg_peak_voltages = v_chg_smooth[Chg_peak_indices]
            Chg_peak_heights = dqdv_chg_smooth[Chg_peak_indices]
            print(f"On Cycle {cycle_id},Charge, the Peaks are Peak Voltages: {Chg_peak_voltages}, Peak Heights: {Chg_peak_heights}, Peak Indices: {Chg_peak_indices}\n")
    
            #--------------------------On Discharging--------------------------
            height_range = min_height
            prominence_range = min_prominence
            DChg_peak_indices = []
            iterations = 0
            dqdv_dchg_smooth = df_dqdv[f'Cycle_{cycle_id}_dQdVDChg_Smooth']
            v_dchg_smooth = df_dqdv[f'Cycle_{cycle_id}_VDChg']
            
            # Looping height and prominence from minimum value for flexibility
            while (len(DChg_peak_indices) > max_peaks or len(DChg_peak_indices) == 0) and iterations < max_iterations:
                print(f"Iteration {iterations}: len(DChg_peak_indices) = {len(DChg_peak_indices)}, height_range = {height_range}, prominence_range = {prominence_range}")
    
                # Detect peaks
                DChg_peak_indices, _ = find_peaks(-dqdv_dchg_smooth, height=height_range, prominence=prominence_range)
    
                # Adjust height and prominence based on the number of detected peaks
                if len(DChg_peak_indices) > max_peaks:
                    print("Detected more than 2 peaks; increasing thresholds")
                    height_range = min(height_range + height_step, max_height)
                    prominence_range = min(prominence_range + prominence_step, max_prominence)
                elif len(Chg_peak_indices) == 0:
                    print("No peaks detected; decreasing thresholds")
                    height_range = max(height_range - height_step, min_height)
                    prominence_range = max(prominence_range - prominence_step, min_prominence)

                iterations += 1     # Increment iteration count
    
            # Final peak detection after exiting the loop
            DChg_peak_indices, _ = find_peaks(-dqdv_dchg_smooth, height=height_range, prominence=prominence_range)
            DChg_peak_voltages = v_dchg_smooth[DChg_peak_indices]
            DChg_peak_heights = dqdv_dchg_smooth[DChg_peak_indices]
            print(f"On Cycle {cycle_id}, Discharge, the Peaks are Peak Voltages: {DChg_peak_voltages}, Peak Heights: {DChg_peak_heights}, Peak Indices: {DChg_peak_indices}\n")

            # Combine peak data into a dataframe for further analysis or export
            peaks_data = pd.DataFrame({
                f'Voltage_Charge_Peaks_Cycle_{cycle_id}': Chg_peak_voltages.reset_index(drop=True),
                f'dQdV_Charge_Peaks_Cycle_{cycle_id}': Chg_peak_heights.reset_index(drop=True),
                f'Voltage_DisCharge_Peaks_Cycle_{cycle_id}': DChg_peak_voltages.reset_index(drop=True),
                f'dQdV_DisCharge_Peaks_Cycle_{cycle_id}': DChg_peak_heights.reset_index(drop=True),
                f'Overvoltage_Peaks_Cycle_{cycle_id}': Chg_peak_voltages.reset_index(drop=True)-DChg_peak_voltages.reset_index(drop=True)
            })
            df_peaks_data.append(peaks_data)
            
        #---------------Gaussian Fitting based on Detected Peaks---------------
            Chg_gauss_params = []
            DChg_gauss_params = []  
            Chg_gauss_area = []
            DChg_gauss_area = []
            
            #---------------------------On Charging----------------------------
            for Chg_peak in Chg_peak_indices:
                # Take a small window around each peak for fitting
                Chg_x_peak = v_chg_smooth[max(0, Chg_peak - window_size):min(len(v_chg_smooth), Chg_peak + window_size)]
                Chg_y_peak = dqdv_chg_smooth[max(0, Chg_peak - window_size):min(len(v_chg_smooth), Chg_peak + window_size)]
    
                # Initial guesses for amp, mean, sigma
                Chg_amp_guess = dqdv_chg_smooth[Chg_peak]
                Chg_mean_guess = v_chg_smooth[Chg_peak]
                Chg_sigma_guess = 0.05
                
                try:
                    Chg_popt, _ = curve_fit(gaussian, Chg_x_peak, Chg_y_peak, p0=[Chg_amp_guess, Chg_mean_guess, Chg_sigma_guess], maxfev=5000)
                    Chg_area = Chg_popt[0] * Chg_popt[2] * np.sqrt(2 * np.pi)
                    Chg_gauss_params.append(Chg_popt)  
                    Chg_gauss_area.append(Chg_area)
                except RuntimeError:
                    continue # Skip if fitting fails
                
            #--------------------------On Discharging--------------------------
            for DChg_peak in DChg_peak_indices:
                # Take a small window around each peak for fitting
                DChg_x_peak = v_dchg_smooth[max(0, DChg_peak - window_size):min(len(v_dchg_smooth), DChg_peak + window_size)]
                DChg_y_peak = dqdv_dchg_smooth[max(0, DChg_peak - window_size):min(len(v_dchg_smooth), DChg_peak + window_size)]
    
                # Initial guesses for amp, mean, sigma
                DChg_amp_guess = dqdv_dchg_smooth[DChg_peak]
                DChg_mean_guess = v_dchg_smooth[DChg_peak]
                DChg_sigma_guess = 0.5
                   
                # Fit Gaussian to each peak
                try:
                    DChg_popt, _ = curve_fit(gaussian, DChg_x_peak, DChg_y_peak, p0=[DChg_amp_guess, DChg_mean_guess, DChg_sigma_guess], maxfev=5000)
                    DChg_area = DChg_popt[0] * DChg_popt[2] * np.sqrt(2 * np.pi)
                    DChg_gauss_params.append(DChg_popt)     
                    DChg_gauss_area.append(DChg_area)
                except RuntimeError:
                    continue # Skip if fitting fails
            
            #------------------Plotting Fitted Curve on dQ/dV------------------
            plt.figure(figsize=(12, 6))

            # Plot the smoothed dQ/dV curve
            plt.plot(v_chg_smooth, dqdv_chg_smooth, label='Charge Smoothed dQ/dV curve', color='blue')
            plt.plot(v_dchg_smooth, dqdv_dchg_smooth, label='Discharge Smoothed dQ/dV curve', color='red')
                
            # Plot each fitted Gaussian
            for Chg_params in Chg_gauss_params:
                plt.plot(v_chg_smooth, gaussian(v_chg_smooth, *Chg_params), '--', label=f'Charging Gaussian fit (mean={Chg_params[1]:.2f})')
                
            # Highlight the detected peaks
            plt.scatter(v_chg_smooth[Chg_peak_indices], dqdv_chg_smooth[Chg_peak_indices], color='red', label='Charge Detected Peaks')
    
            # Plot each fitted Gaussian
            for DChg_params in DChg_gauss_params:
                plt.plot(v_dchg_smooth, gaussian(v_dchg_smooth, *DChg_params), '--', label=f'Discharging Gaussian fit (mean={DChg_params[1]:.2f})')
    
            # Highlight the detected peaks
            plt.scatter(v_dchg_smooth[DChg_peak_indices], dqdv_dchg_smooth[DChg_peak_indices], color='purple', label='Discharge Detected Peaks')
    
            # Add labels, title, and legend
            plt.xlabel('Voltage (V)')
            plt.ylabel('dQ/dV (mAh/V)')
            plt.ylim(dqdv_dchg_smooth[DChg_peak_indices].min(), dqdv_chg_smooth[Chg_peak_indices].max())
            plt.title(f'dQ/dV Curve with fitting of {file_name} Cycle {cycle_id}')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f'{result_folder}/{file_name}/dQdV_fitting_{file_name}_Cycle_{cycle_id}.png', dpi=300)
            plt.show()   
            
            #-------------------Compiling Fitted Properties--------------------
            peak_no_Chg = 1
            for chg_popt in Chg_gauss_params:
                chg_popt = list(chg_popt)  # Convert to list for safe concatenation
                chg_area = chg_popt[0] * chg_popt[2] * np.sqrt(2 * np.pi)
                chg_label = peak_no_Chg
                peak_no_Chg += 1
                gaussian_results.append([cycle_id, 'Charge', chg_label, *chg_popt, chg_area])
                
            peak_no_DChg = 1
            for dchg_popt in DChg_gauss_params:
                dchg_popt = list(dchg_popt)  # Convert to list for safe concatenation
                dchg_area = dchg_popt[0] * dchg_popt[2] * np.sqrt(2 * np.pi)
                dchg_label = peak_no_DChg
                peak_no_DChg += 1
                gaussian_results.append([cycle_id, 'Discharge', dchg_label, *dchg_popt, dchg_area])
                    
    #--------------------------------Exporting---------------------------------
        # Export peak data to CSV
        df_peaks = pd.concat(df_peaks_data, axis=1)
        df_peaks.to_csv(f'{result_folder}/{file_name}/df_peaks_{file_name}.csv', index=False)
        print("Peaks data saved successfully to", f'{result_folder}/{file_name}/df_peaks_{file_name}.csv')
        pd.set_option('display.max_columns', None)  # Show all columns   
        print('DataFrame df_peaks preview: ')
        print(df_peaks.head(5))
        
        # Export fitted peaks properties data to CSV
        df_fitting = pd.DataFrame(gaussian_results, columns=['Cycle ID', 'Status', 'Peak No', 'Amplitude', 'Mean', 'Sigma', 'Area'])
        df_fitting.to_csv(f'{result_folder}/{file_name}/df_fitting_{file_name}.csv', index=False)
        print("Gaussian fitting properties saved successfully to",f'{result_folder}/{file_name}/df_fitting_{file_name}.csv')
        pd.set_option('display.max_columns', None)  # Show all columns   
        print('DataFrame df_fitting preview: ')
        print(df_fitting.head(5))
    
    return df_dqdv, df_peaks, df_fitting