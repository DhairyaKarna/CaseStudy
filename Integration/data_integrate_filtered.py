import pandas as pd
import sqlite3
import os
import sys

def main():
    """
    This function reads the integrated_data.xlsx file and creates a new database with the integrated_filtered_data table.
    """
    
    # Add the data directory to the path so that we can import the data files directly
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(parent_dir, "data/")
    sys.path.append(data_dir)
    
    file_path = "integrated_data.xlsx"
    xls = pd.ExcelFile(file_path)

    # Create a new database 
    db_name = 'integrated_filtered_data.db'
    conn = sqlite3.connect(db_name)

    # Columns under consideration for the ML model and NLP Interface
    columns_aq = [
        "census_tract", "latitude", "longitude", "parameter", "sample_duration",
        "year", "event_type", "observation_count", "observation_percent", 
        "arithmetic_mean", "standard_deviation", "cbsa_code", "cbsa", "geometry"
    ]

    columns_sod = [
        "CERT", "NAMEFULL", "ADDRESBR", "BRNUM", "ASSET", "DEPDOM",
        "DEPSUM", "STNAME", "CITYBR", "CNTYNAMB", "DEPSUMBR",
        "SIMS_LATITUDE", "SIMS_LONGITUDE", "geometry", "census_tract"
    ]

    columns_ncua = [
        "JOIN_NUMBER", "SiteId", "CU_NAME", "PhysicalAddressCity",
        "PhysicalAddressStateCode", "ATM", "DriveThru", "census tract"
    ]

    df_aq = pd.read_excel(xls, sheet_name="AirQuality_EPA_IL", usecols=columns_aq)
    df_sod = pd.read_excel(xls, sheet_name="SOD_IL_2024", usecols=columns_sod)
    df_ncua = pd.read_excel(xls, sheet_name="NCUA_IL_Q2_2024", usecols=columns_ncua)
    
    # rename columns to prevent SQL syntax errors
    df_ncua.rename(columns={"census tract": "census_tract"}, inplace=True)

    # Merge the dataframes on the census_tract column and create a new table 
    df_aq = df_aq.add_suffix('_AQ')
    df_sod = df_sod.add_suffix('_SOD')
    df_ncua = df_ncua.add_suffix('_NCUA')

    integrated_filtered_data = df_aq.merge(df_sod, left_on='census_tract_AQ', right_on='census_tract_SOD', how='left')\
                        .merge(df_ncua, left_on='census_tract_AQ', right_on='census_tract_NCUA', how='left')
    
    # Rename the columns to remove the suffixes for census_tract and reordering the columns                    
    integrated_filtered_data.rename(columns={"census_tract_AQ": "census_tract"}, inplace=True)
    columns_order = ['census_tract'] + [col for col in integrated_filtered_data.columns if col != 'census_tract']
    integrated_filtered_data = integrated_filtered_data[columns_order]

    integrated_filtered_data.drop(columns=['census_tract_SOD', 'census_tract_NCUA'], inplace=True)
    integrated_filtered_data.drop_duplicates(inplace=True)

    # Drop rows with missing values in the SOD and NCUA columns
    sod_columns = [col for col in integrated_filtered_data.columns if '_SOD' in col]
    ncua_columns = [col for col in integrated_filtered_data.columns if '_NCUA' in col]

    integrated_filtered_data = integrated_filtered_data[integrated_filtered_data[sod_columns + ncua_columns].notna().any(axis=1)]

    # Save the integrated_filtered_data table to the database and an excel file                        
    integrated_filtered_data.to_sql("Integrated_Filtered_Data", conn, if_exists="replace", index=False)
    integrated_filtered_data.to_excel("integrated_filtered_data.xlsx", index=False)
    print(integrated_filtered_data.head())

    conn.close()              
    
    print("Integrated filtered data saved to", db_name)
    print("Integrated filtered data saved to integrated_filtered_data.xlsx")         


if __name__ == "__main__":
    main()