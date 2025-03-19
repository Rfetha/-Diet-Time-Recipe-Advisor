import streamlit as st
import pandas as pd
import numpy as np
import re
from recommendation_model import recommend, df_prepare

def main():
    st.title("Recipe Recommendation System")
    
    # Get nutritional values from the user
    min_Calories = st.number_input("Minimum Calories", min_value=0, max_value=2000, value=500)
    max_Calories = st.number_input("Maximum Calories", min_value=0, max_value=2000, value=800)
    
    min_Protein = st.number_input("Minimum Protein", min_value=0, max_value=200, value=30)
    max_Protein = st.number_input("Maximum Protein", min_value=0, max_value=200, value=60)
    
    min_Fat = st.number_input("Minimum Fat", min_value=0, max_value=200, value=0)
    max_Fat = st.number_input("Maximum Fat", min_value=0, max_value=200, value=100)
    
    min_Sugar = st.number_input("Minimum Sugar", min_value=0, max_value=200, value=0)
    max_Sugar = st.number_input("Maximum Sugar", min_value=0, max_value=200, value=40)
    
    ingredient_filter = st.text_input("Ingredients to Exclude (Separate with Commas), Leave Blank if None", "sugar")
    ingredient_filter = [x.strip() for x in ingredient_filter.split(",")]

    answer_number = st.number_input("How many recipe do you want", min_value=1, max_value=5, value=3)
    
    if st.button("Get Recommendation"):
        
        df = df_prepare()

        min_values = [min_Calories, min_Fat, 0, 0, 0, 0, 0, min_Sugar, min_Protein]
        max_values = [max_Calories, max_Fat, 13, 300, 2300, 325, 40, max_Sugar, max_Protein]
        
        test_input = np.array([[800, 10, 2, 30, 200, 40, 5, 20, 15]])
        
        try:
            recommended_items = recommend(answer_number,
                                          df, 
                                          _input=test_input, 
                                          min_nutritional_values=min_values, 
                                          max_nutritional_values=max_values, 
                                          ingredient_filter=ingredient_filter, 
                                          params={'return_distance': False})
            
            if not recommended_items.empty:
                st.write("**Recommended Recipes:**")
                recommended_items_columns = ["Name", "RecipeIngredientParts", "RecipeInstructions", "Calories", "ProteinContent"]
                
                for idx, row in recommended_items.iterrows():
                    #st.write(f"### Recommendation {idx + 1}:")
                    for col in recommended_items_columns:
                        if col == "RecipeIngredientParts" :
                            output = ", ".join(row[col]) if isinstance(row[col], list) else row[col]
                            cleaned_output = re.sub(r'c\((.*?)\)', lambda m: m.group(1).replace('"', ''), output)
                            st.write(f"**{col}:** {cleaned_output}")

                        elif col == "RecipeInstructions":
                            output = row[col]
                            output = output[2:-1]
                            cleaned_output = re.sub(r'c\((.*?)\)', r'\1', output)  
                            cleaned_output = cleaned_output.replace('"', '') 
                            st.write(f"**{col}:**\n{cleaned_output}")
                
                        else:
                            st.write(f"**{col}:** {row[col]}")

                    st.write("---")

        except ValueError as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()