import pandas as pd
import os
import sys
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    """
        Main function for correlation analysis.
        This function loads the branch density and PM2.5 data, calculates the correlation matrix,
        and visualizes the correlation matrix using a heatmap
    """
      
    # Add the data directory to the path so that we can import the data files directly
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(parent_dir, "data/")
    sys.path.append(data_dir)
    
    # Load the branch density and PM2.5 data
    branch_density_pm_file = "branch_counts_with_pm25.xlsx"
    df = pd.read_excel(branch_density_pm_file)
    
    correlation = df[['unique_bank_count', 'unique_creditunion_count', 'total_branch_count', 'mean_pm25_concentration']].corr()
    
    # Plot the correlation matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Matrix")
    plt.show()

    # Save the correlation heatmap image
    correlation_heatmap_file = "correlation_heatmap.png"
    plt.savefig(correlation_heatmap_file)
    print(f"Correlation heatmap saved to {correlation_heatmap_file}")

if __name__ == "__main__":
    main()