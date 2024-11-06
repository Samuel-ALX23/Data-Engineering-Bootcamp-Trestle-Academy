import pandas as pd
import numpy as np
import requests
from io import StringIO
from datetime import datetime

file_path = r"https://drive.google.com/uc?id=19bgbc4hU69jVNRTdXH3S1FfAuv-V8Efx"

try:
    # Fetch the CSV file
    response = requests.get(file_path)
    response.raise_for_status()  # Raise an error for bad responses

    # Load the CSV content into a DataFrame
    from io import StringIO
    data = pd.read_csv(StringIO(response.text))

    # Display the first few rows of the dataframe
    print(data.head())

except requests.exceptions.RequestException as e:
    print(f"Error loading dataset: {e}")
except Exception as e:
    print(f"An error occurred: {e}")


def load_dataset(file_path):
    """
    Load the dataset and perform initial inspection
    """
    try:
        df = pd.read_csv(file_path)
        print("Dataset loaded successfully!")
        print("\nInitial shape:", df.shape)
        print("\nColumns:", df.columns.tolist())
        print("\nData Preview:")
        print(df.head())
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

def check_missing_values(df):
    """
    Identify and handle missing values
    """
    print("\n=== Missing Values Analysis ===")
    missing_stats = df.isnull().sum()
    print("\nMissing values per column:")
    print(missing_stats)
    
    # Fill missing values based on data type
    df['age'] = df['age'].fillna(df['age'].median())
    df['course'] = df['course'].fillna('Unknown')
    df['enrollment_date'] = df['enrollment_date'].fillna(df['enrollment_date'].mode()[0])
    df['is_intern'] = df['is_intern'].fillna('No')
    
    return df

def standardize_datatypes(df):
    """
    Convert columns to appropriate data types
    """
    try:
        # Convert age to integer
        df['age'] = df['age'].astype(int)
        
        # Convert enrollment_date to datetime
        df['enrollment_date'] = pd.to_datetime(df['enrollment_date'])
        
        print("\nData types standardized successfully!")
        print("\nCurrent data types:")
        print(df.dtypes)
        return df
    except Exception as e:
        print(f"Error standardizing data types: {e}")
        return df

def normalize_text_data(df):
    """
    Standardize text columns
    """
    # Convert course_name to title case
    df['course'] = df['course'].str.title()
    
    # Strip whitespace
    df['course'] = df['course'].str.strip()
    
    return df

def filter_age_range(df, min_age=18, max_age=45):
    """
    Filter out records with age outside specified range
    """
    initial_count = len(df)
    df = df[(df['age'] >= min_age) & (df['age'] <= max_age)]
    filtered_count = len(df)
    
    print(f"\nRemoved {initial_count - filtered_count} records with age outside {min_age}-{max_age} range")
    return df

def standardize_binary_values(df):
    """
    Standardize binary columns like is_intern
    """
    # Create mapping for various possible values
    intern_mapping = {
        'yes': 'Yes',
        'y': 'Yes',
        'true': 'Yes',
        '1': 'Yes',
        'no': 'No',
        'n': 'No',
        'false': 'No',
        '0': 'No'
    }
    
    df['is_intern'] = df['is_intern'].str.lower()
    df['is_intern'] = df['is_intern'].map(intern_mapping).fillna('No')
    
    return df

def save_cleaned_data(df, output_path):
    """
    Save the cleaned dataset
    """
    try:
        df.to_csv(output_path, index=False)
        print(f"\nCleaned dataset saved successfully to {output_path}")
    except Exception as e:
        print(f"Error saving cleaned dataset: {e}")

def main():
    # File paths
    input_file = "student_data.csv"  # Replace with your input file path
    output_file = "cleaned_student_data.csv"
    
    # Step 1: Load Dataset
    print("Step 1: Loading Dataset...")
    df = load_dataset(file_path)
    if df is None:
        return
    
    # Step 2: Handle Missing Values
    print("\nStep 2: Handling Missing Values...")
    df = check_missing_values(df)
    
    # Step 3: Standardize Data Types
    print("\nStep 3: Standardizing Data Types...")
    df = standardize_datatypes(df)
    
    # Step 4: Normalize Text Data
    print("\nStep 4: Normalizing Text Data...")
    df = normalize_text_data(df)
    
    # Step 5: Filter Age Range
    print("\nStep 5: Filtering Age Range...")
    df = filter_age_range(df)
    
    # Step 6: Standardize Binary Values
    print("\nStep 6: Standardizing Binary Values...")
    df = standardize_binary_values(df)
    
    # Step 7: Save Cleaned Data
    print("\nStep 7: Saving Cleaned Data...")
    save_cleaned_data(df, output_file)
    
    # Print final summary
    print("\n=== Final Data Summary ===")
    print(f"Final number of records: {len(df)}")
    print("\nSample of cleaned data:")
    print(df.head())
    print("\nColumn info:")
    print(df.info())

if __name__ == "__main__":
    main()