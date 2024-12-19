import pandas as pd
import sqlite3
import os
import sys

def main():
    """
        This function reads the different sheets from the Case Study for Position SE_Data (1).xlsx file and 
        creates a new database with the Integrated_Data table.
        The function also saves the integrated data to an Excel file for backup purposes.    
    """
    
    # Add the data directory to the path so that we can import the data files directly
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(parent_dir, "data/")
    sys.path.append(data_dir)
    
    file_path = "20241125 Case Study for Position SE_Data (1).xlsx"
    xls = pd.ExcelFile(file_path)

    sheet_names = xls.sheet_names

    db_name = 'integrated_all_data.db'
    conn = sqlite3.connect(db_name)

    # Read the different sheets from the Excel file
    df_aq = pd.read_excel(xls, sheet_name="AirQuality_EPA_IL")
    df_sod = pd.read_excel(xls, sheet_name="SOD_IL_2024")
    df_ncua = pd.read_excel(xls, sheet_name="NCUA_IL_Q2_2024")

    # Rename columns to match the database schema and avoid SQL syntax errors
    df_ncua.rename(columns={"census tract": "census_tract"}, inplace=True)


    # Add suffixes to the columns to avoid column name conflicts
    df_aq = df_aq.add_suffix('_AQ')
    df_sod = df_sod.add_suffix('_SOD')
    df_ncua = df_ncua.add_suffix('_NCUA')

    # Merge the dataframes
    integrated_data = df_aq.merge(df_sod, left_on='census_tract_AQ', right_on='census_tract_SOD', how='left')\
                        .merge(df_ncua, left_on='census_tract_AQ', right_on='census_tract_NCUA', how='left')
                            
    integrated_data.to_sql("Integrated_Data", conn, if_exists="replace", index=False)
    print(integrated_data.head())

    integrated_data.to_excel("integrated_all_data.xlsx", index=False)

    conn.close()    
    
    print("All Integrated data saved to", db_name)
    print("All Integrated data saved to integrated_all_data.xlsx")


if __name__ == "__main__":
    main()                   