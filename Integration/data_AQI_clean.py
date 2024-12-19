import pandas as pd
import os
import sys

def main():
    """
        There was an issue with provided case study dataset
        (There were mulitple missing values in the 'census_tract' column in the AirQuality sheet that were present in the SOD & NCUA sheet).
        Therefore, we decided to calculate the mean PM2.5 concentration for each census tract in 2020 using the AQI data.
        This function reads the AQI data and calculates the mean PM2.5 concentration for each census tract in 2020.
        The function then saves the results to an Excel file.
    """
    
    # Add the data directory to the path so that we can import the data files directly
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(parent_dir, "data/")
    sys.path.append(data_dir)
    
    AQI_df = pd.read_csv("Daily_Census_Tract-Level_PM2.5_Concentrations__2016_-_2020.csv") 
    
    # Filter the data for 2020 and calculate the mean PM2.5 concentration for each census tract
    AQI_2020 = AQI_df[AQI_df['year'] == 2020]
    AQI_2020_means = AQI_2020.groupby('ctfips')['DS_PM_pred'].mean().reset_index(name='mean_pm25_concentration')
    
    AQI_2020_means.rename(columns={'ctfips': 'census_tract'}, inplace=True)
    
    output_file = 'AQI_2020_means.xlsx'
    AQI_2020_means.to_excel(output_file, index=False)  
    
    print("Mean PM2.5 concentration data for 2020 saved to", output_file)

if __name__ == "__main__":
    main()