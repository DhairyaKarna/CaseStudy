import pandas as pd
import os 
import sys

def main():
    """
        This function reads the case study data and the integrated data, and calculates the branch density for each dataset.
        The branch density is calculated as the number of branches per census tract.
        The function then saves the branch density data to an Excel file.
        This function also merges the branch density data with the AQI means data and saves the merged data to an Excel file.
    """
    
    
     # Add the data directory to the path so that we can import the data files directly
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(parent_dir, "data/")
    sys.path.append(data_dir)
    
    case_study_file = "20241125 Case Study for Position SE_Data (1).xlsx"
    integrated_aqi_data_file = "Integrated_with_PM25.xlsx"
    
    sod_data = pd.read_excel(case_study_file, sheet_name="SOD_IL_2024")
    ncua_data = pd.read_excel(case_study_file, sheet_name="NCUA_IL_Q2_2024")
    integrated_data = pd.read_excel(integrated_aqi_data_file)
    
    # Since all rows in SOD data are unique, we can simply count the number of rows for each census tract
    sod_branch_count = sod_data.groupby('census_tract').size().reset_index(name='bank_branch_count')
    sod_branch_count_desc = sod_branch_count.sort_values('bank_branch_count', ascending=False)
    
    # Since all rows in NCUA data are unique, we can simply count the number of rows for each census tract
    ncua_branch_count = ncua_data.groupby('census tract').size().reset_index(name='credit_union_branch_count')
    ncua_branch_count.rename(columns={'census tract': 'census_tract'}, inplace=True)
    ncua_branch_count_desc = ncua_branch_count.sort_values('credit_union_branch_count', ascending=False)
    
    # For the integrated data, we need to count the number of unique bank branches and credit union branches for each census tract
    integrated_sod_counts = integrated_data.groupby('census_tract')['CERT'].nunique().reset_index(name='unique_bank_count')
    integrated_ncua_counts = integrated_data.groupby('census_tract')['SiteId'].nunique().reset_index(name='unique_creditunion_count')
    integrated_branch_count = pd.merge(integrated_sod_counts, integrated_ncua_counts, on='census_tract', how='outer')
    integrated_branch_count['total_branch_count'] = integrated_branch_count['unique_bank_count'] + integrated_branch_count['unique_creditunion_count']
    integrated_branch_count_desc = integrated_branch_count.sort_values('total_branch_count', ascending=False)
    
    # Combine the SOD and NCUA branch counts
    sod_ncua_combined = pd.merge(sod_branch_count, ncua_branch_count, on='census_tract', how='outer')
    sod_ncua_combined.fillna(0, inplace=True)
    sod_ncua_combined['total_branch_count'] = sod_ncua_combined['bank_branch_count'] + sod_ncua_combined['credit_union_branch_count']
    sod_ncua_combined_desc = sod_ncua_combined.sort_values('total_branch_count', ascending=False)
    
    output_file = 'branch_counts.xlsx'
    with pd.ExcelWriter(output_file) as writer:
        sod_branch_count_desc.to_excel(writer, sheet_name='SOD', index=False)
        ncua_branch_count_desc.to_excel(writer, sheet_name='NCUA', index=False)
        integrated_branch_count_desc.to_excel(writer, sheet_name='Integrated', index=False)
        sod_ncua_combined_desc.to_excel(writer, sheet_name='SOD_NCUA_Combined', index=False)
        
    print("Branch density new data saved to", output_file)
    
    # Merge the integrated branch count data with the AQI means data
    aqi_means_file = "AQI_2020_means.xlsx"
    aqi_means = pd.read_excel(aqi_means_file)
    
    integrated_branch_count_with_pm25 = pd.merge(integrated_branch_count, aqi_means, on='census_tract', how='left')
    integrated_branch_count_with_pm25_desc = integrated_branch_count_with_pm25.sort_values('total_branch_count', ascending=False)
    
    # Save the integrated branch count data with AQI means to an Excel file
    output_file = 'branch_counts_with_pm25.xlsx'
    integrated_branch_count_with_pm25_desc.to_excel(output_file, index=False)
    
    print("Branch density data with PM2.5 saved to", output_file)

if __name__ == '__main__':
    main()