import pandas as pd
import os
import sys
import spacy

# Load spaCy's pre-trained NLP model
nlp = spacy.load("en_core_web_sm")

# Function to interpret query
def parse_query(query, column_mappings):
    doc = nlp(query.lower())
    
    # Extract conditions and fields
    conditions = []
    for token in doc:
        if token.text in column_mappings.keys():
            column = column_mappings[token.text]
            
            # Handle numeric filters
            if token.nbor(-1).text in ["above", "greater"]:
                value = float([t.text for t in doc if t.like_num][0])
                conditions.append((column, ">", value))
            elif token.nbor(-1).text in ["below", "less"]:
                value = float([t.text for t in doc if t.like_num][0])
                conditions.append((column, "<", value))
    
    return conditions


# Function to dynamically filter dataset
def apply_conditions(conditions, df):
    filtered_df = df
    for column, operator, value in conditions:
        if operator == ">":
            filtered_df = filtered_df[filtered_df[column] > value]
        elif operator == "<":
            filtered_df = filtered_df[filtered_df[column] < value]
    return filtered_df


def main():
    
    
    # Add the data directory to the path so that we can import the data files directly
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(parent_dir, "data/")
    sys.path.append(data_dir)
    
    # Load the branch density and PM2.5 data
    branch_density_pm_file = "branch_counts_with_pm25.xlsx"
    df = pd.read_excel(branch_density_pm_file)
    
    # Prepare column mappings for easier matching
    column_mappings = {
        "pollution": "mean_pm25_concentration",
        "bank": "unique_bank_count",
        "credit union": "unique_creditunion_count",
        "total branches": "total_branch_count",
    }
    
    
    print("Welcome to the NLP Data Query Interface!")
    print("You can ask questions like:")
    print(" - Show me tracts with pollution above 9.0")
    print(" - List tracts with total branches greater than 20")
    
    while True:
        query = input("\nEnter your query (or type 'exit' to quit): ")
        if query.lower() == "exit":
            print("Goodbye!")
            break
        
        # Parse the query
        conditions = parse_query(query, column_mappings)
        
        if conditions:
            # Apply conditions to the dataset
            results = apply_conditions(conditions, df)
            
            if not results.empty:
                print("\nQuery Results:")
                print(results)
            else:
                print("\nNo results found for your query.")
        else:
            print("\nSorry, I couldn't understand your query. Please try again.")
    

if __name__ == '__main__':
    main()