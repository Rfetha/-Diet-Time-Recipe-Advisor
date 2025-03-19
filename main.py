# source /home/ersoy/global_venv_file/.venv/bin/activate
import pandas as pd
import numpy as np
from recommendation_model import recommend, df_prepare

def main():
    
    max_Calories = 800
    max_daily_Fat = 100
    max_daily_Saturatedfat = 13
    max_daily_Cholesterol = 300
    max_daily_Sodium = 2300
    max_daily_Carbohydrate = 325
    max_daily_Fiber = 40
    max_daily_Sugar = 40
    max_daily_Protein = 60
    max_nutritional_values = [max_Calories, max_daily_Fat, max_daily_Saturatedfat, 
                max_daily_Cholesterol, max_daily_Sodium, 
                max_daily_Carbohydrate, max_daily_Fiber, max_daily_Sugar, max_daily_Protein]

    min_Calories = 500
    min_daily_Fat = 0
    min_daily_Saturatedfat = 0
    min_daily_Cholesterol = 0
    min_daily_Sodium = 0
    min_daily_Carbohydrate = 0
    min_daily_Fiber = 0
    min_daily_Sugar = 0
    min_daily_Protein = 30
    min_nutritional_values = [min_Calories, min_daily_Fat, min_daily_Saturatedfat, 
                min_daily_Cholesterol, min_daily_Sodium, 
                min_daily_Carbohydrate, min_daily_Fiber, min_daily_Sugar, min_daily_Protein]
     
    df = df_prepare()
    # Calories,Fat,SaturatedFat,Cholesterol,Sodium,Carbs,Fiber,Sugar,Protein
    # test_input = df.iloc[0:1, 6:15].to_numpy()
    test_input = np.array([[800, 10, 2, 30, 200, 40, 5, 20, 15]])

    try:
        recommended_items = recommend(df, 
                                      _input=test_input, 
                                      min_nutritional_values=min_nutritional_values, 
                                      max_nutritional_values=max_nutritional_values, 
                                      ingredient_filter=['sugar'], 
                                      params={'return_distance': False})
        #print(recommended_items.columns)
        recommended_items_columns = [
            'Name', 'RecipeIngredientParts', 'Calories', 'FatContent',
            'SaturatedFatContent', 'CholesterolContent', 'SodiumContent',
            'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent',
            'RecipeInstructions'
       ]
        filtered_recommended_items = recommended_items[recommended_items_columns]

        for x in range(len(filtered_recommended_items)): 
            print(f"Recommendation Number {x + 1}:")  # Kullanıcı dostu numaralandırma için +1 ekledik
            for y in range(len(recommended_items_columns)):  
                print(f"{recommended_items_columns[y]}: {filtered_recommended_items.iloc[x, y]}")
            print("-" * 50) 

        # print(recommended_items[recommended_items_columns])
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()