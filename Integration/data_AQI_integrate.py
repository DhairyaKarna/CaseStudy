import pandas as pd
import os
import sys

def main():
    """
        This function integrates the data from the case study with the PM2.5 data.
        The data from the case study is in the file "20241125 Case Study for Position SE_Data (1).xlsx".
        The PM2.5 data is in the file "AQI_2020_means.xlsx".
        The integrated data is saved in the file "Integrated_with_PM25.xlsx".
    """
    
    # Add the data directory to the path so that we can import the data files directly
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(parent_dir, "data/")
    sys.path.append(data_dir)
    
    case_study_file = "20241125 Case Study for Position SE_Data (1).xlsx"
    aqi_means_file = "AQI_2020_means.xlsx"
    output_file = "Integrated_with_PM25.xlsx"
    
    sod_data = pd.read_excel(case_study_file, sheet_name="SOD_IL_2024")
    ncua_data = pd.read_excel(case_study_file, sheet_name="NCUA_IL_Q2_2024")
    aqi_means = pd.read_excel(aqi_means_file)
    
    # Define SOD columns
    columns_sod = [
        "CERT", "NAMEFULL", "ADDRESBR", "BRNUM", "ASSET", "DEPDOM",
        "DEPSUM", "STNAME", "CITYBR", "CNTYNAMB", "DEPSUMBR",
        "SIMS_LATITUDE", "SIMS_LONGITUDE", "geometry", "census_tract", "mean_pm25_concentration"
    ]

    # Merge SOD with PM2.5 data
    sod_data = pd.merge(sod_data, aqi_means, on="census_tract", how="left")
    sod_df = sod_data[columns_sod]
    
    sod_df = sod_df.dropna(subset=["census_tract"])
    
    columns_ncua = [
        "JOIN_NUMBER", "SiteId", "CU_NAME", "PhysicalAddressCity",
        "PhysicalAddressStateCode", "ATM", "DriveThru", "census tract", "mean_pm25_concentration"
    ]

    # Merge NCUA with PM2.5 data
    ncua_data = pd.merge(ncua_data.rename(columns={"census tract": "census_tract"}), aqi_means, on="census_tract", how="left")
    ncua_df = ncua_data.rename(columns={"census_tract": "census tract"})[columns_ncua]
    
    ncua_df = ncua_df.dropna(subset=["census tract"])
    ncua_df.rename(columns={"census tract": "census_tract"}, inplace=True)
    
    integrated_data = pd.concat([sod_df, ncua_df], ignore_index=True)
    
    # Reorder columns to have the census_tract in the beginning and mean_pm25_concentration at the end
    columns_order = ['census_tract'] + [col for col in integrated_data.columns if col not in ['census_tract', 'mean_pm25_concentration']] + ['mean_pm25_concentration']
    integrated_data = integrated_data[columns_order]
    
    integrated_data.to_excel(output_file, index=False)
    
    print("AQI Integrated data saved to", output_file)

if __name__ == "__main__":
    main()