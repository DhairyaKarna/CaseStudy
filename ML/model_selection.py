import pandas as pd
import os
import sys
import pickle
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


def main():
    """
        Main function for model selection and evaluation.
        This function loads the branch density and PM2.5 data, trains and evaluates multiple regression models,
        selects the best model based on evaluation metrics, and saves the model to a file.
        It also demonstrates how to use the model to make predictions on new data.
    """
    
    
    # Add the data directory to the path so that we can import the data files directly
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(parent_dir, "data/")
    sys.path.append(data_dir)
    
    # Load the branch density and PM2.5 data
    branch_density_pm_file = "branch_counts_with_pm25.xlsx"
    df = pd.read_excel(branch_density_pm_file)
    

    features = ["unique_bank_count", "unique_creditunion_count", "total_branch_count"]
    target = "mean_pm25_concentration"
    
    X = df[features]
    y = df[target]
    
    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Standardize the features because the Random Forest and Gradient Boosting models are not scale-invariant
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train and evaluate the models
    models = {
        "Random Forest": RandomForestRegressor(random_state=42),
        "Gradient Boosting": GradientBoostingRegressor(random_state=42),
        "Linear Regression": LinearRegression()
    }

    # Train and evaluate the models using the scaled data and display the results    
    results = {}
    for name, model in models.items():
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        rmse = sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        results[name] = {
            "RMSE": rmse,
            "R2": r2
        }

    # Display results
    print("Model Evaluation Results:")
    for name, metrics in results.items():
        print(f"\n{name}:")
        print(f"  Root Mean Squared Error (RMSE): {metrics['RMSE']}")
        print(f"  R-squared (R2): {metrics['R2']}")
        
    # After training the models, it turned out that the Random Forest model performed the best in terms of RMSE and R2.
    # Feature importance for Random Forest
    rf_model = models["Random Forest"]
    feature_importances = rf_model.feature_importances_
    importance_df = pd.DataFrame({"Feature": features, "Importance": feature_importances})
    print("\nFeature Importances (Random Forest):")
    print(importance_df.sort_values(by="Importance", ascending=False))
    
    
    # Predict PM2.5 levels for new data
    new_data = pd.DataFrame({
        "unique_bank_count": [10, 17, 24],  # Example bank counts
        "unique_creditunion_count": [5, 8, 11]  # Example credit union counts
    })
    new_data["total_branch_count"] = new_data["unique_bank_count"] + new_data["unique_creditunion_count"] 

    new_data_scaled = scaler.transform(new_data)
    new_predictions = rf_model.predict(new_data_scaled)

    plt.figure(figsize=(8, 6))
    plt.plot(new_data["total_branch_count"], new_predictions, marker='o', linestyle='-', color='b')
    plt.title("Predicted PM2.5 Levels vs Total Branch Count")
    plt.xlabel("Total Branch Count")
    plt.ylabel("Predicted PM2.5 Levels")
    plt.grid(True)
    plt.show()
    
    # Save the plot to a file named "predicted_pm25_vs_branch_count.png"
    plot_file = "predicted_pm25_vs_branch_count.png"
    plt.savefig(plot_file)
    print(f"\nPlot saved to {plot_file}")
    
    # Save the Random Forest model to a file
    model_file = "random_forest_model.pkl"
    pickle.dump(model, open(model_file, 'wb'))
    print(f"Random Forest model saved to {model_file}")
        
    
if __name__ == '__main__':
    main()