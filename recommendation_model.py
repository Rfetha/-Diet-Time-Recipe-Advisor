import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer


# Load data
def df_prepare(path="data/recipes.csv"):
    data = pd.read_csv(path)
    df = data.copy()

    # Select relevant columns
    columns = [ "RecipeId", "Name", "CookTime", "PrepTime", "TotalTime", "RecipeIngredientParts",
                "Calories", "FatContent", "SaturatedFatContent", "CholesterolContent",
                "SodiumContent", "CarbohydrateContent", "FiberContent", "SugarContent", "ProteinContent",
                "RecipeInstructions" 
    ]
    df = df[columns]
    return df

# Function for scaling
def scaling(dataframe):
    scaler = StandardScaler()
    prep_data = scaler.fit_transform(dataframe.iloc[:, 6:15].to_numpy())
    return prep_data, scaler

# Function for nearest neighbors prediction
def nn_predictor(prep_data, n_neighbors):
    neigh = NearestNeighbors(n_neighbors=n_neighbors, metric='cosine', algorithm='brute')
    neigh.fit(prep_data)
    return neigh

# Function to build pipeline
def build_pipeline(neigh, scaler, params):
    transformer = FunctionTransformer(neigh.kneighbors, kw_args=params)
    pipeline = Pipeline([('std_scaler', scaler), ('NN', transformer)])
    return pipeline

# Function to extract filtered data
def extract_data(dataframe, ingredient_filter, min_nutritional_values, max_nutritional_values):
    extracted_data = dataframe.copy()
    
    # Apply minimum, maximum nutritional value filters
    for column, minimum in zip(extracted_data.columns[6:15], min_nutritional_values):
        extracted_data = extracted_data[extracted_data[column] >= minimum]
    
    for column, maximum in zip(extracted_data.columns[6:15], max_nutritional_values):
        extracted_data = extracted_data[extracted_data[column] < maximum]
    
    if ingredient_filter is not None:
        for ingredient in ingredient_filter:
            extracted_data = extracted_data[extracted_data['RecipeIngredientParts'].str.contains(ingredient, regex=False)] 
    
    if extracted_data.empty:
        raise ValueError("No data left after filtering. Check your nutritional value or ingredient filters.")
    
    return extracted_data

# Function to apply the pipeline to input
def apply_pipeline(pipeline, _input, extracted_data):
    return extracted_data.iloc[pipeline.transform(_input)[0]]

# End-to-end recommendation function
def recommend(answer_number, dataframe, _input, min_nutritional_values, max_nutritional_values, ingredient_filter=None, params={'return_distance': False}):
    extracted_data = extract_data(dataframe, ingredient_filter, min_nutritional_values, max_nutritional_values)
    print(f"Extracted data shape: {extracted_data.shape}")  # Check the shape of the data after filtering
    
    prep_data, scaler = scaling(extracted_data)
    print(f"Prepared data shape: {prep_data.shape}")  # Check if scaling is working
    
    neigh = nn_predictor(prep_data, answer_number)
    pipeline = build_pipeline(neigh, scaler, params)
    
    return apply_pipeline(pipeline, _input, extracted_data)
