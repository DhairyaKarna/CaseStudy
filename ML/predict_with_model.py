import pandas as pd
import os
import sys
import pickle

def predict_with_model(model_file, new_data_file, output_file):
    """
        Load a trained regression model from a file, make predictions on new data, and save the predictions to a file.
        
        Args:
            model_file (str): The file containing the trained regression model.
            new_data_file (str): The file containing the new data on which to make predictions.
            output_file (str): The file to which the predictions should be saved.
    """
    
    # Load the trained model from the file
    with open(model_file, "rb") as file:
        model = pickle.load(file)
    
    # Load the new data on which to make predictions
    new_data = pd.read_csv(new_data_file)
    
    # Make predictions on the new data
    predictions = model.predict(new_data)
    
    # Save the predictions to a file
    pd.Series(predictions).to_csv(output_file, index=False)


def main(prediction_file):
    """
        Main function for making predictions on new data using a trained regression model.
    """
    
    # Add the data directory to the path so that we can import the data files directly
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(parent_dir, "data/")
    sys.path.append(data_dir)
    
    # Assuming we recieve prediction_file as a parameter we first create the file paths
    model_file = os.path.join(data_dir, "random_forest_model.pkl")
    new_data_file = os.path.join(data_dir, prediction_file)
    output_file = os.path.join(data_dir, "predictions.csv")
    
    # Call the predict_with_model function to make predictions on the new data
    predict_with_model(model_file, new_data_file, output_file)
    print(f"Predictions saved to {output_file}")
    
if __name__ == "__main__":
    main()